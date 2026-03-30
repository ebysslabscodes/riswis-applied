import argparse
import json
from pathlib import Path
from typing import Dict

from riswis.engine import run


DEFAULT_MULTIPLIERS = {
    "T1": 1.5,
    "T2": 1.0,
    "T3": 0.7,
}


def load_tiers(path: str) -> Dict[str, str]:
    """
    Load document tier assignments from JSON.

    Expected format:
    {
      "doc_id": "T1",
      "doc_id_2": "T3"
    }
    """
    tiers_path = Path(path)

    if not tiers_path.exists():
        raise FileNotFoundError(f"Tiers file not found: {path}")

    with tiers_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(
            "tiers.json must contain a JSON object mapping doc IDs to tiers."
        )

    return data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="riswis",
        description="RISWIS Applied — governance-aware retrieval with visible ranking decisions.",
    )

    parser.add_argument(
        "--query",
        required=True,
        help="Query string to run against the document set.",
    )
    parser.add_argument(
        "--docs",
        default="data/docs",
        help="Path to the documents directory. Default: data/docs",
    )
    parser.add_argument(
        "--tiers",
        default="data/tiers.json",
        help="Path to the tiers JSON file. Default: data/tiers.json",
    )
    parser.add_argument(
        "--output",
        default="outputs",
        help="Path to the output directory. Default: outputs",
    )
    parser.add_argument(
        "--t1",
        type=float,
        default=DEFAULT_MULTIPLIERS["T1"],
        help="Multiplier for T1 documents. Default: 1.5",
    )
    parser.add_argument(
        "--t2",
        type=float,
        default=DEFAULT_MULTIPLIERS["T2"],
        help="Multiplier for T2 documents. Default: 1.0",
    )
    parser.add_argument(
        "--t3",
        type=float,
        default=DEFAULT_MULTIPLIERS["T3"],
        help="Multiplier for T3 documents. Default: 0.7",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    tiers = load_tiers(args.tiers)

    tier_multipliers = {
        "T1": args.t1,
        "T2": args.t2,
        "T3": args.t3,
    }

    result = run(
        query=args.query,
        docs_path=args.docs,
        tiers=tiers,
        tier_multipliers=tier_multipliers,
        output_dir=args.output,
    )

    decision = result["policy_decision"]
    summary = result["run_summary"]
    ranked_results = result["ranked_results"]

    print("\nRISWIS Applied")
    print(f"Query: {summary['query']}")
    print(f"Documents: {summary['document_count']}")
    print(f"Output directory: {args.output}")
    print()

    for item in ranked_results:
        print(
            f"{item['id']} | tier={item['tier']} | "
            f"raw_rank={item['raw_rank']} | weighted_rank={item['weighted_rank']} | "
            f"delta={item['delta']} | score={item['score']:.4f} | "
            f"mult={item['multiplier']:.2f} | weighted={item['weighted_score']:.4f}"
        )

    print()

    if decision["flipped"]:
        print("Rank flip detected")
    else:
        print("No rank flip detected")

    print(f"Semantic winner: {decision['semantic_winner']}")
    print(f"Policy winner:   {decision['policy_winner']}")
    print(f"Reason:          {decision['reason']}")
    print()
    print("Wrote:")
    print("- ranked_results.json")
    print("- policy_decision.json")
    print("- run_summary.json")


if __name__ == "__main__":
    main()
