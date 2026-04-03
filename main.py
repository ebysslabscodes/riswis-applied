import os

os.environ["ANONYMIZED_TELEMETRY"] = "False"

from riswis.cli import main
from datetime import datetime, timezone


def check_docs_vs_ingest(docs_path="data/docs", ingest_file="last_ingest.txt"):
    """
    Warn if documents have changed since the last Chroma ingest.
    """
    if not os.path.exists(ingest_file):
        print("⚠️ No ingest record found. Run `python ingest.py`.")
        return

    with open(ingest_file, "r", encoding="utf-8") as f:
        ingest_time = datetime.fromisoformat(f.read().strip())

    latest_doc_time = max(
        datetime.fromtimestamp(
            os.path.getmtime(os.path.join(docs_path, filename)),
            timezone.utc,
        )
        for filename in os.listdir(docs_path)
        if filename.endswith(".txt")
    )

    if latest_doc_time > ingest_time:
        print("⚠️ Documents changed since last ingest. Run `python ingest.py`.")


if __name__ == "__main__":
    check_docs_vs_ingest()
    main()
