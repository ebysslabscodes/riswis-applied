# RISWIS Applied

RISWIS Applied is a governance layer that controls and exposes ranking decisions in retrieval systems.

It controls what the system sees before generation and makes ranking decisions visible, inspectable, and auditable.

This is not a model.
This is not a replacement for RAG.

RISWIS Applied sits between retrieval and generation and makes ranking behavior explicit.

---

## Run It (Quick Start)

### 1. Create environment

python -m venv .venv
..venv\Scripts\Activate.ps1

### 2. Install dependencies

pip install -r requirements.txt

### 3. Ingest documents

python ingest.py

### 4. Run query

python main.py --query "feeling tired all the time"

---

## Core Idea

Most systems retrieve information and pass it directly into a model.

The selection step — what gets chosen and why — is usually hidden.

RISWIS Applied separates two things:

* semantic similarity (what matches the query)
* policy weighting (what should be prioritized)

Both remain visible.

---

## Where It Fits

Data → Retrieval → RISWIS (GRL) → LLM → Output

RISWIS introduces a Governance Retrieval Layer (GRL) between retrieval and generation.

The GRL:

* applies structured weighting based on source tiers
* reorders results based on policy
* exposes ranking changes before generation
* produces auditable outputs

---

## What It Does

For each query, RISWIS Applied:

* retrieves documents using semantic similarity
* applies policy weighting using tier multipliers
* produces a final ranked list
* records what changed and why

Outputs are deterministic and inspectable.

---

## Example Behavior

A document may rank #1 by similarity but drop to #2 after policy is applied.

Another document may move from #2 to #1 due to higher trust weighting.

RISWIS makes this movement visible:

raw_rank → weighted_rank → delta

This exposes when policy overrides similarity.

---

## Output

Each run produces three files:

* ranked_results.json
* policy_decision.json
* run_summary.json

These are the only outputs. No intermediate or temporary artifacts are stored.

---

## Why It Exists

Modern systems make decisions before answering.

Those decisions are rarely visible.

RISWIS Applied makes these decisions explicit and inspectable before generation.

This allows:

* inspection of ranking behavior
* verification of policy influence
* auditability before generation
* controlled integration into existing systems

---

## Positioning

RISWIS Applied is not:

* a model
* a retrieval system
* a search engine

RISWIS Applied is:

* a governance layer
* a ranking control system
* a visibility layer for retrieval behavior

It can be used alongside existing retrieval systems without replacing them.

---

## Data

RISWIS Applied is data-agnostic.

It does not include bundled datasets.

Users provide:

* documents
* tier assignments
* policy configuration

---

## Example Use

python main.py --query "causes of chronic fatigue"

---

## Design Principles

* visibility over opacity
* control over automation
* deterministic outputs
* minimal storage
* integration over replacement

---

## Troubleshooting

### NumPy error (`np.float_`)

If you see an error related to `np.float_`, ensure NumPy is pinned:

numpy<2

Then reinstall:

pip uninstall -y numpy chromadb chroma-hnswlib
pip install -r requirements.txt

---

### Chroma database errors

If you see errors during ingest or query (SQLite / seq_id / TypeError):

Delete the local vector store:

Remove-Item -Recurse -Force .\chroma_db

Then rebuild:

python ingest.py

---

## Current Scope

RISWIS Applied focuses on:

* ranking visibility
* policy influence
* controlled output

It does not include:

* model training
* generation logic
* external APIs

---

## Status

Initial product build focused on establishing core behavior and observable ranking control.

---

## Summary

RISWIS Applied controls what the system sees before it answers.

It makes ranking decisions visible.
It makes policy influence measurable.

---

## License

To be defined.
