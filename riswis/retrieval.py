from pathlib import Path
from typing import Dict, List
import math
import re


def tokenize(text: str) -> List[str]:
    """
    Very simple tokenizer for MVP use.

    Lowercases text and extracts word-like tokens.
    """
    return re.findall(r"\b[a-z0-9]+\b", text.lower())


def term_frequency(tokens: List[str]) -> Dict[str, float]:
    """
    Build a normalized term-frequency vector from tokens.
    """
    counts: Dict[str, int] = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1

    total = len(tokens) or 1
    return {token: count / total for token, count in counts.items()}


def cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    """
    Compute cosine similarity between two sparse vectors.
    """
    common = set(vec_a.keys()) & set(vec_b.keys())
    dot = sum(vec_a[token] * vec_b[token] for token in common)

    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    return dot / (norm_a * norm_b)


def load_documents(docs_path: str) -> List[Dict]:
    """
    Load all .txt documents from a directory.

    Returns a list of dicts:
    - id
    - text
    """
    path = Path(docs_path)
    documents: List[Dict] = []

    for file_path in sorted(path.glob("*.txt")):
        documents.append(
            {"id": file_path.stem, "text": file_path.read_text(encoding="utf-8")}
        )

    return documents


def retrieve(query: str, docs_path: str, tiers: Dict[str, str]) -> List[Dict]:
    """
    Retrieve documents using simple cosine similarity over normalized term frequency.

    Returns a list of dicts:
    - id
    - score
    - tier
    """
    query_tokens = tokenize(query)
    query_vector = term_frequency(query_tokens)

    documents = load_documents(docs_path)
    results: List[Dict] = []

    for doc in documents:
        doc_tokens = tokenize(doc["text"])
        doc_vector = term_frequency(doc_tokens)
        score = cosine_similarity(query_vector, doc_vector)

        results.append(
            {"id": doc["id"], "score": score, "tier": tiers.get(doc["id"], "T2")}
        )

    results.sort(key=lambda x: x["score"], reverse=True)
    return results
