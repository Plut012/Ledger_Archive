# Phase 02: Quick Reference Card

## Run Tests

```bash
# Backend unit tests
PYTHONPATH=backend uv run python backend/test_narrative_state.py

# Integration test
PYTHONPATH=backend uv run python backend/test_integration_complete.py

# Interactive UI test
# Open: http://localhost:8000/test_narrative_state_ui.html
```

## Frontend Usage

```javascript
// Initialize
await window.StateManager.initialize();

// Update trust/suspicion
await window.StateManager.incrementTrust(10);
await window.StateManager.incrementSuspicion(5);

// Track progress
await window.StateManager.addPuzzleSolved('puzzle_id');
await window.StateManager.addFileDiscovered('file_path');

// Check unlocks
window.StateManager.isFileUnlocked('~/archive/.witness/hello.txt');
window.StateManager.isPuzzleSolved('tutorial_complete');

// Trigger reset
await window.StateManager.resetIteration('MANUAL_RESET');

// Subscribe to changes
window.StateManager.subscribe((state) => {
    console.log('State updated:', state);
});
```

## API Endpoints

```bash
# Initialize
POST /api/narrative/state/init

# Update
POST /api/narrative/state/update

# Reset
POST /api/narrative/state/reset

# Export
GET /api/narrative/state/export

# Import
POST /api/narrative/state/import

# LLM Context
GET /api/narrative/state/llm-context
```

## Story Triggers

| Trust | Effect |
|-------|--------|
| 0 | Start |
| 20 | Graveyard location shared |
| 40 | Graveyard access unlocked |
| 60 | Letters from past unlocked |
| 80 | Source template revealed |
| 90 | Network collapse begins |

## Files Created

**Code**: 14 files (~1,100 lines)
**Docs**: 6 comprehensive guides

## Documentation

- **Quick Start**: `QUICKSTART_NARRATIVE_STATE.md`
- **Testing**: `NARRATIVE_STATE_TESTING.md`
- **Demo**: `PHASE_02_FINAL_DEMO.md`
- **Summary**: `PHASE_02_SUMMARY.md`

## Status

✅ **COMPLETE** - All tests passing, production ready
