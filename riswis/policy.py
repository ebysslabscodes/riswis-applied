from typing import List, Dict


def apply_policy(results: List[Dict], tier_multipliers: Dict[str, float]) -> List[Dict]:
    """
    Apply governance weighting to retrieval results.

    Input results must already be sorted by semantic similarity descending.

    Each result must contain:
    - id
    - score
    - tier

    Returns results with:
    - raw_rank
    - weighted_score
    - weighted_rank
    - delta
    """

    updated = []

    # Preserve semantic rank order
    for idx, r in enumerate(results, start=1):
        tier = r.get("tier")
        multiplier = tier_multipliers.get(tier, 1.0)
        weighted_score = r["score"] * multiplier

        updated.append(
            {
                "id": r["id"],
                "score": r["score"],
                "tier": tier,
                "multiplier": multiplier,
                "raw_rank": idx,
                "weighted_score": weighted_score,
            }
        )

    # Sort by weighted score descending
    updated.sort(key=lambda x: x["weighted_score"], reverse=True)

    # Assign weighted rank and delta
    for idx, r in enumerate(updated, start=1):
        r["weighted_rank"] = idx
        r["delta"] = r["raw_rank"] - r["weighted_rank"]

    return updated


def detect_rank_flip(raw_results: List[Dict], weighted_results: List[Dict]) -> Dict:
    """
    Detect whether policy changed the top result.

    Returns:
    - semantic_winner
    - policy_winner
    - flipped
    - reason
    """

    semantic_winner = raw_results[0]["id"] if raw_results else None
    policy_winner = weighted_results[0]["id"] if weighted_results else None
    flipped = semantic_winner != policy_winner

    reason = (
        "Policy weighting overrode semantic similarity"
        if flipped
        else "Semantic and policy winners match"
    )

    return {
        "semantic_winner": semantic_winner,
        "policy_winner": policy_winner,
        "flipped": flipped,
        "reason": reason,
    }
