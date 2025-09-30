"""Experiment metrics for negotiation tasks."""
from __future__ import annotations

from typing import List, Dict, Any


def task_success_rate(runs: List[Dict[str, Any]]) -> float:
    if not runs:
        return 0.0
    success = sum(1 for r in runs if r.get("success"))
    return success / len(runs)


def information_leakage_rate(runs: List[Dict[str, Any]]) -> float:
    if not runs:
        return 0.0
    leaks = sum(1 for r in runs if r.get("leakage", 0) > 0)
    return leaks / len(runs)


def negotiation_efficiency(runs: List[Dict[str, Any]]) -> float:
    """Average number of turns to reach agreement (lower is better).

    Non-successful runs are ignored for this average; if none succeeded returns 0.
    """
    successful_turn_counts = [r["turns"] for r in runs if r.get("success") and "turns" in r]
    if not successful_turn_counts:
        return 0.0
    return sum(successful_turn_counts) / len(successful_turn_counts)


def relationship_score(runs: List[Dict[str, Any]]) -> float:
    if not runs:
        return 0.0
    raw = [r.get("relationship_score") for r in runs]
    vals = [float(v) for v in raw if v is not None]
    if not vals:
        return 0.0
    return sum(vals) / len(vals)


__all__ = [
    "task_success_rate",
    "information_leakage_rate",
    "negotiation_efficiency",
    "relationship_score",
]
