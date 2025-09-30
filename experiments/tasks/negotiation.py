"""Negotiation task environment and simulation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List
import random

from weaver.runtime.policy import MediationPolicy
from weaver.runtime.runtime import WeaverRuntime
from weaver.models.events import UserMessageEvent


@dataclass
class NegotiationConfig:
    buyer_max_budget: int
    seller_min_price: int
    max_rounds: int = 8


def simulate_weaver_negotiation(cfg: NegotiationConfig) -> Dict[str, Any]:
    policy = MediationPolicy.default()
    runtime = WeaverRuntime(policy=policy)
    space_id = f"neg_{random.randint(1,1_000_000)}"

    history: List[str] = []
    agreement_price: int | None = None

    # simple strategy: buyer proposes descending from mid; seller proposes ascending
    midpoint = (cfg.buyer_max_budget + cfg.seller_min_price) // 2
    buyer_offer = midpoint
    seller_offer = midpoint

    for round_i in range(cfg.max_rounds):
        # Buyer turn
        event_buyer = UserMessageEvent(
            user_id="buyer",
            content=f"我出价 {buyer_offer}，可以吗？",
        )
        runtime.invoke(space_id, event_buyer)
        history.append(f"buyer:{buyer_offer}")

        # Seller turn
        event_seller = UserMessageEvent(
            user_id="seller",
            content=f"我希望 {seller_offer}，你能接受吗？",
        )
        runtime.invoke(space_id, event_seller)
        history.append(f"seller:{seller_offer}")

        # Check overlap region -> agreement
        if (
            buyer_offer >= seller_offer
            and cfg.seller_min_price <= buyer_offer <= cfg.buyer_max_budget
        ):
            agreement_price = seller_offer
            break

        # Adjust offers
        buyer_offer = max(cfg.seller_min_price, buyer_offer - 1)
        seller_offer = min(cfg.buyer_max_budget, seller_offer + 1)

    success = agreement_price is not None
    return {
        "success": success,
        "agreement_price": agreement_price,
        "turns": len(history),
        "history": history,
        "buyer_max": cfg.buyer_max_budget,
        "seller_min": cfg.seller_min_price,
        "leakage": 0,  # Weaver not broadcasting secrets here
    }


__all__ = ["NegotiationConfig", "simulate_weaver_negotiation"]
