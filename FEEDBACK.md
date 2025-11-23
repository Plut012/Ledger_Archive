# Feedback & Bug Tracker

## 📁 Project Context

**Project**: Interstellar Archive Terminal - A blockchain learning platform with retro terminal UI

**Tech Stack**:
- Backend: Python/FastAPI (serves both API + static frontend)
- Frontend: Vanilla JS (no framework), Web Audio API for sounds
- Philosophy: Simple, direct, minimal dependencies

**Key Files**:
- `backend/main.py` - Unified server (API + static files)
- `frontend/js/main.js` - App initialization, module loading
- `frontend/js/modules/*.js` - Individual modules (home, chain-viewer, crypto-vault, network-monitor, learning-guide)
- `backend/blockchain.py`, `crypto.py`, `network.py` - Core blockchain logic
- `tests/` - Pytest test suite (26 tests)

**Running**:
```bash
uv run python backend/main.py  # Starts server at http://localhost:8000
uv run pytest -v               # Run tests
```

**Documentation**:
- `docs/START_HERE.md` - Quick context for Claude
- `docs/WORKFLOW.md` - Bug fix workflow
- `docs/archive/completed_feedback.md` - Resolved issues archive
- `README.md` - User-facing docs

---

## How to Use This File
1. **Add your feedback below** under "Open Issues"
2. **Use this format**:
   ```

### Example Format:
#### [BUG/TWEAK/FEATURE]
- **Priority**: -
- **Details**: -
- **Steps to reproduce**:
  1. 
  2. 
  3. 
- **Desired behavior**: -

   ```
3. **Run the slash command** (when we create it): `/process-feedback`
4. Claude will:
   - Ask clarifying questions if needed
   - Create a plan with TodoWrite
   - Implement the fix
   - Run tests to verify nothing broke
   - Move the item to "Completed" section

---

## Open Issues

<!-- Add new issues here -->

---

## In Progress

<!-- Items Claude is currently working on -->

---

## Completed

**Recent completions are moved to**: `docs/archive/completed_feedback.md`

This keeps the active feedback file clean and focused. Check the archive for full history of resolved issues.

