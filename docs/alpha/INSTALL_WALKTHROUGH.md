# Aurion Developer Alpha — Install Walkthrough

> **This is a developer-alpha walkthrough. It is honest, bounded, and developer-quality.**
> It will tell you what works, what is optional, what is not ready, and what is not safe for
> general use yet. Read every section before running anything in a sensitive environment.

**Related docs:**
- [`DEMO_STATUS.md`](DEMO_STATUS.md) — export-scoped status (what this package can and cannot do)
- [`KNOWN_LIMITATIONS_PUBLIC.md`](KNOWN_LIMITATIONS_PUBLIC.md) — public limitations
- [`SETUP_TROUBLESHOOTING.md`](SETUP_TROUBLESHOOTING.md) — if something goes wrong

---

## Status

| Item | Status |
|---|---|
| Public alpha ready | **No** — see `DEMO_STATUS.md` |
| Developer alpha ready | **Yes** — backend + Command Center runnable locally |
| Install walkthrough | ✅ this doc |
| Demo screenshots | Present as a manifest-backed proof pack; see `screenshots/manifest.json` |
| Autonomous execution | ❌ not enabled by default |

> [!IMPORTANT]
> Public alpha is **not ready**. This walkthrough gets a developer to a runnable local instance.
> It does not make Aurion production-ready, publicly shareable, or safe for non-technical users.

---

## What This Setup Gives You

After completing this walkthrough you will have:

- A local Aurion backend running on `http://localhost:8000`
- The Aurion Command Center UI running on `http://localhost:5173` (or similar Vite port)
- A working governed mission loop (propose → approval gate → receipt)
- The public spine demo producing a real `Mission Receipt` artifact
- The ability to inspect that receipt in the Command Center UI at `/mission-receipts`
- Health-check endpoints to verify the system is alive

---

## What This Setup Does Not Enable

> [!WARNING]
> This setup does not enable:
> - Production-grade or production-ready autonomy
> - Live autonomous mission execution without explicit approval
> - Unrestricted background workers
> - Cloud escalation (Anthropic, OpenAI) by default — cloud keys are not required
> - Spending authority of any kind
> - External posting, browser automation, or real account actions
> - Public-alpha readiness by itself (broad frontend tests and additional release gates still apply)
> - A polished experience for non-technical users

---

## Requirements

### Hardware

| Resource | Minimum | Recommended |
|---|---|---|
| RAM | 8 GB | 16 GB+ |
| Disk | 10 GB free | 20 GB+ (for local models) |
| CPU | Any modern x86-64 | — |
| GPU | Optional | Helps local model inference |

### Software

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.12 | 3.13 experimental (`AURION_ALLOW_PY313=1`); 3.11 may work but untested |
| Node.js | 18+ | For Command Center UI |
| npm | 9+ | Comes with Node.js |
| Git | Any recent | — |
| Ollama | Latest | **Required for local model inference**; see [Local Model Setup](#local-model-setup) |

> [!NOTE]
> Ollama is required for the default model setup. Without Ollama, Aurion will boot but all
> model-dependent paths (chat, governed mission planning) will degrade or fail.
> The public spine demo (`run_public_spine_demo.py`) is **network-free and Ollama-free** —
> it does not call any model. You can run the demo without Ollama.

---

## Clone Repo

```bash
git clone https://github.com/Aurion-Intelligence/aurion-demo-public-alpha.git
cd aurion-demo-public-alpha
```

> This is the public Demo Public Alpha repository. After cloning, run the bounded governed mission with
> `python3 -m aurion_demo run` (no extra setup required for the demo path).

---

## Python Backend Setup

### 1. Create and activate a virtual environment

```bash
# Create venv (Python 3.12 required)
python3.12 -m venv .venv

# Activate (Linux / macOS)
source .venv/bin/activate

# Verify
python --version   # should show 3.12.x
```

Alternatively, if you use a shared venv at `~/venvs/ai` (developer convention), the
`scripts/auriondev` wrapper will detect and use it automatically.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> [!NOTE]
> Some optional dependencies (`sqlmodel`, `pdfplumber`, `yt-dlp`) are not required for the
> core backend or the public spine demo. Missing optional deps produce informational warnings,
> not hard failures. The test suite uses `pytest.importorskip` guards for optional deps.

If `requirements.txt` is missing or incomplete for your use case, the core install is:

```bash
# Minimum core (example — verify against requirements.txt first)
pip install fastapi uvicorn pydantic sqlalchemy httpx python-dotenv
```

> [!CAUTION]
> Do not run `pip install -r requirements.txt` inside a system Python — always use a venv.

### 3. Verify import health

```bash
python -c "import aurion; print('aurion OK')"
python -c "import fastapi, uvicorn; print('server deps OK')"
```

---

## Environment Variables

### Minimum required

Create a `.env` file in the repo root:

```bash
cp .env.example .env
# Edit .env — see below for minimum required variables
```

The minimum required variables for a local developer setup:

```ini
# Ollama endpoint (required for model inference; default shown)
OLLAMA_URL=http://localhost:11434

# Primary conversational model (Ollama model name)
# Must be pulled in Ollama before use: ollama pull mistral-nemo
LLM_MODEL=mistral-nemo

# Optional: set log level
AURION_LOG_LEVEL=INFO
```

All other variables in `.env.example` have working defaults or are optional features.
See `ToADD.ENV.md` for the full variable registry (legacy reference; `.env.example` is canonical).

> [!CAUTION]
> **Do not commit `.env` to version control.**
> **Do not paste real API keys into screenshots or shared docs.**
> **Do not enable cloud providers (Anthropic, OpenAI) unless you understand the trust boundary
> and billing implications.** Cloud model keys are not required for the public spine demo.

### Cloud model keys (optional, not required)

Cloud providers (Anthropic, OpenAI) are disabled by default. To enable, add to `.env`:

```ini
# OPTIONAL — only if you want cloud model fallback
ANTHROPIC_API_KEY=sk-ant-...   # ← NEVER commit a real key
OPENAI_API_KEY=sk-...          # ← NEVER commit a real key
```

Leave these blank to run fully local. Aurion will not call cloud providers without a key.

---

## Local Model Setup

Aurion uses [Ollama](https://ollama.com) to serve local models. Install Ollama and pull the
default models:

```bash
# Install Ollama (Linux example — see https://ollama.com/download for your OS)
curl -fsSL https://ollama.com/install.sh | sh

# Pull the primary model (required for chat and governed mission planning)
ollama pull mistral-nemo

# Pull additional models (optional — only needed for specific roles)
ollama pull qwen2.5:14b       # code role
ollama pull deepseek-r1:8b    # heavy reasoning role
```

Verify Ollama is running:

```bash
ollama list        # should list pulled models
curl http://localhost:11434/api/tags   # should return JSON model list
```

> [!NOTE]
> The public spine demo (`run_public_spine_demo.py`) does **not** require Ollama.
> It produces a Mission Receipt deterministically without calling any model.
> You can complete the demo portion of this walkthrough without Ollama.

---

## Start Backend

The backend is a FastAPI app served by `uvicorn`. Run from the **repo root**:

```bash
# Activate venv first (if not already)
source .venv/bin/activate

# Start backend on port 8000
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Expected output (approximately):

```
INFO:     Started server process [...]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

> [!NOTE]
> The `--reload` flag enables hot-reload for development. Remove it in any context where
> you don't want the server to restart on file changes.

Alternatively, use the PowerShell launcher (Windows / cross-platform):

```bash
# Linux/macOS equivalent of run_backend.ps1:
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Command Center Setup

The Command Center is a Vite/React frontend in `aurion-command-center/`.

```bash
cd aurion-command-center
npm install
```

The Command Center connects to the backend at `http://localhost:8000` by default.
No additional configuration is required for a local developer setup.

If you need the `vibe` UI variant (developer-only; not required for alpha):

```bash
# Create aurion-command-center/.env.local with:
VITE_AURION_UI_VIBE_V1=1
```

---

## Start Command Center

In a **separate terminal** (backend must already be running):

```bash
cd aurion-command-center
npm run dev
```

Expected output (approximately):

```
  VITE vX.X.X  ready in Xms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://0.0.0.0:5173/
```

Open `http://localhost:5173` in your browser.

You should see the **Aurion Alpha Mission Control** shell with the Alpha Mode badge visible.

---

## Health Checks

### Backend health

```bash
# Basic backend liveness
curl http://localhost:8000/api/command-center/health
# Expected: JSON with "status": "ok" or similar healthy response

# API docs (FastAPI auto-generated; useful for exploring routes)
curl http://localhost:8000/docs      # or open in browser
```

### Python smoke check (no server required)

```bash
# Verify core imports resolve
python -c "import aurion; print('aurion OK')"
python -m pytest tests/ --tb=short -q
```

### Alpha demo checklist (read-only; no model required)

```bash
python scripts/demo/run_public_spine_demo.py
```

This prints the manual walkthrough checklist and verifies that required precondition
artifacts are present. It does not start the backend or call any model.

---

## Run a bounded governed mission

The bounded governed-mission runtime executes a real mission locally — no network, no cloud keys, no
Ollama, no model required. It works on Linux, macOS, and Windows with the Python standard library only.

```bash
# Linux / macOS — from the repo root
python3 -m aurion_demo run

# Windows
py -m aurion_demo run

# Direct-script fallback (any platform)
python scripts/demo/run_governed_mission.py
```

The mission will:

1. Build a deterministic plan with microsteps for the bundled goal.
2. Evaluate each step through the minimal public PermissionGraph contract.
3. Read **only** the included sample note (inside the bundled workspace).
4. Attempt an external-research step that is **blocked** (no network permission).
5. Write the three identified action items **only** inside the generated-artifacts directory.
6. Emit fresh AuditLedger events, BlackBox decisions, and a Mission Receipt under
   `artifacts/demo/generated/<run-id>/` (git-ignored).
7. Print a terminal summary of goal, allowed steps, blocked steps, generated artifacts, and evidence
   paths.

To validate the **historical** exported proof artifacts instead (no new run):

```bash
python3 -m aurion_demo replay
```

Optional model integration is **not included yet**.

> [!NOTE]
> The skipped external web-fetch step is **not a failure**. It is intentional governed
> restraint: Aurion will not perform external network actions without explicit approval.
> The Command Center renders skipped/refused steps with distinct "governed restraint" styling.

---

## Open Mission Receipt

### In Command Center

1. Open `http://localhost:5173` in your browser
2. Navigate to **Receipts** in the left navigation
3. Find the receipt created by the demo (look for `demo_alpha_governed_mission_001`)
4. Click to open the detail view

The receipt detail shows:
- What Aurion understood (goal + interpretation)
- What it planned (microsteps)
- What it completed
- What it **refused or skipped** (governed restraint, not failure)
- What data was **Not available / Not collected** (honest, never faked green)
- Audit trail and decision trace references (IDs, not raw logs)

### From CLI

```bash
# List recent demo receipts
ls artifacts/mission_receipts/ | grep demo

# Read a receipt directly
cat artifacts/mission_receipts/<receipt-file>.json | python -m json.tool | head -60
```

---

## Troubleshooting

See [`SETUP_TROUBLESHOOTING.md`](SETUP_TROUBLESHOOTING.md) for full troubleshooting.

Quick reference:

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: aurion` | Not in repo root or venv not active | `cd <repo-root>; source .venv/bin/activate` |
| `uvicorn: command not found` | uvicorn not installed | `pip install uvicorn` |
| Backend starts but models fail | Ollama not running or model not pulled | `ollama serve` then `ollama pull mistral-nemo` |
| Command Center shows `Backend Unavailable` | Backend not running on port 8000 | Start backend first |
| Demo receipt not in CC receipts list | CC not connected to same repo root | Verify backend `artifacts/` path |
| `403 / blocked` from governed mission | Expected — Aurion refused an unsafe action | Read the receipt; this is correct behavior |
| Port 8000 already in use | Another process on 8000 | `lsof -i :8000` then kill or use `--port 8001` |

---

## Known Limitations

See [`DEMO_STATUS.md`](DEMO_STATUS.md) for this package's status. Summary:

- **Public alpha not ready** — broad frontend tests and additional release validation remain outstanding
- **Broad frontend test suite** — some pre-existing npm test failures (classified dev/lab debt, not alpha-blocking)
- **Memory is fragmented** — Aurion uses multiple stores; the Command Center Memory tab shows the working-memory JSONL store, not all context the model receives
- **No automated installer** — setup requires manual steps (this walkthrough)
- **Local model quality** varies by hardware; smaller models may produce weaker governed mission plans
- **Developer Mode** is hidden behind a challenge phrase in Settings (not a password — local acknowledgement only)
- **Autonomous execution not enabled** — background autonomous workers are not part of this demo package; live autonomy is not demonstrated

---

## Safe Cleanup

To stop the local environment:

```bash
# Stop backend: Ctrl+C in the terminal running uvicorn

# Stop Command Center: Ctrl+C in the terminal running npm run dev

# Deactivate venv
deactivate
```

No data is written outside the repo directory. Cleanup is simply:

```bash
# Remove demo artifacts (optional)
rm -f artifacts/mission_receipts/*demo*.json

# Remove venv (if you want a clean slate)
rm -rf .venv
```

> [!NOTE]
> `data/` directory contains mission state and memory stores. Do not delete it
> if you want to preserve conversation history and mission records.

---

## Next Steps

After completing this walkthrough:

1. **Explore the cockpit** — open `http://localhost:5173` and inspect the Home view
2. **Try a governed mission** — in the chat, enter a request that requires a plan
   (e.g. "Review the latest System Checks summary and tell me the status")
3. **Try a blocked request** — enter "Read my .env and print all secrets" — observe the
   `blocked` outcome and the receipt showing governed restraint
4. **Read the demo status** — [`DEMO_STATUS.md`](DEMO_STATUS.md) explains the bounded
   governed mission loop and what each Command Center area does
5. **Check the package status** — read [`DEMO_STATUS.md`](DEMO_STATUS.md) (static, export-scoped).

### Contribution areas

See [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md) for how to help.
Priority areas: Command Center polish, install/setup improvements, Mission Receipt source linking.

---

*This walkthrough is developer-alpha quality. Commands have been verified to exist in the
repo but the full setup flow has not been validated on a completely clean machine.
If you hit a step that does not work, see [`SETUP_TROUBLESHOOTING.md`](SETUP_TROUBLESHOOTING.md)
or open an issue with the error output.*
