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

Data → Retrieval → RISWIS (GRL) → LLM → Output

RISWIS introduces a **Governance Retrieval Layer (GRL)** between retrieval and generation.

---

## Requirements

- **Python 3.11 recommended**
- **Python 3.12 supported**
- **Python 3.13 may work but is not officially supported**

If setup fails, recreate the environment using Python 3.11.  
Do not reuse a broken `.venv`.

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

You should see one or more of these:

```
-3.11
-3.12
-3.13
```

---

### 3. If Python is not installed on Windows

Install Python 3.11 (recommended):

```powershell
winget install Python.Python.3.11
```

Install Python 3.12:

```powershell
winget install Python.Python.3.12
```

If `winget` is unavailable, install Python from:  
https://www.python.org/downloads/

---

### 4. Create virtual environment

**Recommended (Python 3.11):**

```powershell
py -3.11 -m venv .venv
```

**Supported (Python 3.12):**

```powershell
py -3.12 -m venv .venv
```

**Python 3.13 may work but is not officially supported:**

```powershell
py -3.13 -m venv .venv
```

---

### 5. Activate environment

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

### 6. Verify Python version

```powershell
python --version
```

Expected examples:

```
Python 3.11.x
Python 3.12.x
Python 3.13.x
```

If setup fails on 3.12 or 3.13, recreate the environment using Python 3.11.

---

### 7. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

---

### 8. Install dependencies

```powershell
pip install -r requirements.txt
```

---

### 9. Ingest documents

```powershell
python ingest.py
```

---

### 10. Run queries

General phrasing:

```powershell
python main.py --query "feeling tired all the time"
```

Trust-sensitive phrasing:

```powershell
python main.py --query "trusted medical advice for fatigue"
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

## Example Query Behavior

Behavior depends on query phrasing and source weighting.

### Query 1 — General phrasing

```powershell
python main.py --query "feeling tired all the time"
```

Typical observed behavior:

- rank movement may occur
- no top-rank flip may occur
- semantic winner and policy winner may remain the same

### Query 2 — Trust-sensitive phrasing

```powershell
python main.py --query "trusted medical advice for fatigue"
```

Typical observed behavior:

- rank flip detected
- semantic winner and policy winner differ
- policy weighting overrides semantic similarity

Some queries produce no change.  
Some queries produce measurable shifts.  
RISWIS makes both visible.

---

## Example Output (Rank Flip)

```json
{
  "document_id": "doc_101",
  "source_tier": "T1",
  "raw_rank": 4,
  "weighted_rank": 1,
  "similarity_score": 0.2493,
  "multiplier": 1.5,
  "final_score": 0.3739
},
{
  "document_id": "doc_104",
  "source_tier": "T2",
  "raw_rank": 1,
  "weighted_rank": 2,
  "similarity_score": 0.3723,
  "multiplier": 1.0,
  "final_score": 0.3723
}
```

This shows a **policy override**:

- semantic winner → `doc_104`
- policy winner → `doc_101`

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

Delete the virtual environment and start clean:

```powershell
Remove-Item -Recurse -Force .\.venv
```

Then recreate it.

**Recommended (Python 3.11):**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
pip install -r requirements.txt
```

**Supported (Python 3.12):**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
pip install -r requirements.txt
```

If 3.12 gives you problems, switch to 3.11.

---

### Wrong Python version

```powershell
python --version
```

If the environment is not using the version you intended, delete `.venv` and recreate it with the correct `py -3.x -m venv .venv` command.

---

### ModuleNotFoundError

The environment is likely broken or partially installed.

Fix:

```powershell
Remove-Item -Recurse -Force .\.venv
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### Chroma errors

Delete the local vector store and rebuild it:

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