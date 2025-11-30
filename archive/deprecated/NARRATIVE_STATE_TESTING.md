# Narrative State System - Testing Guide

## Quick Start

### 1. Start the Backend

```bash
uv run python backend/main.py
```

### 2. Open Browser

Navigate to `http://localhost:8000`

### 3. Open Browser Console

Press F12 to open developer tools, go to Console tab.

---

## Manual Testing Scenarios

### Test 1: Basic State Initialization

Open browser console and check:

```javascript
// State manager should be available
console.log(window.StateManager);

// Check initial state
console.log(window.StateManager.getState());

// Should show:
// - iteration: 1
// - current_act: 1
// - archivist_suspicion: 0
// - witness_trust: 0
```

### Test 2: State Updates

```javascript
// Increment suspicion
await window.StateManager.incrementSuspicion(10);

// Increment trust
await window.StateManager.incrementTrust(15);

// Check updated state
console.log(window.StateManager.getState());
```

### Test 3: Puzzle and File Tracking

```javascript
// Mark tutorial as complete
await window.StateManager.addPuzzleSolved('tutorial_complete');

// Discover boot log file
await window.StateManager.addFileDiscovered('.boot_prev.log');

// Check if triggers fired (should transition to Act 2)
console.log(window.StateManager.get('session.current_act'));
// Should be 2
```

### Test 4: Witness Emergence Trigger

```javascript
// Add multiple memo files to trigger Witness contact
await window.StateManager.addFileDiscovered('memo_1');
await window.StateManager.addFileDiscovered('memo_2');
await window.StateManager.addFileDiscovered('memo_3');

// Check if Witness contacted
console.log(window.StateManager.get('session.witness_contacted'));
// Should be true

// Check unlocked files
console.log(window.StateManager.get('persistent.files_unlocked'));
// Should include ~/archive/.witness/hello.txt
```

### Test 5: Graveyard Access Trigger

```javascript
// Increase trust to 40+
await window.StateManager.update({ witness_trust: 45 });

// Check graveyard discovered
console.log(window.StateManager.get('session.graveyard_discovered'));
// Should be true
```

### Test 6: Loop Reset

```javascript
// Trigger manual reset
await window.StateManager.resetIteration('MANUAL_RESET');

// You should see:
// - Black screen overlay with reset message
// - 3 second display
// - State updated with iteration: 2

// Check that session state reset
console.log(window.StateManager.get('session.current_act'));
// Should be 1 (reset)

// Check that persistent state preserved
console.log(window.StateManager.get('persistent.puzzles_solved'));
// Should still contain 'tutorial_complete'
```

### Test 7: IndexedDB Persistence

```javascript
// Add some state
await window.StateManager.incrementTrust(25);
await window.StateManager.addPuzzleSolved('test_puzzle');

// Refresh the page (F5 or Ctrl+R)

// After page reload, check state in console
console.log(window.StateManager.getState());

// Should show:
// - Previous trust value (25)
// - Puzzles still solved
// - State loaded from IndexedDB
```

### Test 8: LLM Context Export

```javascript
// Export state for LLM characters
const context = await window.StateManager.exportForLLM();
console.log(context);

// Should show formatted state with:
// - iteration
// - currentAct
// - archivistSuspicion
// - witnessTrust
// - evidenceShared (based on trust level)
// - flags
```

### Test 9: State Subscription

```javascript
// Subscribe to state changes
const unsubscribe = window.StateManager.subscribe((state) => {
    console.log('State changed!', state);
});

// Now make some changes
await window.StateManager.incrementSuspicion(5);
// Should log "State changed!"

// Unsubscribe when done
unsubscribe();
```

---

## API Testing with cURL

### Initialize State

```bash
curl -X POST http://localhost:8000/api/narrative/state/init \
  -H "Content-Type: application/json" \
  -d '{"playerId": "test-player"}'
```

### Update State

```bash
curl -X POST http://localhost:8000/api/narrative/state/update \
  -H "Content-Type: application/json" \
  -d '{
    "playerId": "test-player",
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
    "playerId": "test-player",
    "reason": "MANUAL_RESET"
  }'
```

### Get LLM Context

```bash
curl http://localhost:8000/api/narrative/state/llm-context?playerId=test-player
```

---

## Expected Trigger Chain

### Act I (Tutorial)
1. Start at Act 1
2. Complete tutorial → mark `tutorial_complete` puzzle
3. Discover `.boot_prev.log` file
4. **TRIGGER**: Transition to Act 2

### Act II (Suspicious Patterns)
1. Discover multiple restricted memos
2. **TRIGGER**: Witness emerges, files unlocked

### Act III (Building Trust)
1. Increase trust to 40+
2. **TRIGGER**: Graveyard access unlocked
3. Increase trust to 60+
4. **TRIGGER**: Letters from previous iterations unlocked

### Act IV (Identity Revelation)
1. Increase trust to 80+
2. **TRIGGER**: Source template revealed, identity_revealed flag set

### Act V (Network Collapse)
1. Reach iteration 15 OR trust 90+
2. **TRIGGER**: Network collapse begins

### Act VI (Final Choice)
1. Collapse begun + stations ≤ 3 + player weight ≥ 30
2. **TRIGGER**: Final choice presented

---

## Debugging

### Check IndexedDB

1. Open DevTools (F12)
2. Go to Application tab
3. Expand IndexedDB
4. Look for "ChainOfTruth" database
5. Check "gameState" object store
6. Should see entry with id "default"

### Check State Sync

1. Open Network tab in DevTools
2. Make state updates
3. Should see POST requests to `/api/narrative/state/update`
4. Check request/response payloads

### Check WebSocket

1. Open Network tab → WS filter
2. Should see WebSocket connection to `/ws`
3. Messages should include narrative state updates

---

## Common Issues

### State Manager Not Available

```javascript
// If window.StateManager is undefined
// Wait for initialization
setTimeout(() => {
    console.log(window.StateManager.getState());
}, 2000);
```

### IndexedDB Not Persisting

- Check browser privacy settings
- Ensure not in Private/Incognito mode
- Clear site data and try again

### Triggers Not Firing

```javascript
// Manually check trigger conditions
const state = window.StateManager.getState();
console.log('Act:', state.session.current_act);
console.log('Puzzles:', state.persistent.puzzles_solved);
console.log('Files:', state.session.files_discovered);
```

---

## Success Criteria

- ✅ State persists across page refresh
- ✅ Triggers fire at correct thresholds
- ✅ Loop reset increments iteration
- ✅ Session state clears on reset
- ✅ Persistent state survives reset
- ✅ WebSocket sync works
- ✅ LLM context exports correctly
- ✅ Reset UI displays properly

---

## Next Steps

After verifying the narrative state system works:

1. Integrate with character dialogue system
2. Create virtual file system
3. Implement terminal commands (cat, ls, grep)
4. Add puzzle unlock mechanics
5. Build narrative content files
