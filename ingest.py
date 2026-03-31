from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os
from datetime import datetime, timezone

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Start persistent Chroma
client = chromadb.Client(
    Settings(
        is_persistent=True,
        persist_directory="./chroma_db",
    )
)

collection = client.get_or_create_collection(name="riswis_docs")

DOCS_PATH = "data/docs"

documents = []
ids = []

for i, filename in enumerate(sorted(os.listdir(DOCS_PATH))):
    filepath = os.path.join(DOCS_PATH, filename)

    if not filename.endswith(".txt"):
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    documents.append(text)
    ids.append(filename.replace(".txt", ""))

# Optional: clear and rebuild for clean re-ingest
existing = collection.get()
if existing["ids"]:
    collection.delete(ids=existing["ids"])

embeddings = model.encode(documents).tolist()

collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=ids,
)

print("✅ Documents embedded and stored in Chroma")

with open("last_ingest.txt", "w", encoding="utf-8") as f:
    f.write(datetime.now(timezone.utc).isoformat())

print("📝 Updated ingest timestamp")
