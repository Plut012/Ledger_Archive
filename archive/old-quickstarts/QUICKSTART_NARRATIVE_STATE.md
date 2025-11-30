# Narrative State System - Quick Start Guide

## What is the Narrative State System?

The narrative state system manages the loop-based story progression, tracking player progress across "consciousness transfers" (iteration resets) while maintaining persistent data.

### Key Concepts

- **Persistent State**: Data that survives loops (iteration count, puzzles solved, files unlocked)
- **Session State**: Data that resets each loop (current act, suspicion, trust, flags)
- **Triggers**: Story beats that fire when conditions are met
- **Loop Resets**: Consciousness transfers that reset session state but preserve progress

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│               DUAL-LAYER STATE                      │
├─────────────────────────────────────────────────────┤
│  Persistent (survives loops)                        │
│  - Iteration count                                  │
│  - Puzzles solved                                   │
│  - Files unlocked                                   │
│  - Messages to future selves                        │
│                                                     │
│  Session (resets each loop)                        │
│  - Current act                                      │
│  - ARCHIVIST suspicion                             │
│  - WITNESS trust                                    │
│  - Flags (graveyard, identity, collapse)           │
└─────────────────────────────────────────────────────┘
          │                            │
          │ IndexedDB                  │ In-Memory + API
          ▼                            ▼
┌──────────────────┐         ┌──────────────────┐
│  Browser Storage │         │  Backend Server  │
│  - Persists      │◄──HTTP─►│  - Evaluates     │
│  - Offline OK    │         │  - Triggers      │
└──────────────────┘         └──────────────────┘
```

---

## Quick Setup

### 1. Backend is Already Running

If you've started the server with:

```bash
uv run python backend/main.py
```

The narrative state endpoints are already available!

### 2. Test Backend Functionality

```bash
PYTHONPATH=backend uv run python backend/test_narrative_state.py
```

Expected output:
```
✓ Basic State Creation
✓ State Serialization
✓ Trigger System
✓ Loop Reset System
✓ LLM Context Export
✓ Reset Messages
```

### 3. Test Frontend Integration

Open your browser to `http://localhost:8000` and open the console (F12):

```javascript
// Check state manager is available
console.log(window.StateManager);

// View current state
console.log(window.StateManager.getState());
```

---

## Common Use Cases

### Use Case 1: Update Player Trust

```javascript
// Increment WITNESS trust by 10
await window.StateManager.incrementTrust(10);

// Check if this triggered any story beats
const state = window.StateManager.getState();
console.log('Current act:', state.session.current_act);
console.log('Files unlocked:', state.persistent.files_unlocked);
```

### Use Case 2: Mark Puzzle Solved

```javascript
// Mark a puzzle as complete
await window.StateManager.addPuzzleSolved('first_key_generated');

// Check if puzzle was saved
const isSolved = window.StateManager.isPuzzleSolved('first_key_generated');
console.log('Puzzle solved:', isSolved);
```

### Use Case 3: Trigger a Loop Reset

```javascript
// Manual reset (player accepts diagnostic)
await window.StateManager.resetIteration('MANUAL_RESET');

// After 3 seconds, check new state
setTimeout(() => {
    const state = window.StateManager.getState();
    console.log('New iteration:', state.persistent.iteration);
    console.log('Act (should be 1):', state.session.current_act);
    console.log('Puzzles (preserved):', state.persistent.puzzles_solved);
}, 4000);
```

### Use Case 4: Check Unlocked Files

```javascript
// Check if a file is unlocked by story progression
const unlocked = window.StateManager.isFileUnlocked('~/archive/.witness/hello.txt');

if (unlocked) {
    console.log('File is accessible!');
} else {
    console.log('File locked - build more trust');
}
```

### Use Case 5: Subscribe to State Changes

```javascript
// Listen for state changes
const unsubscribe = window.StateManager.subscribe((newState) => {
    console.log('State updated!');

    if (newState.reset) {
        console.log('Loop reset occurred!');
    }

    if (newState.session.witness_contacted) {
        console.log('WITNESS has emerged!');
    }
});

// Later: unsubscribe when done
unsubscribe();
```

---

## Story Triggers

The system includes 7 automatic triggers:

### 1. Act II Transition
**Condition**: Tutorial complete + boot log discovered
**Effect**: Transition to Act 2

```javascript
await window.StateManager.addPuzzleSolved('tutorial_complete');
await window.StateManager.addFileDiscovered('.boot_prev.log');
// Act should now be 2
```

### 2. Witness Emergence
**Condition**: 3+ restricted memos discovered
**Effect**: Witness contact, files unlocked

```javascript
await window.StateManager.addFileDiscovered('memo_1');
await window.StateManager.addFileDiscovered('memo_2');
await window.StateManager.addFileDiscovered('memo_3');
// Witness should now be contacted
```

### 3. Graveyard Access
**Condition**: Trust >= 40
**Effect**: Graveyard discovered

```javascript
await window.StateManager.update({ witness_trust: 45 });
// Graveyard should now be accessible
```

### 4. Letters from Past Iterations
**Condition**: Trust >= 60
**Effect**: Unlock letters from iterations 3, 7, 11, 14, 16

```javascript
await window.StateManager.update({ witness_trust: 65 });
// Letters should now be unlocked
```

### 5. Source Template Revealed
**Condition**: Trust >= 80
**Effect**: Identity revealed, Act 4

```javascript
await window.StateManager.update({ witness_trust: 85 });
// Source template unlocked, identity_revealed = true
```

### 6. Network Collapse
**Condition**: Iteration >= 15 OR Trust >= 90
**Effect**: Collapse begins, Act 5

```javascript
await window.StateManager.update({ witness_trust: 95 });
// Network collapse initiated
```

### 7. Final Choice
**Condition**: Collapse + Stations <= 3 + Weight >= 30
**Effect**: Act 6, final decision

```javascript
await window.StateManager.update({
    stations_active: 3,
    player_weight: 35
});
// Final choice presented
```

---

## API Reference

### State Manager Methods

#### Core Operations
- `initialize()` - Load from IndexedDB or create new state
- `update(updates)` - Update state and evaluate triggers
- `resetIteration(reason)` - Trigger loop reset
- `getState()` - Get current state
- `get(path)` - Get specific value (e.g., 'session.current_act')

#### Helper Methods
- `incrementSuspicion(amount)` - Increase ARCHIVIST suspicion
- `incrementTrust(amount)` - Increase WITNESS trust
- `addPuzzleSolved(puzzleId)` - Mark puzzle complete
- `addFileDiscovered(filePath)` - Record file discovery
- `addCommandToHistory(command)` - Track command usage
- `isFileUnlocked(filePath)` - Check if file is accessible
- `isPuzzleSolved(puzzleId)` - Check if puzzle is solved

#### Advanced
- `exportForLLM()` - Get state formatted for character context
- `subscribe(callback)` - Listen for state changes
- `setupWebSocket(ws)` - Enable real-time sync

---

## Backend API Endpoints

All endpoints are prefixed with `/api/narrative/state/`

### Initialize State
```bash
curl -X POST http://localhost:8000/api/narrative/state/init \
  -H "Content-Type: application/json" \
  -d '{"playerId": "player1"}'
```

### Update State
```bash
curl -X POST http://localhost:8000/api/narrative/state/update \
  -H "Content-Type: application/json" \
  -d '{
    "playerId": "player1",
    "updates": {
      "witness_trust": 50,
      "archivist_suspicion": 20
    }
  }'
```

### Trigger Reset
```bash
curl -X POST http://localhost:8000/api/narrative/state/reset \
  -H "Content-Type: application/json" \
  -d '{
    "playerId": "player1",
    "reason": "MANUAL_RESET"
  }'
```

### Get LLM Context
```bash
curl http://localhost:8000/api/narrative/state/llm-context?playerId=player1
```

---

## Data Persistence

### IndexedDB Storage

The state manager automatically saves to IndexedDB:

```javascript
// State is saved automatically after each update
await window.StateManager.incrementTrust(10);
// Already saved to IndexedDB

// Refresh the page - state is restored
window.location.reload();
// After reload, state is loaded from IndexedDB
```

### Checking IndexedDB

1. Open DevTools (F12)
2. Go to Application tab
3. Expand IndexedDB → ChainOfTruth → gameState
4. See your saved state

### Clearing State

```javascript
// Clear IndexedDB
const db = await window.StateManager.openDB();
const tx = db.transaction(['gameState'], 'readwrite');
await tx.objectStore('gameState').clear();

// Refresh to start fresh
window.location.reload();
```

---

## Integration with LLM Characters

The state system exports context for character responses:

```javascript
// Get context for ARCHIVIST
const context = await window.StateManager.exportForLLM();

// Context includes:
// - iteration
// - currentAct
// - archivistSuspicion
// - witnessTrust
// - puzzlesSolved
// - evidenceShared (based on trust level)
// - flags (graveyard, witness, identity, collapse)
```

Characters can use this to:
- Adjust dialogue based on suspicion level
- Share information based on trust
- Reference player's progress
- React to act transitions

---

## Troubleshooting

### State Manager Not Available

```javascript
// Wait for initialization
setTimeout(() => {
    if (window.StateManager) {
        console.log('Ready!');
    }
}, 2000);
```

### IndexedDB Not Persisting

- Check browser privacy settings
- Disable Private/Incognito mode
- Clear site data and retry

### Triggers Not Firing

```javascript
// Debug trigger conditions
const state = window.StateManager.getState();
console.log('Act:', state.session.current_act);
console.log('Puzzles:', Array.from(state.persistent.puzzles_solved));
console.log('Files:', Array.from(state.session.files_discovered));
console.log('Trust:', state.session.witness_trust);
```

### Server Connection Issues

```javascript
// Check if server is running
fetch('/api/narrative/state/export?playerId=default')
    .then(r => r.json())
    .then(d => console.log('Server OK:', d))
    .catch(e => console.error('Server error:', e));
```

---

## Testing Guide

### Interactive UI Test

Open `test_narrative_state_ui.html` in browser:

```bash
# Start server
uv run python backend/main.py

# Open in browser
open http://localhost:8000/test_narrative_state_ui.html
```

Click through the test buttons to verify:
- State initialization
- Suspicion/trust updates
- Trigger evaluation
- Loop resets
- IndexedDB persistence

### Manual Browser Testing

See [`NARRATIVE_STATE_TESTING.md`](NARRATIVE_STATE_TESTING.md) for detailed test scenarios.

---

## Next Steps

Now that you have the narrative state system working:

1. **Integrate with modules**: Add state tracking to Chain Viewer, Crypto Vault, etc.
2. **Create narrative content**: Write files that unlock based on triggers
3. **Build puzzles**: Design challenges that update state when solved
4. **Character integration**: Use state context in ARCHIVIST/WITNESS responses
5. **UI enhancements**: Show iteration count, act, suspicion/trust meters

---

## Learn More

- **Full specification**: [`docs/integration_plans/02_NARRATIVE_STATE.md`](docs/integration_plans/02_NARRATIVE_STATE.md)
- **Implementation details**: [`docs/integration_plans/02_IMPLEMENTATION_SUMMARY.md`](docs/integration_plans/02_IMPLEMENTATION_SUMMARY.md)
- **Testing guide**: [`NARRATIVE_STATE_TESTING.md`](NARRATIVE_STATE_TESTING.md)

---

*"Each iteration, the same. Each iteration, different. The loop remembers all."*
