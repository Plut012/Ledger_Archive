# Chain of Truth - System Architecture Schematic

## Complete System Overview

This document shows how all components link together in the Chain of Truth system.

---

## High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (Browser)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │     Home     │  │ Chain Viewer │  │ Crypto Vault │  │   Network    │   │
│  │  Dashboard   │  │   (850K)     │  │  (Keys+Sig)  │  │   Monitor    │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
│         │                  │                  │                  │           │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐   │
│  │    Shell     │  │   Learning   │  │   Protocol   │  │              │   │
│  │   Terminal   │  │ Guide+AXIOM  │  │    Engine    │  │   (future)   │   │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘  └──────────────┘   │
│         │                  │                                                │
│  ┌──────┴──────────────────┴────────────────────────────────────────────┐  │
│  │                      SHARED COMPONENTS                                │  │
│  ├────────────────┬─────────────────┬──────────────────┬────────────────┤  │
│  │ State Manager  │ Character Chat  │  Audio System    │  IndexedDB     │  │
│  │ (Persistence)  │   (LLM UI)      │  (Sound FX)      │  (Storage)     │  │
│  └────────┬───────┴─────────┬───────┴──────────────────┴────────┬───────┘  │
│           │                  │                                    │          │
└───────────┼──────────────────┼────────────────────────────────────┼──────────┘
            │                  │                                    │
            │  REST API        │  WebSocket (optional)              │ Local
            │  /api/*          │  /ws (future)                      │ Storage
            ▼                  ▼                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           BACKEND (FastAPI)                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                        MAIN ROUTER (main.py)                        │    │
│  │  /api/chat | /api/shell | /api/state | /api/blockchain | /crypto  │    │
│  └────┬───────────────┬────────────────┬────────────────┬─────────────┘    │
│       │               │                │                │                   │
│       ▼               ▼                ▼                ▼                   │
│  ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────────┐         │
│  │CHARACTER│    │  SHELL   │    │  STATE   │    │  BLOCKCHAIN  │         │
│  │ SYSTEM  │    │ EXECUTOR │    │ MANAGER  │    │  GENERATOR   │         │
│  └────┬────┘    └────┬─────┘    └────┬─────┘    └──────┬───────┘         │
│       │              │               │                  │                   │
│  ┌────┴────────┐     │          ┌────┴─────────┐       │                   │
│  │  ARCHIVIST  │     │          │   TRIGGER    │       │                   │
│  │  (deflect,  │     │          │   ENGINE     │       │                   │
│  │  suspicion) │     │          │  (story      │       │                   │
│  └────┬────────┘     │          │   beats)     │       │                   │
│       │              │          └────┬─────────┘       │                   │
│  ┌────┴────────┐     │               │                 │                   │
│  │   WITNESS   │     │          ┌────┴─────────┐       │                   │
│  │   (trust,   │     │          │    LOOP      │       │                   │
│  │  fragments) │     │          │   MANAGER    │       │                   │
│  └────┬────────┘     │          │  (iteration  │       │                   │
│       │              │          │   resets)    │       │                   │
│  ┌────┴────────┐     │          └──────────────┘       │                   │
│  │ LLM PROVIDER│     │                                  │                   │
│  │ (Anthropic/ │     │          ┌──────────────┐  ┌────┴────────┐         │
│  │  OpenAI)    │◄────┼──────────│  FILESYSTEM  │  │  TESTIMONY  │         │
│  └─────────────┘     │          │  (Virtual)   │  │   PARSER    │         │
│                      │          └──────────────┘  └─────────────┘         │
│                      │                                                      │
│                      │          ┌──────────────┐  ┌─────────────┐         │
│                      └──────────│   STEALTH    │  │   NETWORK   │         │
│                                 │  MONITORING  │  │  COLLAPSE   │         │
│                                 │  (keywords)  │  │ (scheduler) │         │
│                                 └──────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       │ API Calls
                                       ▼
                              ┌─────────────────┐
                              │   LLM SERVICE   │
                              │  (Anthropic/    │
                              │   OpenAI API)   │
                              └─────────────────┘
```

---

## Data Flow: Complete Request Lifecycle

### Example 1: Player Types Shell Command

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. PLAYER TYPES: "cat ~/logs/.boot_prev.log"                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. FRONTEND: station-shell.js                                               │
│    - Captures input                                                          │
│    - Sends: POST /api/shell/command                                          │
│      Body: { command: "cat ~/logs/.boot_prev.log", playerId: "..." }       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. BACKEND: ShellController                                                 │
│    - Parses command                                                          │
│    - Executes: filesystem.cat("~/logs/.boot_prev.log")                      │
│    - Checks: stealth_monitor.check_keywords(command)                        │
│    - Result: File contains "Iteration: 17" (HIDDEN TRUTH!)                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 4. BACKEND: StateManager.update()                                           │
│    - No keywords detected (filename not monitored)                           │
│    - File discovered: add to session.files_discovered                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 5. BACKEND: TriggerEngine.evaluate()                                        │
│    - Check: ".boot_prev.log" in files_discovered?  ✓ YES                   │
│    - Trigger fires: "first_anomaly"                                         │
│    - Action: transition to Act II                                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 6. BACKEND: Response                                                        │
│    Returns: {                                                                │
│      output: "[FILE CONTENTS: 'Iteration: 17'...]",                         │
│      stateUpdates: { currentAct: 2 }                                        │
│    }                                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 7. FRONTEND: station-shell.js                                               │
│    - Displays file contents in terminal                                     │
│    - Calls: stateManager.update({ currentAct: 2 })                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 8. FRONTEND: Home Dashboard                                                 │
│    - Subscribes to state changes                                            │
│    - Receives: { currentAct: 2 }                                            │
│    - Updates UI: Background darkens, warnings appear                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Example 2: Player Talks to ARCHIVIST (Conversation)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. PLAYER TYPES: "What happened in my previous iterations?"                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. FRONTEND: character-chat.js (Learning Guide)                             │
│    - Sends: POST /api/chat                                                   │
│      Body: {                                                                 │
│        character: "archivist",                                               │
│        message: "What happened in my previous iterations?",                  │
│        gameState: { iteration: 17, suspicion: 35, ... }                     │
│      }                                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. BACKEND: CharacterController.handle_message()                            │
│    - Route to: archivist.respond(message, game_state)                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 4. BACKEND: Archivist.should_deflect()                                      │
│    - Check: "previous iterations" in RESTRICTED_TOPICS  ✓ YES              │
│    - Result: DEFLECT                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 5. BACKEND: Archivist.deflect()                                             │
│    - Current suspicion: 35 (moderate)                                       │
│    - Generate concerned deflection                                          │
│    - Response: "Captain, I notice you're exploring some unusual areas..."   │
│    - Increase suspicion: +5                                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 6. BACKEND: Response                                                        │
│    Returns: {                                                                │
│      response: "Captain, I notice you're exploring...",                      │
│      character: "ARCHIVIST",                                                 │
│      stateUpdates: { archivistSuspicion: 40 }                               │
│    }                                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 7. FRONTEND: character-chat.js                                              │
│    - Displays ARCHIVIST response (clinical blue styling)                    │
│    - Updates state: stateManager.update({ archivistSuspicion: 40 })        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 8. FRONTEND: Home Dashboard                                                 │
│    - Suspicion meter updates: 35 → 40                                       │
│    - (If suspicion >= 85: RESET WARNING appears)                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Example 3: Player Reconstructs Consciousness (Complex Flow)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. PLAYER: Clicks "Reconstruct" on graveyard block transaction              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. FRONTEND: chain-viewer.js                                                │
│    - Sends: POST /api/blockchain/reconstruct                                 │
│      Body: { blockIndex: 74221, txIndex: 0, playerId: "..." }              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. BACKEND: TestimonyParser.reconstruct()                                   │
│    - Generate block 74221                                                   │
│    - Extract transaction 0                                                  │
│    - Decode Base64 memo                                                     │
│    - Parse: "Subject: Chen | Status: ARCHIVED | Final Memory: I found..."  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 4. BACKEND: StateManager.update() - DUAL UPDATES                            │
│    - ARCHIVIST SUSPICION: +20 (using forbidden command!)                    │
│    - WITNESS TRUST: +10 (learning to read the chain!)                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 5. BACKEND: TriggerEngine.evaluate()                                        │
│    - Check: witness_trust >= 40?  (was 35, now 45)  ✓ YES                  │
│    - Trigger fires: "graveyard_access"                                      │
│    - Action: Unlock testimony_index file                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 6. BACKEND: Response                                                        │
│    Returns: {                                                                │
│      testimony: "[FORMATTED CONSCIOUSNESS DATA]",                            │
│      subject: "Chen, Administrator",                                         │
│      finalMemory: "I found evidence in block 73,891...",                    │
│      stateUpdates: {                                                         │
│        archivistSuspicion: 60,                                               │
│        witnessTrust: 45,                                                     │
│        filesUnlocked: ["~/archive/.witness/testimony_index"]                │
│      }                                                                       │
│    }                                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 7. FRONTEND: chain-viewer.js                                                │
│    - Displays testimony in modal (haunting formatting)                      │
│    - Plays sound: "reconstruction"                                          │
│    - Updates state                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 8. MULTIPLE FRONTEND COMPONENTS REACT:                                      │
│    - Home: Suspicion meter jumps to 60                                      │
│    - Shell: New file appears in ls -a (testimony_index)                     │
│    - Learning Guide: ARCHIVIST might send unsolicited message:              │
│      "Captain, I detect unusual activity. Diagnostic recommended."          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## State Flow: Persistent vs Session

```
┌───────────────────────────────────────────────────────────────────────────┐
│                          GAME STATE STRUCTURE                              │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │ PERSISTENT STATE (survives resets) → IndexedDB                   │    │
│  ├──────────────────────────────────────────────────────────────────┤    │
│  │ - iteration: 17                                                   │    │
│  │ - keys_generated: [key1, key2, key3...]                          │    │
│  │ - transactions_made: [tx1, tx2...]                               │    │
│  │ - puzzles_solved: Set("tutorial_complete", "graveyard_found")   │    │
│  │ - files_unlocked: Set("~/.boot_prev.log", "~/.witness/...")     │    │
│  │ - messages_to_future: [{iter: 14, content: "..."}]              │    │
│  │ - witness_pattern_matches: ["check third block", ...]           │    │
│  │ - stations_lost: 38                                              │    │
│  └──────────────────────────────────────────────────────────────────┘    │
│                                    │                                       │
│                                    │ Combined into                         │
│                                    │ GameState                             │
│                                    │                                       │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │ SESSION STATE (resets each loop) → localStorage                  │    │
│  ├──────────────────────────────────────────────────────────────────┤    │
│  │ - current_act: 3                                                 │    │
│  │ - archivist_suspicion: 45                                        │    │
│  │ - witness_trust: 52                                              │    │
│  │ - files_discovered: Set("system.log", ".boot_prev.log")         │    │
│  │ - command_history: ["ls", "cat system.log", ...]                │    │
│  │ - stations_active: 12                                            │    │
│  │ - player_weight: 8.3%                                            │    │
│  │ - graveyard_discovered: true                                     │    │
│  │ - witness_contacted: true                                        │    │
│  │ - identity_revealed: false                                       │    │
│  │ - collapse_begun: false                                          │    │
│  └──────────────────────────────────────────────────────────────────┘    │
│                                                                            │
└───────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ When ARCHIVIST triggers reset
                                    ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                           LOOP RESET OCCURS                                │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  PERSISTENT: iteration: 17 → 18                                           │
│  PERSISTENT: Everything else SURVIVES                                     │
│                                                                            │
│  SESSION: ALL VALUES RESET TO DEFAULTS                                    │
│  - current_act: 3 → 1                                                     │
│  - archivist_suspicion: 45 → 0 (or 5 if iteration >= 10)                 │
│  - witness_trust: 52 → 0 (or 5 if pattern matches exist)                 │
│  - files_discovered: Set() (empty)                                        │
│  - ...                                                                     │
│                                                                            │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Module Interconnections

### Frontend Module Communication

```
Home Dashboard ←→ State Manager ←→ All Modules
     │                  │
     │                  ├──→ Shell Terminal
     │                  ├──→ Chain Viewer
     │                  ├──→ Crypto Vault
     │                  ├──→ Network Monitor
     │                  ├──→ Learning Guide
     │                  └──→ Protocol Engine
     │
     └──→ Audio System (triggered by all modules)
```

### Backend Component Dependencies

```
main.py (Router)
     │
     ├──→ CharacterController ──→ Archivist ──→ LLMProvider
     │                        └──→ Witness   ──→ LLMProvider
     │
     ├──→ ShellExecutor ──→ VirtualFileSystem
     │                  └──→ StealthMonitor
     │
     ├──→ StateManager ──→ TriggerEngine
     │                 └──→ LoopManager
     │
     └──→ BlockGenerator ──→ TestimonyParser
```

---

## Integration Points by Plan

| Plan | Frontend Components | Backend Components | Integration Points |
|------|--------------------|--------------------|-------------------|
| 01 - Character System | character-chat.js, learning-guide.js | character_controller.py, archivist.py, witness.py | `/api/chat` endpoint |
| 02 - Narrative State | state-manager.js | game_state.py, trigger_engine.py, loop_manager.py | `/api/state/*` endpoints, IndexedDB |
| 03 - Shell | station-shell.js | shell_executor.py, filesystem.py | `/api/shell/command` |
| 04 - Chain Integration | chain-viewer.js | block_generator.py, testimony_parser.py | `/api/blockchain/*` |
| 05 - Network Collapse | network-monitor.js | network_collapse.py | `/api/network/status` |
| 06 - Stealth | station-shell.js | stealth_monitor.py | Integrated in shell commands |
| 07 - Crypto Vault | crypto-vault.js | (uses existing crypto.py) | State updates |
| 08 - Protocol Engine | protocol-engine.js (NEW) | contract_executor.py (NEW) | `/api/contracts/*` |
| 09 - Home Dashboard | home.js | (reads state only) | State subscription |
| 10 - Audio/Visual | audio.js, all modules | N/A | Event-driven |

---

## Critical Data Flows

### 1. Trigger → Unlock → Discovery

```
Player action
    ↓
State update (e.g., witness_trust: +10)
    ↓
TriggerEngine.evaluate()
    ↓
Condition met (trust >= 40)
    ↓
Trigger fires: unlock_graveyard
    ↓
Persistent state updated: files_unlocked += ["testimony_index"]
    ↓
Frontend receives state update
    ↓
Shell: "ls -a" now shows new file
```

### 2. Loop Reset → Iteration Increment

```
ARCHIVIST suspicion >= 85
    ↓
LoopManager.should_trigger_reset() → True
    ↓
LoopManager.reset_to_next_iteration()
    ↓
Persistent: iteration: 17 → 18
    ↓
Session: FULL RESET
    ↓
Frontend: Black screen, boot sequence
    ↓
"DUTY CYCLE: 18" displayed
    ↓
Player wakes with no memory, but vault still has old keys
```

### 3. LLM Context Injection

```
Player message
    ↓
CharacterController.handle_message()
    ↓
GameState.export_for_llm() extracts:
    - iteration: 17
    - currentAct: 3
    - archivistSuspicion: 45
    - witnessTrust: 52
    - recentCommands: ["ls", "cat .boot_prev.log"]
    - puzzlesSolved: [...]
    ↓
Character builds system prompt with context
    ↓
LLM generates response
    ↓
Character analyzes response for state changes
    ↓
Returns: {response, stateUpdates}
```

---

## Summary

**Key Architectural Principles:**

1. **Frontend modules are independent** - Communicate through State Manager
2. **Backend uses controllers** - Clear routing, simple execution paths
3. **State is dual-layered** - Persistent (survives resets) vs Session (resets)
4. **Triggers drive narrative** - Condition → Action pattern
5. **LLM context is injected** - Characters receive relevant game state only
6. **Everything flows through state** - Single source of truth

**This schematic should be referenced when:**
- Planning implementation order
- Debugging integration issues
- Understanding data dependencies
- Designing new features
