# RISWIS Applied

**semantic winner ≠ policy winner**

RISWIS Applied is a governance layer that controls and exposes ranking decisions in retrieval systems.

It determines what the system sees before generation and makes ranking decisions visible, inspectable, and auditable.

> This is not a model.  
> This is not a replacement for RAG.  
> RISWIS Applied sits between retrieval and generation and makes ranking behavior explicit.

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

```
Data → Retrieval → RISWIS (GRL) → LLM → Output
```

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

```bash
git clone https://github.com/ebysslabscodes/riswis-applied.git
cd riswis-applied
```

---

### 2. Check installed Python versions

```powershell
py -0
```

You should see:

```
-3.11
```

If 3.11 is not listed, install it first:  
https://www.python.org/downloads/

---

### 3. Create virtual environment (FORCE Python 3.11)

```powershell
py -3.11 -m venv .venv
```

---

### 4. Activate environment

**Windows:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Mac/Linux:**

```bash
source .venv/bin/activate
```

You should now see:

```
(.venv) PS C:\...
```

---

### 5. Verify Python version (CRITICAL)

```powershell
python --version
```

Must show:

```
Python 3.11.x
```

If not → delete `.venv` and restart.

---

### 6. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

---

### 7. Install dependencies

```powershell
pip install -r requirements.txt
```

---

### 8. Ingest documents

```powershell
python ingest.py
```

---

### 9. Run query

```powershell
python main.py --query "feeling tired all the time"
```

---

## Demo Data

The repository includes a small demo corpus (`doc_101`–`doc_106`) with predefined source tiers.

Run `python ingest.py` to load them before querying.

---

## What You'll See

Each result includes:

- `raw_rank` → semantic similarity ranking
- `weighted_rank` → ranking after policy weighting
- `delta` → movement caused by policy

You can directly observe:

- when policy overrides similarity
- which document wins
- why the decision occurred

---

## Example Output (Rank Flip)

```json
{
  "document_id": "doc_101",
  "source_tier": "T2",
  "raw_rank": 1,
  "weighted_rank": 2,
  "similarity_score": 0.91,
  "multiplier": 1.0,
  "final_score": 0.91
},
{
  "document_id": "doc_104",
  "source_tier": "T1",
  "raw_rank": 2,
  "weighted_rank": 1,
  "similarity_score": 0.87,
  "multiplier": 1.3,
  "final_score": 1.13
}
```

This shows a **policy override**:

- semantic winner → `doc_101`
- policy winner → `doc_104`

This is the core behavior of RISWIS.

---

## Output

Each run produces:

- `ranked_results.json`
- `policy_decision.json`
- `run_summary.json`

No intermediate artifacts are stored.

---

## Core Idea

RISWIS Applied separates:

- **semantic similarity** → what matches
- **policy weighting** → what should win

Both remain visible.

---

## Troubleshooting

### Setup failed

Start clean:

```powershell
Remove-Item -Recurse -Force .\.venv
```

Then rebuild:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
pip install -r requirements.txt
```

---

### Wrong Python version

```powershell
python --version
```

If not 3.11 → delete `.venv` and recreate it.

---

### ModuleNotFoundError

Environment is broken. Reset it:

```powershell
Remove-Item -Recurse -Force .\.venv
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### Chroma errors

```powershell
Remove-Item -Recurse -Force .\chroma_db
python ingest.py
```

---

## Positioning

RISWIS Applied is **not**:

- a model
- a retrieval system
- a search engine

RISWIS Applied **is**:

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

Licensed under the **Ebysslabs Ethical Use License v1.1**  
(CC BY-ND 4.0 base with additional restrictions)

- No military use
- No surveillance use
- No law enforcement use

© 2026 Ronald Reed (Ebysslabs)