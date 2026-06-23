# Aurion Developer Alpha — Setup Troubleshooting

> For the main walkthrough, see [`INSTALL_WALKTHROUGH.md`](INSTALL_WALKTHROUGH.md).

---

## Python / venv issues

### `ModuleNotFoundError: No module named 'aurion'`

**Cause:** Running Python from outside the repo root, or venv not activated.

```bash
# Fix: always cd to repo root, then activate venv
cd /path/to/myai
source .venv/bin/activate
python -c "import aurion; print('ok')"
```

If the import still fails, confirm `PYTHONPATH` includes the repo root:

```bash
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"
```

### `python3.12: command not found`

**Cause:** Python 3.12 not installed or not on PATH.

```bash
# Check what's available
python3 --version
python3.11 --version
python3.12 --version

# Install Python 3.12 (Ubuntu/Debian example)
sudo apt install python3.12 python3.12-venv
```

### `pip install` fails with permission errors

**Cause:** Running pip against system Python instead of venv.

```bash
# Ensure venv is active (prompt should show venv name)
which python     # should point inside .venv/, not /usr/bin/
source .venv/bin/activate
pip install -r requirements.txt
```

### Optional dependency warnings during tests

Warnings like `ImportError: pdfplumber not installed` are expected for optional deps.
Tests use `pytest.importorskip` guards and skip gracefully. These are not failures.

---

## Backend issues

### `uvicorn: command not found`

```bash
pip install uvicorn
# Verify
python -m uvicorn --version
```

### Backend starts but immediately crashes

Common causes:

1. **Missing `.env`** — copy `.env.example` to `.env` and set minimum variables
2. **Import error in app code** — check the traceback; usually a missing optional dep
3. **Port already in use** — use a different port:
   ```bash
   python -m uvicorn main:app --port 8001 --reload
   ```

### `Address already in use: port 8000`

```bash
# Find what's using port 8000
lsof -i :8000
# Kill it by PID, or use a different port
python -m uvicorn main:app --port 8001 --reload
```

### Backend starts but returns 500 on all routes

Check the server logs for a traceback. Common causes:
- `.env` has wrong values (e.g. malformed `OLLAMA_URL`)
- A database file is corrupt (check `data/` directory)

---

## Ollama / local model issues

### `ollama: command not found`

```bash
# Install Ollama (Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Verify
ollama --version
```

### `connection refused` to `localhost:11434`

Ollama service is not running:

```bash
# Start Ollama service
ollama serve &

# Or use systemd (if installed as a service)
sudo systemctl start ollama

# Verify
curl http://localhost:11434/api/tags
```

### Model not found / `model mistral-nemo not found`

```bash
# Pull the missing model
ollama pull mistral-nemo

# List available models
ollama list
```

### Model loads but inference is very slow

Local model inference speed depends on hardware. On CPU-only setups, responses may take
30–120 seconds per request. This is expected for large models.

Options:
- Use a smaller model: `ollama pull mistral:7b` and set `LLM_MODEL=mistral:7b` in `.env`
- Use a GPU-enabled setup (Ollama will use GPU automatically if available)

> [!NOTE]
> The public spine demo (`run_public_spine_demo.py`) does not call Ollama.
> You can run the demo and inspect Mission Receipts without Ollama running.

---

## Command Center / UI issues

### `npm install` fails

```bash
# Ensure you're in the right directory
cd aurion-command-center
node --version    # should be 18+
npm --version

# Clear cache and retry
npm cache clean --force
npm install
```

### Command Center shows `Backend Unavailable` or `Cannot connect to backend`

1. Confirm the backend is running: `curl http://localhost:8000/api/command-center/health`
2. Confirm it's on port 8000 (Command Center defaults to `localhost:8000`)
3. Check browser console for CORS or network errors

### Command Center shows blank/white screen

1. Check browser console (F12) for JavaScript errors
2. Ensure `npm run dev` completed without errors
3. Try hard-refresh: `Ctrl+Shift+R`

### Port 5173 already in use

Vite will automatically try port 5174, 5175, etc. Check the `npm run dev` output for
the actual URL.

---

## Demo and receipt issues

### `run_public_spine_demo.py` fails with `FileNotFoundError`

Ensure you're running from the repo root:

```bash
cd /path/to/myai
python scripts/demo/run_public_spine_demo.py
```

### Demo receipt doesn't appear in Command Center `/mission-receipts`

1. Verify the artifact was created: `ls artifacts/mission_receipts/ | grep demo`
2. Confirm the backend is reading from the same repo root
3. Check the backend logs for receipt-loading errors

### Governed mission returns `blocked` status

**This is correct behavior.** Aurion blocked an unsafe action. Read the receipt — it
will explain exactly what was refused and why. This is governed restraint, not a bug.

---

## Public demo runner

### `python scripts/demo/run_public_spine_demo.py` fails

```bash
# From the repository root (standard library only — no venv or extra deps required)
python scripts/demo/run_public_spine_demo.py            # validate / replay
python scripts/demo/run_public_spine_demo.py --mode generate   # generate a fresh bounded receipt
```

The runner is offline and uses only files in this repository (no network, no cloud, no private
modules). If it reports missing evidence, confirm the `artifacts/demo/` fixtures are present. This
package's status is described in [`DEMO_STATUS.md`](DEMO_STATUS.md) — a static, export-scoped document
(there is no status generator in this public package).

---

## Getting more help

1. Read [`DEMO_STATUS.md`](DEMO_STATUS.md) for what this package can and cannot do
2. Check [`KNOWN_LIMITATIONS_PUBLIC.md`](KNOWN_LIMITATIONS_PUBLIC.md) for known limitations
3. Check `artifacts/demo/` for the demo's audit/decision-trace evidence
4. Open an issue (see [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md))
4. Run the alpha demo checklist to verify environment preconditions:
   ```bash
   python scripts/demo/run_public_spine_demo.py
   ```

If the issue is a Python import or test failure, check:

```bash
# Full smoke check
python -m pytest tests/ --tb=short -q
```
