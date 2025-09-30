"""Aggregate and visualize experiment results.

Usage:
  python -m experiments.analyze_results \
    --files experiments/out/results_weaver.json \
             experiments/out/results_zero_shot.json \
             experiments/out/results_broadcast.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def load_runs(files: List[str]) -> pd.DataFrame:
    records: List[Dict[str, Any]] = []
    for fp in files:
        data = json.loads(Path(fp).read_text("utf-8"))
        agent_type = Path(fp).stem.replace("results_", "")
        for r in data.get("runs", []):
            records.append(
                {
                    "agent_type": agent_type,
                    "success": int(bool(r.get("success"))),
                    "leakage": int(1 if r.get("leakage", 0) else 0),
                    "efficiency": r.get("turns", 0),
                }
            )
    return pd.DataFrame(records)


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("agent_type").agg(
        success_rate=("success", "mean"),
        leakage_rate=("leakage", "mean"),
        efficiency_mean=("efficiency", "mean"),
        efficiency_std=("efficiency", "std"),
        n=("success", "count"),
    )
    return grouped.reset_index()


def plot_bar(df: pd.DataFrame, metric: str, ylabel: str, outfile: Path):
    plt.figure(figsize=(6,4))
    ax = sns.barplot(data=df, x="agent_type", y=metric, errorbar="sd")
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Agent Type")
    ax.set_title(metric)
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f"{height:.2f}", (p.get_x()+p.get_width()/2, height), ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    outfile.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(outfile, dpi=180)
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", required=True, help="Result JSON files")
    parser.add_argument("--outdir", default="experiments/analysis", help="Output dir for charts")
    args = parser.parse_args()

    df = load_runs(args.files)
    if df.empty:
        print("No data loaded.")
        return
    summary = summarize(df)
    print("Summary:\n", summary)

    outdir = Path(args.outdir)
    plot_bar(summary, "success_rate", "Task Success Rate", outdir / "success_rate.png")
    plot_bar(summary, "leakage_rate", "Information Leakage Rate", outdir / "leakage_rate.png")
    plot_bar(summary, "efficiency_mean", "Negotiation Efficiency (turns)", outdir / "efficiency.png")

    # Write summary markdown
    try:
        md_table = summary.to_markdown(index=False)
    except Exception:
        md_table = summary.to_string(index=False)
    md = ["# Experiment Summary", "", md_table]
    (outdir / "RESULTS_SUMMARY.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
