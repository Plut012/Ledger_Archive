# Documentation Audit - Action Plan

**Goal**: Reduce root directory clutter, keep only essential user-facing docs

---

## Root Directory Files - Categorization

### ✅ KEEP (6 files - Essential user-facing)

| File | Why Keep | Purpose |
|------|----------|---------|
| **README.md** | Primary entry point | First thing users see, project overview |
| **QUICKSTART.md** | Essential for users | 5-minute setup guide |
| **STORY.md** | Game reference | Narrative design, player reference |
| **GAMEPLAY_TECH.md** | Game reference | Mechanics reference |
| **FEEDBACK.md** | User support | Bug reporting |
| **PROJECT_COMPLETE.md** | Summary document | Final status, showcase |

---

### 📦 ARCHIVE (3 files - Process docs, not user-facing)

| File | Action | Reason |
|------|--------|--------|
| **DOCUMENTATION_CONSOLIDATION_PLAN.md** | → `archive/process/` | Internal consolidation plan |
| **DOCUMENTATION_CONSOLIDATION_COMPLETE.md** | → `archive/process/` | Internal completion report |
| **DOCS_INDEX.md** | → `archive/deprecated/` | Superseded by README structure |

**Why archive DOCS_INDEX.md?**
- README.md now has clear doc links
- Too much redundancy with README
- Adds clutter without unique value
- Information duplicated in README

---

### 📁 MOVE (18 files - Developer/historical docs)

**PHASE_XX_COMPLETE.md (9 files)**
All phase completion docs → `docs/phases/`

| File | New Location |
|------|--------------|
| PHASE_02_COMPLETE.md | docs/phases/phase-02-narrative-state.md |
| PHASE_03_COMPLETE.md | docs/phases/phase-03-shell-filesystem.md |
| PHASE_04_COMPLETE.md | docs/phases/phase-04-chain-integration.md |
| PHASE_05_COMPLETE.md | docs/phases/phase-05-network-collapse.md |
| PHASE_06_COMPLETE.md | docs/phases/phase-06-stealth-mechanics.md |
| PHASE_07_COMPLETE.md | docs/phases/phase-07-crypto-vault.md |
| PHASE_08_COMPLETE.md | docs/phases/phase-08-protocol-engine.md |
| PHASE_09_COMPLETE.md | docs/phases/phase-09-home-dashboard.md |
| PHASE_10_COMPLETE.md | docs/phases/phase-10-audio-visual.md |

**PHASE_XX_QUICKREF.md (9 files)**
All quick refs → `docs/api/`

| File | New Location |
|------|--------------|
| PHASE_02_QUICKREF.md | docs/api/narrative-state.md |
| PHASE_03_QUICKREF.md | docs/api/shell-filesystem.md |
| PHASE_04_QUICKREF.md | docs/api/chain-integration.md |
| PHASE_05_QUICKREF.md | docs/api/network-collapse.md |
| PHASE_06_QUICKREF.md | docs/api/stealth-mechanics.md |
| PHASE_07_QUICKREF.md | docs/api/crypto-vault.md |
| PHASE_08_QUICKREF.md | docs/api/protocol-engine.md |
| PHASE_09_QUICKREF.md | docs/api/home-dashboard.md |
| PHASE_10_QUICKREF.md | docs/api/audio-visual.md |

---

### ❌ DELETE (0 files)

**Nothing to delete** - All files have value either as:
- User-facing documentation (keep in root)
- Developer reference (move to docs/)
- Process documentation (archive)

---

## New Directory Structure

```
chain/
├── README.md                      # Main entry (updated with better links)
├── QUICKSTART.md                  # Quick setup
├── PROJECT_COMPLETE.md            # Final summary
├── STORY.md                       # Narrative reference
├── GAMEPLAY_TECH.md               # Mechanics reference
├── FEEDBACK.md                    # Bug reporting
│
├── docs/
│   ├── user/
│   │   ├── getting-started.md     # Existing
│   │   └── gameplay-guide.md      # Existing
│   │
│   ├── phases/                    # NEW - Phase implementation history
│   │   ├── README.md              # Phase overview
│   │   ├── phase-02-narrative-state.md
│   │   ├── phase-03-shell-filesystem.md
│   │   ├── phase-04-chain-integration.md
│   │   ├── phase-05-network-collapse.md
│   │   ├── phase-06-stealth-mechanics.md
│   │   ├── phase-07-crypto-vault.md
│   │   ├── phase-08-protocol-engine.md
│   │   ├── phase-09-home-dashboard.md
│   │   └── phase-10-audio-visual.md
│   │
│   ├── api/                       # NEW - API quick references
│   │   ├── README.md              # API overview
│   │   ├── narrative-state.md
│   │   ├── shell-filesystem.md
│   │   ├── chain-integration.md
│   │   ├── network-collapse.md
│   │   ├── stealth-mechanics.md
│   │   ├── crypto-vault.md
│   │   ├── protocol-engine.md
│   │   ├── home-dashboard.md
│   │   └── audio-visual.md
│   │
│   └── integration_plans/         # Existing (keep)
│
├── archive/
│   ├── process/                   # NEW - Internal process docs
│   │   ├── consolidation-plan.md
│   │   └── consolidation-complete.md
│   ├── old-quickstarts/           # Existing
│   ├── phase-fragments/           # Existing
│   └── deprecated/                # Existing (add DOCS_INDEX.md)
│
└── backend/
    ├── API_KEY_SETUP.md           # Keep (essential setup)
    ├── CHARACTER_SYSTEM_README.md # Keep (technical reference)
    └── IMPLEMENTATION_SUMMARY.md  # Keep (backend overview)
```

---

## Summary of Changes

### Root Directory
**Before**: 26 markdown files
**After**: 6 markdown files
**Reduction**: 77% fewer files in root

### Files by Action
- **Keep in root**: 6 files
- **Move to docs/phases/**: 9 files
- **Move to docs/api/**: 9 files
- **Archive**: 3 files
- **Delete**: 0 files

---

## Rationale

### Why Keep These 6?

**README.md** - Non-negotiable entry point
**QUICKSTART.md** - First thing users need
**PROJECT_COMPLETE.md** - Showcases what was built
**STORY.md** - Players reference this
**GAMEPLAY_TECH.md** - Players reference this
**FEEDBACK.md** - Support/issues

### Why Move Phase Docs?

- Developer/historical reference, not user-facing
- Users don't need 9 phase docs in root
- Better organized in `docs/phases/`
- Still accessible, just not in the way

### Why Move Quick Refs?

- API reference material
- Developers use these, not players
- Belongs in `docs/api/` structure
- Can consolidate into single API ref later

### Why Archive Process Docs?

- Internal consolidation docs
- Not needed for daily use
- Valuable as historical record
- Clutters root directory

---

## Implementation Steps

1. Create `docs/phases/` directory
2. Create `docs/api/` directory
3. Create `archive/process/` directory
4. Move 9 PHASE_XX_COMPLETE.md → docs/phases/ (rename)
5. Move 9 PHASE_XX_QUICKREF.md → docs/api/ (rename)
6. Move consolidation docs → archive/process/
7. Move DOCS_INDEX.md → archive/deprecated/
8. Update README.md with new structure
9. Create docs/phases/README.md (overview)
10. Create docs/api/README.md (overview)

---

## Updated README.md Structure

```markdown
# Chain of Truth

## Quick Links
- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
- **[PROJECT_COMPLETE.md](PROJECT_COMPLETE.md)** - What's been built
- **[STORY.md](STORY.md)** - Narrative design
- **[GAMEPLAY_TECH.md](GAMEPLAY_TECH.md)** - Game mechanics

## Documentation

### For Players
- [Installation Guide](docs/user/getting-started.md)
- [Gameplay Guide](docs/user/gameplay-guide.md)

### For Developers
- [API Reference](docs/api/README.md) - All endpoints
- [Phase History](docs/phases/README.md) - Implementation details
- [System Architecture](docs/integration_plans/SYSTEM_ARCHITECTURE.md)
- [Backend Setup](backend/API_KEY_SETUP.md)

## Support
- [Report Issues](FEEDBACK.md)
```

---

## Result

**Clean root directory** with only essential user-facing files:
- README (overview)
- QUICKSTART (setup)
- PROJECT_COMPLETE (summary)
- STORY (narrative)
- GAMEPLAY_TECH (mechanics)
- FEEDBACK (support)

**Organized docs/** with clear categories:
- user/ - Player guides
- phases/ - Implementation history
- api/ - API references
- integration_plans/ - Architecture (existing)

**Preserved history** in archive/:
- process/ - Consolidation docs
- old-quickstarts/ - Superseded guides
- phase-fragments/ - Merged pieces
- deprecated/ - Outdated docs

---

**Approve this plan?** I'll execute all moves and create necessary overview files.
