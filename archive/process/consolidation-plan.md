# Documentation Consolidation Plan

**Current State**: 40 documentation files in root directory
**Goal**: Organize into clear, hierarchical structure with no duplication

---

## Proposed Structure

```
chain/
├── README.md                          # Main entry point (keep, update)
├── QUICKSTART.md                      # Single quick start guide (NEW - consolidate 3 guides)
├── PROJECT_COMPLETE.md                # Project completion summary (keep)
│
├── docs/
│   ├── user/                          # User-facing documentation
│   │   ├── getting-started.md         # Installation & first steps
│   │   ├── gameplay-guide.md          # How to play
│   │   ├── tutorial.md                # Complete tutorial walkthrough
│   │   └── faq.md                     # Frequently asked questions
│   │
│   ├── developer/                     # Developer documentation
│   │   ├── architecture.md            # System architecture (existing)
│   │   ├── api-reference.md           # All API endpoints
│   │   ├── testing-guide.md           # How to run tests
│   │   └── contributing.md            # Contribution guidelines
│   │
│   ├── features/                      # Feature-specific documentation
│   │   ├── character-system.md        # LLM characters
│   │   ├── narrative-state.md         # Loop mechanics & state
│   │   ├── filesystem.md              # Shell & filesystem
│   │   ├── stealth-mechanics.md       # Evasion system
│   │   ├── network-collapse.md        # Station deaths
│   │   ├── crypto-vault.md            # Encrypted letters
│   │   ├── protocol-engine.md         # Smart contracts
│   │   └── chain-integration.md       # Graveyard blocks
│   │
│   ├── phases/                        # Implementation history (archive)
│   │   ├── README.md                  # Phase overview
│   │   ├── phase-02-narrative.md      # Consolidate phase 02 docs
│   │   ├── phase-03-filesystem.md     # Consolidate phase 03 docs
│   │   ├── phase-04-chain.md          # Consolidate phase 04 docs
│   │   ├── phase-05-collapse.md       # Consolidate phase 05 docs
│   │   ├── phase-06-stealth.md        # Consolidate phase 06 docs
│   │   ├── phase-07-vault.md          # Consolidate phase 07 docs
│   │   ├── phase-08-contracts.md      # Consolidate phase 08 docs
│   │   ├── phase-09-degradation.md    # Consolidate phase 09 docs
│   │   └── phase-10-polish.md         # Consolidate phase 10 docs
│   │
│   └── integration_plans/             # Keep existing (already organized)
│       ├── 00_OVERVIEW.md
│       ├── 01_CHARACTER_SYSTEM.md
│       └── ... (all existing plans)
│
└── archive/                           # Move deprecated/redundant docs here
    ├── old-quickstarts/
    ├── phase-fragments/
    └── deprecated/
```

---

## Consolidation Actions

### 1. Create New Consolidated Documents

**QUICKSTART.md** (consolidate these 3):
- `QUICK_START.md`
- `QUICKSTART_CHARACTER_SYSTEM.md`
- `QUICKSTART_NARRATIVE_STATE.md`
- `STARTUP_GUIDE.md`

**docs/user/getting-started.md** (consolidate):
- Installation steps from README
- Setup from STARTUP_GUIDE
- First run instructions

**docs/user/gameplay-guide.md** (consolidate):
- `GAMEPLAY_TECH.md`
- Story elements from `STORY.md`
- Tutorial content

**docs/developer/testing-guide.md** (consolidate):
- `NARRATIVE_STATE_TESTING.md`
- Test instructions from phase docs
- All test commands

**docs/features/** (one file per system):
- Extract from phase COMPLETE docs
- Extract from QUICKREF docs
- Extract from IMPLEMENTATION_SUMMARY docs

**docs/phases/** (one consolidated file per phase):
- Phase 02: Merge PHASE_02_COMPLETE.txt, PHASE_02_CERTIFICATE.txt, PHASE_02_FINAL_DEMO.md, PHASE_02_SUMMARY.md, INTEGRATION_02_COMPLETE.md
- Phase 03: Merge PHASE_03_COMPLETE.md, PHASE_03_IMPLEMENTATION.md
- Phase 04: Merge PHASE_04_COMPLETE.md, PHASE_04_IMPLEMENTATION_COMPLETE.md
- Phases 05-10: Keep _COMPLETE.md, archive others

### 2. Update Existing Documents

**README.md**:
- Update with links to new structure
- Keep concise overview
- Point to QUICKSTART.md

**PROJECT_STATUS.md**:
- Archive (superseded by PROJECT_COMPLETE.md)

### 3. Archive Old Documents

Move to `archive/`:
- All duplicate quickstarts
- Phase fragments (CERTIFICATE.txt, COMMIT_MESSAGE.txt, SUMMARY.md)
- IMPLEMENTATION.md files (info moved to features/)
- DOCS_UPDATED.md, DOCUMENTATION_INDEX.md (superseded)
- README_STARTUP.txt (superseded by QUICKSTART.md)

### 4. Keep As-Is

**Root level** (essential files):
- README.md
- QUICKSTART.md (NEW)
- PROJECT_COMPLETE.md
- FEEDBACK.md
- STORY.md (narrative reference)
- GAMEPLAY_TECH.md (game design reference)

**docs/integration_plans/** (already well-organized):
- Keep entire directory unchanged

---

## Files to Consolidate (40 → ~20)

### Root Directory Files (Currently 40)

**Keep & Update (5)**:
1. README.md
2. PROJECT_COMPLETE.md
3. FEEDBACK.md
4. STORY.md
5. GAMEPLAY_TECH.md

**Create New (1)**:
6. QUICKSTART.md (consolidates 4 files)

**Move to docs/phases/ (10)**:
7-16. PHASE_02-10_COMPLETE.md → docs/phases/phase-XX.md (consolidated)

**Move to docs/features/ (10 quickrefs)**:
17-26. PHASE_XX_QUICKREF.md → Extract into feature docs

**Archive (24)**:
- QUICK_START.md
- QUICKSTART_CHARACTER_SYSTEM.md
- QUICKSTART_NARRATIVE_STATE.md
- STARTUP_GUIDE.md
- README_STARTUP.txt
- PROJECT_STATUS.md
- DOCUMENTATION_INDEX.md
- DOCS_UPDATED.md
- NARRATIVE_STATE_TESTING.md
- INTEGRATION_02_COMPLETE.md
- PHASE_02_CERTIFICATE.txt
- PHASE_02_COMPLETE.txt
- PHASE_02_FINAL_DEMO.md
- PHASE_02_SUMMARY.md
- PHASE_03_IMPLEMENTATION.md
- PHASE_04_IMPLEMENTATION_COMPLETE.md
- PHASE_05_COMMIT_MESSAGE.txt
- PHASE_07_SUMMARY.md
- All other phase fragments

---

## Result

**Before**: 40 files in root, significant duplication
**After**: 6 files in root, ~20 organized docs, clear hierarchy

**Benefits**:
- Clear entry points (README → QUICKSTART → detailed docs)
- No duplication
- Easy to find information
- Clean root directory
- Preserved history in phases/
- Feature docs separate from implementation history

---

## Implementation Order

1. Create `docs/` subdirectories
2. Create consolidated QUICKSTART.md
3. Create docs/user/ guides
4. Create docs/developer/ guides
5. Create docs/features/ per-system docs
6. Consolidate phase docs into docs/phases/
7. Move archived files to archive/
8. Update README.md with new structure
9. Delete superseded files
10. Verify all links work

---

**Status**: Plan ready for review and implementation
