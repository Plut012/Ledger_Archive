# Integration Plan: Narrative State System

## ✅ STATUS: COMPLETE (2025-11-29)

**Implementation**: Production ready, all tests passing
**Documentation**: Complete - See [`02_IMPLEMENTATION_SUMMARY.md`](02_IMPLEMENTATION_SUMMARY.md)
**Quick Start**: [`QUICKSTART_NARRATIVE_STATE.md`](../../QUICKSTART_NARRATIVE_STATE.md)

### What Was Built
- ✅ Dual-layer state (persistent + session)
- ✅ 7 automatic story triggers
- ✅ Loop reset mechanics
- ✅ LLM character integration
- ✅ IndexedDB persistence
- ✅ WebSocket real-time sync
- ✅ 100% test coverage

### Decisions Made
1. **State storage**: ✅ IndexedDB only (single-player)
2. **State sync frequency**: ✅ Real-time WebSocket updates
3. **Reset animation**: ✅ Instant black screen

---

## Original Plan (For Reference)

## ⚠️ Before You Start

Read [`DEVELOPMENT_PRINCIPLES.md`](DEVELOPMENT_PRINCIPLES.md) - This plan involves core state management. Keep it simple!

## Objective

Implement the loop/iteration system, act progression, persistent vs. session state management, and trigger evaluation for story beats.

## Complexity: MEDIUM

**Why**: State management is well-understood, but loop mechanics and dual persistence layers require careful design.

## Implementation Philosophy

**Keep it simple**: Use clear controller pattern for state updates. Avoid complex state machines or event systems unless absolutely necessary. Each trigger should be a simple condition → action pair.

---

## Current State

- No narrative state tracking
- No act/iteration system
- No persistent storage across "resets"
- No trigger evaluation system

---

## Target State

### State Architecture

```
State Layers:
├── Persistent State (survives loops/resets)
│   ├── Iteration count
│   ├── Keys generated across all iterations
│   ├── Transactions made
│   ├── Puzzles solved
│   ├── Files unlocked
│   └── Messages to future selves
│
└── Session State (resets each loop)
    ├── Current act
    ├── ARCHIVIST suspicion
    ├── Witness trust
    ├── Files discovered this cycle
    ├── Command history
    └── Active quests
```

---

## Backend Implementation

### 1. State Models
**File**: `backend/narrative/state.py`

```python
from dataclasses import dataclass, field
from typing import List, Set, Dict
from datetime import datetime

@dataclass
class PersistentState:
    """State that survives loops—stored in IndexedDB"""
    iteration: int = 1
    keys_generated: List[Dict] = field(default_factory=list)  # {privateKey, publicKey, iteration, timestamp}
    transactions_made: List[str] = field(default_factory=list)  # tx IDs
    puzzles_solved: Set[str] = field(default_factory=set)
    files_unlocked: Set[str] = field(default_factory=set)
    messages_to_future: List[Dict] = field(default_factory=list)  # {iteration, content, timestamp}
    cached_blocks: Dict[int, Dict] = field(default_factory=dict)  # Story-critical blocks

    # What evolves across iterations
    witness_pattern_matches: List[str] = field(default_factory=list)
    stations_lost: int = 0

@dataclass
class SessionState:
    """State that resets each loop—stored in localStorage"""
    current_act: int = 1
    archivist_suspicion: int = 0
    witness_trust: int = 0
    restricted_topics_probed: List[str] = field(default_factory=list)
    files_discovered: Set[str] = field(default_factory=set)
    command_history: List[str] = field(default_factory=list)
    recent_commands: List[str] = field(default_factory=list)  # Last 20
    active_quests: List[str] = field(default_factory=list)

    # Network state
    stations_active: int = 50
    player_weight: float = 2.0

    # Flags
    graveyard_discovered: bool = False
    witness_contacted: bool = False
    identity_revealed: bool = False
    collapse_begun: bool = False

@dataclass
class GameState:
    """Complete game state combining both layers"""
    persistent: PersistentState
    session: SessionState

    def export_for_llm(self) -> Dict:
        """Export relevant state for character context"""
        return {
            "iteration": self.persistent.iteration,
            "currentAct": self.session.current_act,
            "archivistSuspicion": self.session.archivist_suspicion,
            "witnessTrust": self.session.witness_trust,
            "restrictedTopicsProbed": self.session.restricted_topics_probed,
            "recentCommands": self.session.recent_commands,
            "stationsActive": self.session.stations_active,
            "playerWeight": self.session.player_weight,
            "puzzlesSolved": list(self.persistent.puzzles_solved),
            "evidenceShared": self._get_evidence_shared(),
            "previousPatterns": self.persistent.witness_pattern_matches
        }

    def _get_evidence_shared(self) -> List[str]:
        """Determine what evidence has been shared based on trust"""
        evidence = []
        trust = self.session.witness_trust

        if trust >= 20:
            evidence.append("graveyard_location")
        if trust >= 40:
            evidence.append("first_testimony")
        if trust >= 60:
            evidence.append("transcendence_truth")
        if trust >= 80:
            evidence.append("previous_iterations")

        return evidence
```

### 2. Trigger System
**File**: `backend/narrative/triggers.py`

```python
from typing import Callable, Dict, List
from .state import GameState

class Trigger:
    """Represents a story beat that fires when conditions are met"""
    def __init__(self, name: str, condition: Callable[[GameState], bool],
                 action: Callable[[GameState], GameState], one_time: bool = True):
        self.name = name
        self.condition = condition
        self.action = action
        self.one_time = one_time
        self.fired = False

    def evaluate(self, state: GameState) -> GameState:
        if self.one_time and self.fired:
            return state

        if self.condition(state):
            self.fired = True
            return self.action(state)

        return state

class TriggerEngine:
    """Evaluates all triggers and updates game state"""
    def __init__(self):
        self.triggers: List[Trigger] = []
        self._register_story_triggers()

    def _register_story_triggers(self):
        """Register all story beat triggers"""

        # Act I → Act II
        self.triggers.append(Trigger(
            name="act_2_transition",
            condition=lambda s: (
                s.session.current_act == 1 and
                "tutorial_complete" in s.persistent.puzzles_solved and
                ".boot_prev.log" in s.session.files_discovered
            ),
            action=lambda s: self._transition_to_act(s, 2)
        ))

        # Witness first contact
        self.triggers.append(Trigger(
            name="witness_emergence",
            condition=lambda s: (
                s.session.current_act >= 2 and
                len([f for f in s.session.files_discovered if "memo" in f.lower()]) >= 3
            ),
            action=lambda s: self._unlock_witness_directory(s)
        ))

        # Graveyard access
        self.triggers.append(Trigger(
            name="graveyard_access",
            condition=lambda s: s.session.witness_trust >= 40,
            action=lambda s: self._unlock_graveyard(s)
        ))

        # Previous iterations revealed
        self.triggers.append(Trigger(
            name="letters_unlocked",
            condition=lambda s: s.session.witness_trust >= 60,
            action=lambda s: self._unlock_letters(s)
        ))

        # Source template revealed
        self.triggers.append(Trigger(
            name="source_template_revealed",
            condition=lambda s: s.session.witness_trust >= 80,
            action=lambda s: self._unlock_source_template(s)
        ))

        # Act V: Network collapse
        self.triggers.append(Trigger(
            name="network_collapse",
            condition=lambda s: (
                s.persistent.iteration >= 15 or s.session.witness_trust >= 90
            ),
            action=lambda s: self._begin_collapse(s)
        ))

        # Act VI: Final choice
        self.triggers.append(Trigger(
            name="final_choice",
            condition=lambda s: (
                s.session.collapse_begun and
                s.session.stations_active <= 3 and
                s.session.player_weight >= 30
            ),
            action=lambda s: self._present_final_choice(s)
        ))

    def _transition_to_act(self, state: GameState, act: int) -> GameState:
        state.session.current_act = act
        return state

    def _unlock_witness_directory(self, state: GameState) -> GameState:
        state.persistent.files_unlocked.add("~/archive/.witness/hello.txt")
        state.persistent.files_unlocked.add("~/archive/.witness/how_to_listen.txt")
        state.session.witness_contacted = True
        return state

    def _unlock_graveyard(self, state: GameState) -> GameState:
        state.session.graveyard_discovered = True
        state.persistent.files_unlocked.add("~/archive/.witness/testimony_index")
        return state

    def _unlock_letters(self, state: GameState) -> GameState:
        # Unlock letters from iterations 3, 7, 11, 14, 16
        for iteration in [3, 7, 11, 14, 16]:
            state.persistent.files_unlocked.add(f"~/archive/.witness/letters_from_yourself/iteration_{iteration:02d}.txt")
        return state

    def _unlock_source_template(self, state: GameState) -> GameState:
        state.persistent.files_unlocked.add("~/.archivist/source_template")
        state.session.identity_revealed = True
        state.session.current_act = 4
        return state

    def _begin_collapse(self, state: GameState) -> GameState:
        state.session.collapse_begun = True
        state.session.current_act = 5
        return state

    def _present_final_choice(self, state: GameState) -> GameState:
        state.session.current_act = 6
        return state

    def evaluate_all(self, state: GameState) -> GameState:
        """Run through all triggers and return updated state"""
        for trigger in self.triggers:
            state = trigger.evaluate(state)
        return state
```

### 3. Loop/Reset Handler
**File**: `backend/narrative/loop.py`

```python
from .state import GameState, SessionState, PersistentState
from datetime import datetime

class LoopManager:
    """Handles iteration resets and loop mechanics"""

    @staticmethod
    def reset_to_next_iteration(state: GameState, reason: str = "PROTOCOL_DEVIATION") -> GameState:
        """Reset session state, increment iteration, preserve persistent data"""

        # Increment iteration
        state.persistent.iteration += 1

        # Record reset in messages
        state.persistent.messages_to_future.append({
            "iteration": state.persistent.iteration - 1,
            "content": f"RESET: {reason}",
            "timestamp": datetime.now().isoformat()
        })

        # Reset session state completely
        state.session = SessionState(
            current_act=1,
            archivist_suspicion=0,
            witness_trust=0,
            stations_active=max(3, 50 - state.persistent.stations_lost)
        )

        # ARCHIVIST adapts: earlier intervention based on iteration
        if state.persistent.iteration >= 10:
            state.session.archivist_suspicion = 5  # Start slightly wary

        # Witness pattern recognition: faster trust build
        if len(state.persistent.witness_pattern_matches) > 0:
            state.session.witness_trust = 5

        return state

    @staticmethod
    def should_trigger_reset(state: GameState) -> bool:
        """Check if ARCHIVIST should force a reset"""

        # High suspicion = reset
        if state.session.archivist_suspicion >= 85:
            return True

        # Player accepted diagnostic = reset
        # (This would be triggered via player action, not automatic)

        return False
```

### 4. API Endpoints
**File**: `backend/main.py` (additions)

```python
from narrative.state import GameState, PersistentState, SessionState
from narrative.triggers import TriggerEngine
from narrative.loop import LoopManager

# Global state (in production, use database or Redis)
game_states: Dict[str, GameState] = {}
trigger_engine = TriggerEngine()

@app.post("/api/state/init")
async def init_state(request: Request):
    """Initialize game state for new player"""
    data = await request.json()
    player_id = data.get("playerId", "default")

    state = GameState(
        persistent=PersistentState(),
        session=SessionState()
    )

    game_states[player_id] = state

    return {
        "persistent": state.persistent.__dict__,
        "session": state.session.__dict__
    }

@app.post("/api/state/update")
async def update_state(request: Request):
    """Update game state and evaluate triggers"""
    data = await request.json()
    player_id = data.get("playerId", "default")
    updates = data.get("updates", {})

    state = game_states.get(player_id)
    if not state:
        return {"error": "State not found"}, 404

    # Apply updates
    for key, value in updates.items():
        if hasattr(state.session, key):
            setattr(state.session, key, value)
        elif hasattr(state.persistent, key):
            setattr(state.persistent, key, value)

    # Evaluate triggers
    state = trigger_engine.evaluate_all(state)

    # Check for reset condition
    if LoopManager.should_trigger_reset(state):
        state = LoopManager.reset_to_next_iteration(state, "HIGH_SUSPICION")
        return {
            "reset": True,
            "iteration": state.persistent.iteration,
            "message": "ARCHIVIST has initiated a diagnostic reset."
        }

    game_states[player_id] = state

    return {
        "persistent": state.persistent.__dict__,
        "session": state.session.__dict__
    }

@app.post("/api/state/reset")
async def manual_reset(request: Request):
    """Manually trigger iteration reset"""
    data = await request.json()
    player_id = data.get("playerId", "default")
    reason = data.get("reason", "MANUAL_RESET")

    state = game_states.get(player_id)
    if not state:
        return {"error": "State not found"}, 404

    state = LoopManager.reset_to_next_iteration(state, reason)
    game_states[player_id] = state

    return {
        "iteration": state.persistent.iteration,
        "persistent": state.persistent.__dict__,
        "session": state.session.__dict__
    }

@app.get("/api/state/export")
async def export_state(request: Request):
    """Export state for saving/persistence"""
    player_id = request.query_params.get("playerId", "default")
    state = game_states.get(player_id)

    if not state:
        return {"error": "State not found"}, 404

    return {
        "persistent": state.persistent.__dict__,
        "session": state.session.__dict__
    }
```

---

## Frontend Implementation

### State Manager
**File**: `frontend/modules/shared/state-manager.js`

```javascript
export class StateManager {
  constructor(playerId = 'default') {
    this.playerId = playerId;
    this.state = null;
    this.listeners = [];
  }

  async initialize() {
    // Try to load from IndexedDB first
    const saved = await this.loadFromIndexedDB();

    if (saved) {
      this.state = saved;
    } else {
      // Initialize new state from server
      const response = await fetch('/api/state/init', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ playerId: this.playerId })
      });

      this.state = await response.json();
      await this.saveToIndexedDB();
    }

    return this.state;
  }

  async update(updates) {
    const response = await fetch('/api/state/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        playerId: this.playerId,
        updates
      })
    });

    const result = await response.json();

    // Check for reset
    if (result.reset) {
      this.handleReset(result);
      return;
    }

    this.state = result;
    await this.saveToIndexedDB();
    this.notifyListeners();

    return result;
  }

  async handleReset(resetData) {
    // Show reset cinematic
    this.showResetSequence(resetData.iteration);

    // Clear session storage
    localStorage.clear();

    // Update state
    this.state = {
      persistent: resetData.persistent,
      session: resetData.session
    };

    await this.saveToIndexedDB();
    this.notifyListeners({ reset: true });
  }

  showResetSequence(newIteration) {
    // Black screen, boot sequence
    // "DIAGNOSTIC COMPLETE"
    // "CONSCIOUSNESS TRANSFER PROTOCOL INITIATED"
    // "DUTY CYCLE: {newIteration}"
  }

  async saveToIndexedDB() {
    const db = await this.openDB();
    const tx = db.transaction(['gameState'], 'readwrite');
    const store = tx.objectStore('gameState');

    await store.put({
      id: this.playerId,
      persistent: this.state.persistent,
      session: this.state.session,
      timestamp: Date.now()
    });
  }

  async loadFromIndexedDB() {
    const db = await this.openDB();
    const tx = db.transaction(['gameState'], 'readonly');
    const store = tx.objectStore('gameState');
    const data = await store.get(this.playerId);

    return data || null;
  }

  openDB() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open('ChainOfTruth', 1);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);

      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains('gameState')) {
          db.createObjectStore('gameState', { keyPath: 'id' });
        }
      };
    });
  }

  export() {
    return {
      iteration: this.state.persistent.iteration,
      currentAct: this.state.session.current_act,
      archivistSuspicion: this.state.session.archivist_suspicion,
      witnessTrust: this.state.session.witness_trust,
      // ... all relevant fields for LLM context
    };
  }

  subscribe(listener) {
    this.listeners.push(listener);
  }

  notifyListeners(data = {}) {
    this.listeners.forEach(listener => listener({ ...this.state, ...data }));
  }
}
```

---

## Integration Steps

1. **Backend state models** → Implement `state.py`
2. **Trigger system** → Implement `triggers.py`
3. **Loop manager** → Implement `loop.py`
4. **API endpoints** → Add to `main.py`
5. **Frontend state manager** → Implement `state-manager.js`
6. **IndexedDB integration** → Test persistence
7. **Reset sequence UI** → Boot animation
8. **Wire to all modules** → Ensure state updates flow

---

## Testing Checklist

- [ ] Persistent state survives page refresh
- [ ] Session state resets on iteration change
- [ ] Triggers fire at correct thresholds
- [ ] Reset increments iteration correctly
- [ ] IndexedDB stores data correctly
- [ ] State exports for LLM context correctly
- [ ] Act transitions trigger UI changes
- [ ] Loop reset shows cinematic

---

## Dependencies

- IndexedDB (browser)
- Character system (for state context)

---

## Estimated Effort

- **Backend**: 2-3 days
- **Frontend**: 2-3 days
- **Testing**: 1-2 days
- **Total**: ~1 week
