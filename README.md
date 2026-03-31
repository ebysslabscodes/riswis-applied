# RISWIS Applied

semantic winner ≠ policy winner

RISWIS Applied is a governance layer that controls and exposes ranking decisions in retrieval systems.

It determines what the system sees before generation and makes ranking decisions visible, inspectable, and auditable.

This is not a model.
This is not a replacement for RAG.

RISWIS Applied sits between retrieval and generation and makes ranking behavior explicit.

---

## Requirements

Python 3.10–3.11 recommended  
Python 3.13 is not supported due to dependency limitations (NumPy / PyTorch)

---

## Run It (Quick Start)

### 1. Clone the repository

git clone https://github.com/ebysslabscodes/riswis-applied.git
cd riswis-applied

### 2. Create environment (Python 3.11 recommended)

py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

### 3. Install dependencies

pip install -r requirements.txt

### 4. Ingest documents

python ingest.py

### 5. Run query

python main.py --query "feeling tired all the time"

---

## What You’ll See

Each result includes:

- raw_rank → semantic similarity ranking
- weighted_rank → ranking after policy weighting
- delta → movement caused by policy

You can directly observe:

- when policy overrides similarity
- which document wins
- why the decision occurred

---

## Core Idea

Most systems retrieve information and pass it directly into a model.

The selection step — what gets chosen and why — is usually hidden.

RISWIS Applied separates two components:

- semantic similarity (what matches the query)
- policy weighting (what should be prioritized)

Both remain visible.

---

## Where It Fits

Data → Retrieval → RISWIS (GRL) → LLM → Output

RISWIS introduces a Governance Retrieval Layer (GRL) between retrieval and generation.

The GRL:

- applies structured weighting based on source tiers
- reorders results according to policy
- exposes ranking changes before generation
- produces auditable outputs

---

## What It Does

For each query, RISWIS Applied:

- retrieves documents using semantic similarity
- applies policy weighting using tier multipliers
- produces a final ranked list
- records what changed and why

Outputs are deterministic and inspectable.

---

## Example Behavior

A document may rank #1 by similarity but drop to #2 after policy is applied.

Another document may move from #2 to #1 due to higher trust weighting.

RISWIS makes this movement visible:

raw_rank → weighted_rank → delta

This shows when policy overrides similarity.

---

## Output

Each run produces three files:

- ranked_results.json
- policy_decision.json
- run_summary.json

No intermediate or temporary artifacts are stored.

---

## Why It Exists

Ranking decisions happen before a system generates an answer.

Those decisions are usually hidden.

RISWIS Applied makes them visible before generation.

You can see exactly:

- what was selected
- what changed
- why it changed

---

## Positioning

RISWIS Applied is not:

- a model
- a retrieval system
- a search engine

RISWIS Applied is:

- a governance layer
- a ranking control system
- a visibility layer for retrieval behavior

It integrates with existing retrieval systems without replacing them.

---

## Data

RISWIS Applied is data-agnostic.

Users provide:

- documents
- tier assignments
- policy configuration

---

## Design Principles

- visibility over opacity
- control over automation
- deterministic outputs
- minimal storage
- integration over replacement

---

## Troubleshooting

### NumPy error (np.float_)

If you see an error related to np.float_, ensure NumPy is pinned:

numpy<2

Then reinstall:

pip uninstall -y numpy chromadb chroma-hnswlib
pip install -r requirements.txt

---

### Chroma database errors

If you see errors during ingest or query:

Remove-Item -Recurse -Force .\chroma_db

Then rebuild:

python ingest.py

---

## Current Scope

RISWIS Applied focuses on:

- ranking visibility
- policy influence
- controlled output

It does not include:

- model training
- generation logic
- external APIs

---

## Status

Stable core behavior.

Designed for integration into existing retrieval systems.

---

## Summary

RISWIS Applied controls what the system sees before it answers.

It makes ranking decisions visible.  
It makes policy influence measurable.

---

## License

Licensed under the Ebysslabs Ethical Use License v1.1  
(CC BY-ND 4.0 base with additional restrictions)

- No military use
- No surveillance use
- No law enforcement use

© 2026 Ronald Reed (Ebysslabs)