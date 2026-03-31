# RISWIS Applied

**semantic winner ≠ policy winner**

RISWIS Applied is a governance layer that controls and exposes ranking decisions in retrieval systems.

It determines what the system sees before generation and makes ranking decisions visible, inspectable, and auditable.

**This is not a model.**  
**This is not a replacement for RAG.**

RISWIS Applied sits between retrieval and generation and makes ranking behavior explicit.

---

## What It Does

RISWIS Applied:

- retrieves documents using semantic similarity
- applies policy weighting using tier multipliers
- produces a final ranked list
- records what changed and why

Outputs are deterministic and inspectable.

---

## Where It Fits

Data → Retrieval → RISWIS (GRL) → LLM → Output

RISWIS introduces a **Governance Retrieval Layer (GRL)** between retrieval and generation.

---

## Requirements

- **Python 3.11 required**
- Python 3.13 is **not supported**

If anything fails during setup, delete `.venv` and start over.  
Do not reuse a broken environment.

---

## Run It (Quick Start)

### 1. Clone the repository

git clone https://github.com/ebysslabscodes/riswis-applied.git  
cd riswis-applied

---

### 2. Check installed Python versions

py -0

You should see:

-3.11

If 3.11 is not listed, install it first:  
https://www.python.org/downloads/

---

### 3. Create virtual environment (FORCE Python 3.11)

py -3.11 -m venv .venv

---

### 4. Activate environment

.\.venv\Scripts\Activate.ps1

You should now see:

(.venv) PS C:\...

---

### 5. Verify Python version (CRITICAL)

python --version

Must show:

Python 3.11.x

If not → delete `.venv` and restart.

---

### 6. Upgrade pip

python -m pip install --upgrade pip

---

### 7. Install dependencies

pip install -r requirements.txt

---

### 8. Ingest documents

python ingest.py

---

### 9. Run query

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

## Example Behavior

A document may rank #1 by similarity but drop to #2 after policy is applied.

Another document may move from #2 to #1 due to higher trust weighting.

raw_rank → weighted_rank → delta

---

## Output

Each run produces:

- ranked_results.json
- policy_decision.json
- run_summary.json

No intermediate artifacts are stored.

---

## Core Idea

RISWIS Applied separates:

- semantic similarity → what matches
- policy weighting → what should win

Both remain visible.

---

## Troubleshooting

### Setup failed

Start clean:

Remove-Item -Recurse -Force .\.venv

Then rebuild:

py -3.11 -m venv .venv  
.\.venv\Scripts\Activate.ps1  
python --version  
pip install -r requirements.txt  

---

### Wrong Python version

python --version

If not 3.11 → delete `.venv` and recreate it.

---

### ModuleNotFoundError

Environment is broken. Reset it:

Remove-Item -Recurse -Force .\.venv  
py -3.11 -m venv .venv  
.\.venv\Scripts\Activate.ps1  
pip install -r requirements.txt  

---

### Chroma errors

Remove-Item -Recurse -Force .\chroma_db  
python ingest.py  

---

## Positioning

RISWIS Applied is not:

- a model
- a retrieval system
- a search engine

RISWIS Applied is:

- a governance layer
- a ranking control system
- a visibility layer

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