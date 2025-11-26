# Chain of Truth - Integration Plans

## Overview

This directory contains comprehensive integration plans for transforming the Chain of Truth prototype into a fully-realized narrative thriller with LLM-powered characters and immersive blockchain education.

## ⚠️ READ FIRST: Development Principles

**Before implementing any plan, read [`DEVELOPMENT_PRINCIPLES.md`](DEVELOPMENT_PRINCIPLES.md)**

Key principles:
- **Write simple, robust code** - Controllers with clear execution paths, not clever abstractions
- **Ask clarifying questions** - When approaches, resources, or implementation details are unclear
- **Prioritize readability** - The code should be as clear as the blockchain concepts we're teaching

These principles apply to ALL implementation work in these plans.

## What's Been Created

Based on **STORY.md** and **GAMEPLAY_TECH.md**, these plans detail:

1. **Technical implementation** - Backend and frontend architecture
2. **Story integration** - How narrative beats trigger and progress
3. **Character systems** - LLM integration for ARCHIVIST and Witness
4. **Gameplay mechanics** - Loop system, stealth, procedural generation
5. **Estimated effort** - Time projections for each component

## Files in This Directory

| File | Focus | Complexity | Estimated Time |
|------|-------|------------|----------------|
| **DEVELOPMENT_PRINCIPLES.md** | **⚠️ READ FIRST** - Code quality, TDD workflow | - | - |
| **SYSTEM_ARCHITECTURE.md** | **📊 System schematic** - How everything links together | - | - |
| **00_OVERVIEW.md** | Master plan, architecture, priorities | - | - |
| **01_CHARACTER_SYSTEM.md** | LLM integration, ARCHIVIST, Witness | HIGH | 1.5 weeks |
| **02_NARRATIVE_STATE.md** | Loop mechanics, state management, triggers | MEDIUM | 1 week |
| **03_SHELL_FILESYSTEM.md** | Terminal, commands, hidden files | MEDIUM | 1 week |
| **04_CHAIN_INTEGRATION.md** | Graveyard blocks, testimony, procedural generation | HIGH | 1.5 weeks |
| **05_NETWORK_COLLAPSE.md** | Station deaths, weight calculation | MEDIUM | 4-5 days |
| **06_STEALTH_MECHANICS.md** | ARCHIVIST monitoring, evasion | MEDIUM | 3-4 days |
| **07_CRYPTO_VAULT_STORY.md** | Keys from past iterations, letters | LOW | 2-3 days |
| **08_PROTOCOL_ENGINE.md** | Smart contracts, new module | HIGH | 1-1.5 weeks |
| **09_HOME_DASHBOARD.md** | Progressive degradation UI | LOW | 2-3 days |
| **10_AUDIO_VISUAL.md** | Sound design, visual effects | LOW | 3-4 days |

## Implementation Phases

### Phase 1: Foundation (Weeks 1-2)
**Goal**: Establish core systems that everything else builds on

- ✅ 02_NARRATIVE_STATE - Loop/act system, triggers
- ✅ 03_SHELL_FILESYSTEM - Basic terminal and file discovery
- ✅ 09_HOME_DASHBOARD - Act-based UI states

**Why first**: These provide the scaffolding for all narrative progression.

### Phase 2: Core Gameplay (Weeks 3-5)
**Goal**: Implement the heart of the experience

- ✅ 01_CHARACTER_SYSTEM - ARCHIVIST and Witness LLMs
- ✅ 04_CHAIN_INTEGRATION - Graveyard, testimony, procedural blocks
- ✅ 07_CRYPTO_VAULT_STORY - Keys from past selves

**Why second**: Characters drive the narrative, chain holds the mystery.

### Phase 3: Advanced Mechanics (Weeks 6-7)
**Goal**: Add depth and tension

- ✅ 05_NETWORK_COLLAPSE - Real-time station deaths
- ✅ 06_STEALTH_MECHANICS - ARCHIVIST monitoring
- ✅ 08_PROTOCOL_ENGINE - Smart contracts

**Why third**: These enhance existing systems with complexity.

### Phase 4: Polish (Week 8)
**Goal**: Make it feel alive

- ✅ 10_AUDIO_VISUAL - Sound, effects, atmosphere
- Integration testing
- Playtesting and iteration

**Why last**: Polish after mechanics are solid.

## Total Estimated Timeline

**8-9 weeks** for full implementation with one developer.

**Parallelization potential**: With 2-3 developers, could complete in 4-6 weeks by running phases concurrently.

## Key Architectural Decisions

### Backend Stack
- **FastAPI** (existing) - REST API
- **Python 3.11+** - Backend logic
- **LLM Integration** - OpenAI or Anthropic (abstracted)
- **Storage** - IndexedDB (client-side), optional SQLite

### Frontend Stack
- **Vanilla JavaScript** (existing) - Keep it simple
- **Module system** - Each UI component is independent
- **IndexedDB** - Persistent state across loops
- **localStorage** - Session state

### Data Flow
```
Player Action
    ↓
State Manager (checks narrative conditions)
    ↓
Backend (processes, LLM if needed)
    ↓
Trigger Evaluation (story beats)
    ↓
State Updates
    ↓
UI Updates (reveals, warnings, effects)
```

## How to Use These Plans

### For Implementation
1. Start with **00_OVERVIEW.md** for the big picture
2. Follow phases in order (Foundation → Core → Advanced → Polish)
3. Each plan includes:
   - Current state assessment
   - Target state description
   - Code examples and architecture
   - Integration steps
   - Testing checklist

### For Planning
- Use effort estimates to create sprint plans
- Identify dependencies between plans
- Determine team assignments

### For Reference
- Architecture diagrams and patterns
- API endpoint specifications
- State management structure

## Critical Dependencies

### External
- **LLM API** (OpenAI or Anthropic) - Required for characters
- **Audio assets** - Can start with placeholders
- **Visual assets** - Particle textures, glitch effects

### Internal
- **Narrative State** (Plan 02) must be implemented before most other systems
- **Character System** (Plan 01) required for full narrative experience
- **Chain Integration** (Plan 04) needed for graveyard/testimony mechanics

## Success Metrics

### Technical
- [ ] Loop system reliably resets and persists data
- [ ] LLM characters respond consistently in-character
- [ ] Procedural generation is deterministic
- [ ] Triggers fire at correct thresholds
- [ ] State synchronizes between frontend/backend

### Narrative
- [ ] Players discover hidden files organically
- [ ] Act IV identity reveal feels earned and impactful
- [ ] Final choice feels meaningful (no "correct" answer)
- [ ] Multiple playthroughs reveal new details

### Educational
- [ ] Players can explain blockchain concepts after playing
- [ ] Puzzles teach through doing, not lecturing
- [ ] Technical accuracy maintained throughout

## Next Steps

1. **Review all plans** - Ensure team understands scope
2. **Set up development environment** - LLM API keys, dependencies
3. **Create sprint backlog** - Break plans into tasks
4. **Begin Phase 1** - Start with narrative state system
5. **Iterate based on playtesting** - Adjust pacing, difficulty, reveals

## Questions or Blockers?

- **LLM costs?** - Estimate API usage, consider caching
- **Performance concerns?** - Profile procedural generation
- **Team size?** - Adjust timeline based on resources
- **Scope creep?** - Stick to plans, defer nice-to-haves

---

**Created**: 2025-11-26
**Based on**: STORY.md, GAMEPLAY_TECH.md
**Status**: Planning Complete, Ready for Implementation

These plans represent a complete roadmap from the current prototype to a finished narrative thriller that teaches blockchain concepts through immersive gameplay. Each plan is detailed enough to begin implementation immediately.

Good luck, and may the chain remember what we build.
