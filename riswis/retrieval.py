import os

os.environ["ANONYMIZED_TELEMETRY"] = "False"

from typing import Dict, List

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to local persistent Chroma
client = chromadb.Client(
    Settings(
        is_persistent=True,
        persist_directory="./chroma_db",
        anonymized_telemetry=False,
    )
)

collection = client.get_or_create_collection(name="riswis_docs")


def retrieve(query: str, docs_path: str, tiers: Dict[str, str]) -> List[Dict]:
    """
    Retrieve documents from Chroma using semantic embeddings.

    Returns a list of dicts:
    - id
    - score
    - tier
    """
    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
    )

    ids = results["ids"][0]
    distances = results["distances"][0]

    output: List[Dict] = []

    for i in range(len(ids)):
        score = max(0.0, 1 - distances[i])

        output.append(
            {
                "id": ids[i],
                "score": score,
                "tier": tiers.get(ids[i], "T2"),
            }
        )

    output.sort(key=lambda x: x["score"], reverse=True)
    return output
