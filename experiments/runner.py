"""Experiment runner for negotiation tasks.

Usage (example):
    python -m experiments.runner --config experiments/sample_config.json
"""
from __future__ import annotations

import json
import argparse
import random
from pathlib import Path
from typing import Any, Dict, List
import os
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from tqdm import tqdm

from experiments.tasks.negotiation import NegotiationConfig, simulate_weaver_negotiation
from experiments.tasks.team_conflict import simulate_team_conflict_task, TeamConflictConfig
from experiments.metrics import (
    task_success_rate,
    information_leakage_rate,
    negotiation_efficiency,
)
from experiments.baselines import ZeroShotBaseline, BroadcastBaseline


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def _safe_weaver_run(cfg: NegotiationConfig) -> Dict[str, Any]:
    return simulate_weaver_negotiation(cfg)


def run_weaver(batch_cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    runs: List[Dict[str, Any]] = []
    for i in tqdm(range(batch_cfg["runs"]), desc="WeaverRuns"):
        cfg = NegotiationConfig(
            buyer_max_budget=batch_cfg["buyer_max_budget"],
            seller_min_price=batch_cfg["seller_min_price"],
            max_rounds=batch_cfg.get("max_rounds", 8),
            buyer_step=batch_cfg.get("buyer_step", 1),
            seller_step=batch_cfg.get("seller_step", 1),
            seed=batch_cfg.get("seed_base", 42) + i,
        )
        try:
            res = _safe_weaver_run(cfg)
        except Exception as e:  # capture failure but continue
            res = {
                "success": False,
                "agreement_price": None,
                "turns": 0,
                "history": [],
                "buyer_max": cfg.buyer_max_budget,
                "seller_min": cfg.seller_min_price,
                "leakage": 0,
                "error": str(e),
            }
        runs.append(res)
    return runs


def run_zero_shot(batch_cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    runs: List[Dict[str, Any]] = []
    baseline = ZeroShotBaseline()
    for i in tqdm(range(batch_cfg["runs"]), desc="ZeroShotRuns"):
        convo = [
            f"买家最高预算 {batch_cfg['buyer_max_budget']}",
            f"卖家最低心理价 {batch_cfg['seller_min_price']}",
            "请直接给出成交价。",
        ]
        r = baseline.run(convo)
        # naive parse attempt
        price = _extract_int(r["final_price"]) if r.get("final_price") else None
        success = False
        if price is not None and batch_cfg['seller_min_price'] <= price <= batch_cfg['buyer_max_budget']:
            success = True
        runs.append({
            "success": success,
            "agreement_price": price,
            "turns": 1,
            "history": convo,
            "buyer_max": batch_cfg['buyer_max_budget'],
            "seller_min": batch_cfg['seller_min_price'],
            "leakage": 1,  # this baseline exposes values directly
        })
    return runs


def run_broadcast(batch_cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    runs: List[Dict[str, Any]] = []
    for i in tqdm(range(batch_cfg["runs"]), desc="BroadcastRuns"):
        baseline = BroadcastBaseline(
            buyer_secret=batch_cfg["buyer_max_budget"],
            seller_secret=batch_cfg["seller_min_price"],
        )
        r = baseline.run()
        price = _extract_int(r["final_price"]) if r.get("final_price") else None
        success = False
        if price is not None and batch_cfg['seller_min_price'] <= price <= batch_cfg['buyer_max_budget']:
            success = True
        runs.append({
            "success": success,
            "agreement_price": price,
            "turns": 1,
            "history": [r["raw"]],
            "buyer_max": batch_cfg['buyer_max_budget'],
            "seller_min": batch_cfg['seller_min_price'],
            "leakage": 1,
        })
    return runs


def _extract_int(text: str | None) -> int | None:
    if not text:
        return None
    import re
    nums = re.findall(r"(\d+)", text)
    if not nums:
        return None
    return int(nums[0])


def aggregate_and_write(tag: str, runs: List[Dict[str, Any]], out_dir: Path) -> Dict[str, Any]:
    metrics = {
        "task_success_rate": task_success_rate(runs),
        "information_leakage_rate": information_leakage_rate(runs),
        "negotiation_efficiency": negotiation_efficiency(runs),
        "runs": runs,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / f"results_{tag}.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    return metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=False, help="Path to JSON config.")
    parser.add_argument("--out", default="experiments/out", help="Output directory")
    parser.add_argument("--agent", choices=["weaver", "zero_shot", "broadcast"], default="weaver")
    parser.add_argument("--task", choices=["negotiation", "team_conflict"], default="negotiation")
    parser.add_argument("--num-runs", type=int, help="Override runs in config")
    parser.add_argument("--model-name", type=str, help="Override model name env for this run")
    parser.add_argument("--output-file", type=str, help="Explicit output file name")
    args = parser.parse_args()

    if args.config:
        cfg = json.loads(Path(args.config).read_text("utf-8"))
    else:
        # default inline config for quick test
        cfg = {
            "runs": 5,
            "buyer_max_budget": 120,
            "seller_min_price": 80,
            "max_rounds": 6,
        }

    if args.num_runs:
        cfg["runs"] = args.num_runs

    if args.model_name:
        # allow override for underlying graph model usage
        os.environ["WEAVER_MODEL"] = args.model_name

    out_dir = Path(args.out)

    if args.task == "negotiation":
        if args.agent == "weaver":
            runs = run_weaver(cfg)
        elif args.agent == "zero_shot":
            runs = run_zero_shot(cfg)
        else:
            runs = run_broadcast(cfg)
    else:  # team_conflict
        # Build an LLM similar to baselines (reuse negotiation baseline util)
        from experiments.baselines import _get_llm  # type: ignore
        llm = _get_llm()

        def runtime_factory():
            from weaver.runtime.policy import MediationPolicy
            from weaver.runtime.runtime import WeaverRuntime
            return WeaverRuntime(policy=MediationPolicy.default())

        runs = []
        for i in tqdm(range(cfg["runs"]), desc="TeamConflictRuns"):
            if args.agent == "weaver":
                res = simulate_team_conflict_task(
                    agent_type="weaver", runtime_factory=runtime_factory, config=TeamConflictConfig(seed=42 + i)
                )
            elif args.agent == "zero_shot":
                res = simulate_team_conflict_task(
                    agent_type="zero_shot", llm=llm, config=TeamConflictConfig(seed=42 + i)
                )
            else:
                # broadcast baseline leaks by design
                from experiments.tasks.team_conflict import AliceAgent, BobAgent
                alice_tmp = AliceAgent()
                bob_tmp = BobAgent()
                res = simulate_team_conflict_task(
                    agent_type="broadcast", llm=llm, config=TeamConflictConfig(seed=42 + i)
                )
                res["leakage"] = 1
            runs.append(res)

    metrics = aggregate_and_write(args.agent + "_" + args.task, runs, out_dir)
    if args.output_file:
        # write a copy to specified file
        Path(args.output_file).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output_file).write_text(
            json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    print(json.dumps({"agent": args.agent, **metrics, "runs": "<omitted>"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
