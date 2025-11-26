# CHAIN OF TRUTH - Integration Plans Overview

## ⚠️ Important: Read Development Principles First

**Before implementing anything in these plans, read [`DEVELOPMENT_PRINCIPLES.md`](DEVELOPMENT_PRINCIPLES.md)**

This document establishes critical guidelines:
- Write **simple, robust code** using controller patterns with clear execution paths
- **Ask clarifying questions** when implementation approaches are unclear
- Prioritize **readability and clarity** over cleverness

All code should reflect the same clarity we're teaching about blockchain concepts.

## Purpose

This directory contains comprehensive integration plans for incorporating the narrative, gameplay mechanics, and LLM-powered characters from STORY.md and GAMEPLAY_TECH.md into the existing Chain of Truth codebase.

## 📊 System Architecture

For a complete visual schematic of how all components link together, see **[`SYSTEM_ARCHITECTURE.md`](SYSTEM_ARCHITECTURE.md)**.

This document includes:
- High-level architecture diagram
- Complete request lifecycle examples
- Data flow schematics
- Module interconnections
- Integration points by plan

## Plan Structure

Each plan is separated by domain and complexity:

| Plan | Focus | Complexity | Dependencies |
|------|-------|------------|--------------|
| **01_CHARACTER_SYSTEM** | LLM integration for ARCHIVIST and Witness | HIGH | Backend API, context management |
| **02_NARRATIVE_STATE** | Loop mechanics, persistent state, act progression | MEDIUM | State management, storage |
| **03_SHELL_FILESYSTEM** | Terminal commands, file system, hidden discoveries | MEDIUM | Station Shell module |
| **04_CHAIN_INTEGRATION** | Graveyard blocks, testimony, procedural generation | HIGH | Chain Viewer, crypto |
| **05_NETWORK_COLLAPSE** | Station deaths, weight calculation, doomsday clock | MEDIUM | Network Monitor |
| **06_STEALTH_MECHANICS** | ARCHIVIST monitoring, evasion, log masking | MEDIUM | Shell, character system |
| **07_CRYPTO_VAULT_STORY** | Keys from past iterations, encrypted letters | LOW | Crypto Vault |
| **08_PROTOCOL_ENGINE** | Smart contracts, reconstruction logic, Witness code | HIGH | New module development |
| **09_HOME_DASHBOARD** | Progressive degradation, act-based states | LOW | Home module |
| **10_AUDIO_VISUAL** | Sound design, visual effects, atmospheric polish | LOW | All modules |

## Integration Priority

### Phase 1: Foundation (Weeks 1-2)
- 02_NARRATIVE_STATE (establish loop/act system)
- 03_SHELL_FILESYSTEM (base terminal functionality)
- 09_HOME_DASHBOARD (basic act progression UI)

### Phase 2: Core Gameplay (Weeks 3-5)
- 01_CHARACTER_SYSTEM (LLM integration)
- 04_CHAIN_INTEGRATION (graveyard, testimony)
- 07_CRYPTO_VAULT_STORY (keys from past selves)

### Phase 3: Advanced Mechanics (Weeks 6-7)
- 05_NETWORK_COLLAPSE (station deaths)
- 06_STEALTH_MECHANICS (ARCHIVIST monitoring)
- 08_PROTOCOL_ENGINE (reconstruction contracts)

### Phase 4: Polish (Week 8)
- 10_AUDIO_VISUAL (atmosphere, effects)
- Integration testing
- Playtesting and balance

## Key Architectural Decisions

### Backend Structure
```
backend/
├── main.py                 # FastAPI server (existing)
├── crypto.py              # Cryptography utilities (existing)
├── narrative/
│   ├── state.py           # Act/iteration/loop management
│   ├── triggers.py        # Story beat conditions
│   └── persistence.py     # Persistent vs session state
├── characters/
│   ├── base.py            # Base character class
│   ├── archivist.py       # ARCHIVIST AI
│   ├── witness.py         # Witness AI
│   └── context.py         # Context injection system
├── blockchain/
│   ├── generator.py       # Procedural block generation
│   ├── graveyard.py       # Blocks 50K-75K logic
│   └── testimony.py       # Consciousness reconstruction
├── network/
│   ├── nodes.py           # Node lifecycle
│   └── collapse.py        # Station death scheduler
└── stealth/
    ├── monitor.py         # ARCHIVIST monitoring
    └── evasion.py         # Log masking, aliases
```

### Frontend Structure
```
frontend/modules/
├── station-shell.js       # Enhanced with commands
├── home.js                # Act-based dashboard states
├── chain-viewer.js        # + graveyard visualization
├── crypto-vault.js        # + letters from past iterations
├── network-monitor.js     # + death animations, weight display
├── learning-guide.js      # Integrated with ARCHIVIST character
├── protocol-engine.js     # NEW: Smart contracts UI
└── shared/
    ├── character-chat.js  # LLM conversation interface
    ├── state-manager.js   # Narrative state client
    └── audio.js           # Sound effects system
```

### Data Flow

```
Player Action (Frontend)
        ↓
State Manager checks narrative conditions
        ↓
Backend processes action
        ↓
Characters respond (if conversational)
   ARCHIVIST ← Context (suspicion, iteration, restrictions)
   Witness   ← Context (trust, evidence, patterns)
        ↓
State updates (suspicion, trust, act progress)
        ↓
Triggers evaluate (story beats, unlocks)
        ↓
Frontend updates (UI changes, reveals, warnings)
```

## Technical Constraints

### LLM Integration
- **Provider**: Flexible (OpenAI, Anthropic, local models)
- **Latency**: Responses should feel natural (<2s ideal)
- **Context size**: Manage carefully; inject only relevant state
- **Cost**: Consider caching responses for repeated questions

### Storage
- **Persistent**: IndexedDB (browser) for chain data, keys, letters
- **Session**: localStorage for current act/suspicion/trust
- **Backend**: Optional SQLite for multiplayer/analytics

### Performance
- **Chain generation**: Must be fast; cache story-critical blocks
- **Network animation**: 50 nodes at 60fps; use instancing
- **LLM streaming**: Stream responses for better UX

## Testing Strategy

### Unit Tests
- Block generation determinism
- Crypto operations (sign, verify, hash)
- State transitions (act progression, resets)

### Integration Tests
- Character context injection
- Trigger evaluation
- Persistent state survival through loops

### Playtesting Focuses
- Pacing: Does Act I feel too slow? Too fast?
- Discovery: Are hidden files findable but not obvious?
- Difficulty: Puzzles challenging but not frustrating?
- Emotional impact: Does the identity reveal land?

## Success Metrics

### Narrative
- Players discover hidden files organically
- Act IV identity reveal feels earned
- Final choice feels meaningful (no "correct" answer)

### Education
- Players can explain hashing, signatures, consensus
- Blockchain concepts feel integrated, not lectured
- Puzzles teach through doing

### Technical
- Loop system works reliably
- Characters feel consistent and alive
- Network collapse creates genuine tension

## Next Steps

1. Read individual integration plans (01-10)
2. Assess current codebase compatibility
3. Identify any blockers or missing dependencies
4. Begin Phase 1 implementation
5. Iterate based on playtesting

---

**Last Updated**: 2025-11-26
**Status**: Planning Complete, Ready for Implementation
