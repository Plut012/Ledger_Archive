# Chain of Truth - Documentation Index

Complete guide to all documentation. Start here to find what you need.

---

## 🚀 Quick Links

**Just want to get started?** → [`QUICKSTART.md`](QUICKSTART.md)
**Completed project summary?** → [`PROJECT_COMPLETE.md`](PROJECT_COMPLETE.md)
**Main project README?** → [`README.md`](README.md)

---

## 📚 Documentation Structure

```
chain/
├── README.md                   # Main project overview
├── QUICKSTART.md               # 5-minute setup guide
├── PROJECT_COMPLETE.md         # Complete project summary
├── DOCS_INDEX.md              # This file
├── STORY.md                    # Narrative background
├── GAMEPLAY_TECH.md            # Game design document
├── FEEDBACK.md                 # How to report issues
│
├── docs/
│   ├── user/                   # Player/User guides
│   │   ├── getting-started.md  # Installation & setup
│   │   ├── gameplay-guide.md   # How to play
│   │   ├── tutorial.md         # Complete walkthrough (TODO)
│   │   └── faq.md              # Common questions (TODO)
│   │
│   ├── developer/              # Developer documentation (TODO)
│   │   ├── architecture.md     # System architecture
│   │   ├── api-reference.md    # All API endpoints
│   │   ├── testing-guide.md    # How to run tests
│   │   └── contributing.md     # Contribution guide
│   │
│   ├── features/               # Feature-specific docs
│   │   ├── character-system.md     # LLM characters
│   │   ├── narrative-state.md      # Loop mechanics
│   │   ├── filesystem.md           # Shell & filesystem
│   │   ├── stealth-mechanics.md    # Evasion system
│   │   ├── network-collapse.md     # Station deaths
│   │   ├── crypto-vault.md         # Encrypted letters
│   │   ├── protocol-engine.md      # Smart contracts
│   │   └── chain-integration.md    # Graveyard blocks
│   │
│   ├── phases/                 # Implementation history
│   │   ├── README.md           # Phase overview
│   │   ├── phase-02-narrative.md
│   │   ├── phase-03-filesystem.md
│   │   ├── phase-04-chain.md
│   │   ├── phase-05-collapse.md
│   │   ├── phase-06-stealth.md
│   │   ├── phase-07-vault.md
│   │   ├── phase-08-contracts.md
│   │   ├── phase-09-degradation.md
│   │   └── phase-10-polish.md
│   │
│   └── integration_plans/      # Original planning docs (existing)
│       ├── 00_OVERVIEW.md
│       ├── 01-10 plans...
│       ├── SYSTEM_ARCHITECTURE.md
│       └── DEVELOPMENT_PRINCIPLES.md
│
├── backend/
│   ├── API_KEY_SETUP.md           # API configuration
│   ├── CHARACTER_SYSTEM_README.md  # Character tech details
│   └── IMPLEMENTATION_SUMMARY.md   # Backend summary
│
└── archive/                    # Old/deprecated docs
    ├── old-quickstarts/
    ├── phase-fragments/
    └── deprecated/
```

---

## 📖 Documentation by Audience

### For New Players

**Start here:**
1. [`QUICKSTART.md`](QUICKSTART.md) - Get running in 5 minutes
2. [`docs/user/getting-started.md`](docs/user/getting-started.md) - Complete installation
3. [`docs/user/gameplay-guide.md`](docs/user/gameplay-guide.md) - How to play

**Then explore:**
- [`STORY.md`](STORY.md) - Narrative background
- [`GAMEPLAY_TECH.md`](GAMEPLAY_TECH.md) - Game mechanics
- In-game Learning Guide module - Interactive tutorial

### For Developers

**Essential reading:**
1. [`README.md`](README.md) - Project overview
2. [`PROJECT_COMPLETE.md`](PROJECT_COMPLETE.md) - What's been built
3. [`docs/integration_plans/00_OVERVIEW.md`](docs/integration_plans/00_OVERVIEW.md) - System architecture
4. [`docs/integration_plans/DEVELOPMENT_PRINCIPLES.md`](docs/integration_plans/DEVELOPMENT_PRINCIPLES.md) - Code philosophy

**Deep dives:**
- [`docs/integration_plans/SYSTEM_ARCHITECTURE.md`](docs/integration_plans/SYSTEM_ARCHITECTURE.md) - Technical architecture
- [`backend/CHARACTER_SYSTEM_README.md`](backend/CHARACTER_SYSTEM_README.md) - LLM integration
- Individual phase completion docs in root directory

**API reference:**
- [`backend/API_KEY_SETUP.md`](backend/API_KEY_SETUP.md) - API configuration
- http://localhost:8000/docs - Swagger UI (when running)

### For Contributors

**Before contributing:**
1. [`FEEDBACK.md`](FEEDBACK.md) - How to report issues
2. [`docs/integration_plans/DEVELOPMENT_PRINCIPLES.md`](docs/integration_plans/DEVELOPMENT_PRINCIPLES.md) - Code standards
3. `docs/developer/contributing.md` - Contribution workflow (TODO)

**Understanding the codebase:**
- [`docs/integration_plans/00_OVERVIEW.md`](docs/integration_plans/00_OVERVIEW.md) - Architecture overview
- Phase completion docs - Implementation details
- Test files in `backend/test_*.py` - See how systems work

---

## 📋 Documentation by Topic

### Installation & Setup
- [`QUICKSTART.md`](QUICKSTART.md) - Quick setup
- [`docs/user/getting-started.md`](docs/user/getting-started.md) - Detailed installation
- [`backend/API_KEY_SETUP.md`](backend/API_KEY_SETUP.md) - API configuration
- `backend/start_mongodb.sh` - MongoDB setup script

### Gameplay & Narrative
- [`docs/user/gameplay-guide.md`](docs/user/gameplay-guide.md) - Complete gameplay guide
- [`STORY.md`](STORY.md) - Narrative design
- [`GAMEPLAY_TECH.md`](GAMEPLAY_TECH.md) - Mechanics design
- In-game modules - Interactive experience

### System Architecture
- [`docs/integration_plans/SYSTEM_ARCHITECTURE.md`](docs/integration_plans/SYSTEM_ARCHITECTURE.md) - Technical architecture
- [`docs/integration_plans/00_OVERVIEW.md`](docs/integration_plans/00_OVERVIEW.md) - Integration overview
- [`PROJECT_COMPLETE.md`](PROJECT_COMPLETE.md) - What's implemented

### Features (Individual Systems)
- **Character System**: [`PHASE_02_QUICKREF.md`](PHASE_02_QUICKREF.md), [`PHASE_01_COMPLETE.md`](PHASE_01_COMPLETE.md)
- **Narrative State**: [`PHASE_02_COMPLETE.md`](PHASE_02_COMPLETE.md), [`docs/integration_plans/02_NARRATIVE_STATE.md`](docs/integration_plans/02_NARRATIVE_STATE.md)
- **Filesystem**: [`PHASE_03_COMPLETE.md`](PHASE_03_COMPLETE.md), [`PHASE_03_QUICKREF.md`](PHASE_03_QUICKREF.md)
- **Chain Integration**: [`PHASE_04_COMPLETE.md`](PHASE_04_COMPLETE.md), [`PHASE_04_QUICKREF.md`](PHASE_04_QUICKREF.md)
- **Network Collapse**: [`PHASE_05_COMPLETE.md`](PHASE_05_COMPLETE.md), [`PHASE_05_QUICKREF.md`](PHASE_05_QUICKREF.md)
- **Stealth Mechanics**: [`PHASE_06_COMPLETE.md`](PHASE_06_COMPLETE.md), [`PHASE_06_QUICKREF.md`](PHASE_06_QUICKREF.md)
- **Crypto Vault**: [`PHASE_07_COMPLETE.md`](PHASE_07_COMPLETE.md), [`PHASE_07_QUICKREF.md`](PHASE_07_QUICKREF.md)
- **Protocol Engine**: [`PHASE_08_COMPLETE.md`](PHASE_08_COMPLETE.md), [`PHASE_08_QUICKREF.md`](PHASE_08_QUICKREF.md)
- **Home Dashboard**: [`PHASE_09_COMPLETE.md`](PHASE_09_COMPLETE.md), [`PHASE_09_QUICKREF.md`](PHASE_09_QUICKREF.md)
- **Audio/Visual**: [`PHASE_10_COMPLETE.md`](PHASE_10_COMPLETE.md), [`PHASE_10_QUICKREF.md`](PHASE_10_QUICKREF.md)

### Testing
- `./test-backend.sh` - Run all tests
- [`backend/test_*.py`](backend/) - Individual test suites
- Phase completion docs - Testing sections
- `docs/developer/testing-guide.md` - Complete testing guide (TODO)

### API Reference
- http://localhost:8000/docs - Interactive Swagger UI
- Phase QUICKREF docs - API endpoint summaries
- `backend/main.py` - API endpoint definitions
- `docs/developer/api-reference.md` - Complete reference (TODO)

---

## 🎯 Common Tasks

### "I want to install and run the game"
→ [`QUICKSTART.md`](QUICKSTART.md)

### "I want to learn how to play"
→ [`docs/user/gameplay-guide.md`](docs/user/gameplay-guide.md)

### "I'm stuck on installation"
→ [`docs/user/getting-started.md`](docs/user/getting-started.md) (Troubleshooting section)

### "I want to understand the narrative"
→ [`STORY.md`](STORY.md) + [`docs/user/gameplay-guide.md`](docs/user/gameplay-guide.md)

### "I want to contribute code"
→ [`docs/integration_plans/DEVELOPMENT_PRINCIPLES.md`](docs/integration_plans/DEVELOPMENT_PRINCIPLES.md) + `docs/developer/contributing.md`

### "I want to understand the architecture"
→ [`docs/integration_plans/SYSTEM_ARCHITECTURE.md`](docs/integration_plans/SYSTEM_ARCHITECTURE.md)

### "I want to add a new feature"
→ Read relevant phase completion docs + integration plans

### "I found a bug"
→ [`FEEDBACK.md`](FEEDBACK.md)

### "How do I configure the LLM?"
→ [`backend/API_KEY_SETUP.md`](backend/API_KEY_SETUP.md)

### "How do tests work?"
→ `./test-backend.sh` + individual `backend/test_*.py` files

### "What's been implemented?"
→ [`PROJECT_COMPLETE.md`](PROJECT_COMPLETE.md)

### "How does [specific feature] work?"
→ Find the phase in root directory (e.g., `PHASE_06_COMPLETE.md` for stealth)

---

## 📁 Root Directory Files Explained

### Active Documentation
- **README.md** - Main project overview, first thing new users see
- **QUICKSTART.md** - Fast-track to running the application
- **PROJECT_COMPLETE.md** - Comprehensive completion summary
- **DOCS_INDEX.md** - This file - navigation hub
- **STORY.md** - Narrative design document
- **GAMEPLAY_TECH.md** - Game mechanics design
- **FEEDBACK.md** - Bug reporting and feedback

### Phase Completion Certificates
- **PHASE_02_COMPLETE.md** - Narrative State System
- **PHASE_03_COMPLETE.md** - Shell & Filesystem
- **PHASE_04_COMPLETE.md** - Chain Integration
- **PHASE_05_COMPLETE.md** - Network Collapse
- **PHASE_06_COMPLETE.md** - Stealth Mechanics
- **PHASE_07_COMPLETE.md** - Crypto Vault Story
- **PHASE_08_COMPLETE.md** - Protocol Engine
- **PHASE_09_COMPLETE.md** - Home Dashboard
- **PHASE_10_COMPLETE.md** - Audio & Visual

### Quick Reference Guides
- **PHASE_XX_QUICKREF.md** - API endpoints and quick usage for each phase

### Planning & Design
- **docs/integration_plans/** - Original integration plans (well-organized)
- **backend/IMPLEMENTATION_SUMMARY.md** - Backend implementation overview

---

## 🗂️ Archive Directory

**Location**: `archive/`

Contains superseded documentation that's been consolidated:

- **old-quickstarts/** - Replaced by `QUICKSTART.md`
- **phase-fragments/** - Merged into phase completion docs
- **deprecated/** - Outdated status files, superseded indexes

These files are preserved for reference but should not be used for current information.

---

## 🔄 Documentation Status

### ✅ Complete
- Installation guides
- Quick starts
- Gameplay guide
- All phase completion docs
- Phase quick references
- Integration planning docs
- System architecture
- API key setup

### 🚧 In Progress
- Feature-specific docs (docs/features/)
- Consolidated phase docs (docs/phases/)

### 📋 TODO
- Tutorial walkthrough (docs/user/tutorial.md)
- FAQ (docs/user/faq.md)
- Developer guides (docs/developer/)
- API reference consolidation
- Contributing guide
- Testing guide consolidation

---

## 💡 Documentation Tips

### For Readers
- Start with overview docs before diving deep
- Use Ctrl+F to search within documents
- Check "Last Updated" dates on files
- Archived docs may be outdated - use current versions

### For Writers
- Follow existing formatting conventions
- Include code examples where relevant
- Link to related documents
- Update this index when adding new docs
- Mark TODO items clearly

### For Maintainers
- Keep DOCS_INDEX.md up to date
- Archive superseded docs, don't delete
- Maintain clear directory structure
- Consolidate duplicates
- Regular documentation reviews

---

## 🔗 External Resources

### Technologies Used
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [UV](https://github.com/astral-sh/uv) - Package manager
- [MongoDB](https://www.mongodb.com/docs/) - Database
- [Anthropic Claude](https://docs.anthropic.com/) - LLM API
- [OpenAI](https://platform.openai.com/docs/) - Alternative LLM

### Learning Resources
- Blockchain basics: In-game Learning Guide module
- Smart contracts: [Solidity docs](https://docs.soliditylang.org/)
- Cryptography: In-game Crypto Vault tutorial

---

## 📞 Getting Help

**Installation issues?** → [`docs/user/getting-started.md`](docs/user/getting-started.md) Troubleshooting section

**Gameplay questions?** → [`docs/user/gameplay-guide.md`](docs/user/gameplay-guide.md)

**Bug reports?** → [`FEEDBACK.md`](FEEDBACK.md)

**Can't find what you need?** → Check this index or search the repository

---

**Last Updated**: 2025-11-30
**Documentation Version**: 2.0 (Consolidated)

*"The chain remembers. The documentation persists."*
