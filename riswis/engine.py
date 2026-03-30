from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List
import json

from riswis.policy import apply_policy, detect_rank_flip
from riswis.retrieval import retrieve


def assign_raw_ranks(results: List[Dict]) -> List[Dict]:
    """
    Add raw_rank to similarity-ordered results.
    """
    ranked: List[Dict] = []

    for index, result in enumerate(results, start=1):
        item = dict(result)
        item["raw_rank"] = index
        ranked.append(item)

    return ranked


def merge_weighted_ranks(
    raw_results: List[Dict], weighted_results: List[Dict]
) -> List[Dict]:
    """
    Merge raw ranking information with weighted ranking information and
    compute delta movement.

    Returns a list ordered by weighted rank.
    """
    raw_lookup = {item["id"]: item for item in raw_results}
    merged: List[Dict] = []

    for weighted_rank, item in enumerate(weighted_results, start=1):
        raw_item = raw_lookup[item["id"]]
        raw_rank = raw_item["raw_rank"]
        delta = raw_rank - weighted_rank

        merged.append(
            {
                "id": item["id"],
                "tier": item["tier"],
                "score": raw_item["score"],
                "multiplier": item["multiplier"],
                "weighted_score": item["weighted_score"],
                "raw_rank": raw_rank,
                "weighted_rank": weighted_rank,
                "delta": delta,
            }
        )

    return merged


def ensure_output_dir(output_dir: str) -> Path:
    """
    Ensure output directory exists.
    """
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: Dict | List) -> None:
    """
    Write JSON with readable formatting.
    """
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def run(
    query: str,
    docs_path: str,
    tiers: Dict[str, str],
    tier_multipliers: Dict[str, float],
    output_dir: str = "outputs",
) -> Dict:
    """
    Run the RISWIS Applied pipeline.

    Steps:
    1. Retrieve documents by semantic similarity
    2. Apply GRL policy weighting
    3. Detect whether policy changed the top result
    4. Write the three product outputs

    Returns a summary dict containing all output payloads.
    """
    raw_results = retrieve(query=query, docs_path=docs_path, tiers=tiers)
    raw_results = assign_raw_ranks(raw_results)

    weighted_results = apply_policy(raw_results, tier_multipliers)
    ranked_results = merge_weighted_ranks(raw_results, weighted_results)

    decision = detect_rank_flip(raw_results, weighted_results)

    top_k = min(5, len(ranked_results))
    ranked_results = ranked_results[:top_k]

    timestamp = datetime.now(timezone.utc).isoformat()

    summary = {
        "query": query,
        "timestamp_utc": timestamp,
        "docs_path": docs_path,
        "document_count": len(raw_results),
        "tier_multipliers": tier_multipliers,
        "top_k": top_k,
        "override_detected": decision["flipped"],
        "semantic_winner": decision["semantic_winner"],
        "policy_winner": decision["policy_winner"],
        "reason": decision["reason"],
    }

    output_path = ensure_output_dir(output_dir)

    write_json(output_path / "ranked_results.json", ranked_results)
    write_json(output_path / "policy_decision.json", decision)
    write_json(output_path / "run_summary.json", summary)

    return {
        "ranked_results": ranked_results,
        "policy_decision": decision,
        "run_summary": summary,
    }
