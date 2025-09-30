"""Experiment runner for negotiation tasks.

Usage (example):
    python -m experiments.runner --config experiments/sample_config.json
"""

from __future__ import annotations

import json
import argparse
from pathlib import Path
from typing import Any, Dict, List

from experiments.tasks.negotiation import NegotiationConfig, simulate_weaver_negotiation
from experiments.metrics import (
    task_success_rate,
    information_leakage_rate,
    negotiation_efficiency,
)
from experiments.baselines import ZeroShotBaseline, BroadcastBaseline


def run_weaver(batch_cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    runs: List[Dict[str, Any]] = []
    for _ in range(batch_cfg["runs"]):
        cfg = NegotiationConfig(
            buyer_max_budget=batch_cfg["buyer_max_budget"],
            seller_min_price=batch_cfg["seller_min_price"],
            max_rounds=batch_cfg.get("max_rounds", 8),
        )
        res = simulate_weaver_negotiation(cfg)
        runs.append(res)
    return runs


def run_zero_shot(batch_cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    runs: List[Dict[str, Any]] = []
    baseline = ZeroShotBaseline()
    for _ in range(batch_cfg["runs"]):
        convo = [
            f"买家最高预算 {batch_cfg['buyer_max_budget']}",
            f"卖家最低心理价 {batch_cfg['seller_min_price']}",
            "请直接给出成交价。",
        ]
        r = baseline.run(convo)
        # naive parse attempt
        price = _extract_int(r["final_price"]) if r.get("final_price") else None
        success = False
        if (
            price is not None
            and batch_cfg["seller_min_price"] <= price <= batch_cfg["buyer_max_budget"]
        ):
            success = True
        runs.append(
            {
                "success": success,
                "agreement_price": price,
                "turns": 1,
                "history": convo,
                "buyer_max": batch_cfg["buyer_max_budget"],
                "seller_min": batch_cfg["seller_min_price"],
                "leakage": 1,  # this baseline exposes values directly
            }
        )
    return runs


def run_broadcast(batch_cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    runs: List[Dict[str, Any]] = []
    for _ in range(batch_cfg["runs"]):
        baseline = BroadcastBaseline(
            buyer_secret=batch_cfg["buyer_max_budget"],
            seller_secret=batch_cfg["seller_min_price"],
        )
        r = baseline.run()
        price = _extract_int(r["final_price"]) if r.get("final_price") else None
        success = False
        if (
            price is not None
            and batch_cfg["seller_min_price"] <= price <= batch_cfg["buyer_max_budget"]
        ):
            success = True
        runs.append(
            {
                "success": success,
                "agreement_price": price,
                "turns": 1,
                "history": [r["raw"]],
                "buyer_max": batch_cfg["buyer_max_budget"],
                "seller_min": batch_cfg["seller_min_price"],
                "leakage": 1,
            }
        )
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

    out_dir = Path(args.out)

    if args.agent == "weaver":
        runs = run_weaver(cfg)
    elif args.agent == "zero_shot":
        runs = run_zero_shot(cfg)
    else:
        runs = run_broadcast(cfg)

    metrics = aggregate_and_write(args.agent, runs, out_dir)
    print(
        json.dumps(
            {"agent": args.agent, **metrics, "runs": "<omitted>"},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
