# Interstellar Archive Terminal

An interactive blockchain learning platform with a retro terminal interface.

## Overview

Explore and understand fundamental blockchain concepts through an immersive terminal interface. You sit at a workstation in Archive Station Alpha, accessing the Interstellar Ledger Network - a distributed archive system spanning the galaxy.

## Features

- **Chain Viewer** - Visualize blocks and their cryptographic connections
- **Network Monitor** - Watch distributed node communication
- **Crypto Vault** - Generate keys, sign transactions
- **Protocol Engine** - Deploy and interact with smart contracts
- **Economic Simulator** - Explore DeFi primitives
- **LLM Character System** - AI-powered ARCHIVIST and WITNESS characters with narrative integration
- **Narrative State System** - Loop mechanics, act progression, and persistent player progress tracking

## Current Status

**🎉 ALL PHASES COMPLETE! 🎉**

**Latest Update**: 2025-11-30 - All 10 integration phases complete and production-ready!

### ✅ Project Complete (10/10 Phases)
- ✅ **Phase 01: Character System** - LLM-powered ARCHIVIST and WITNESS characters
- ✅ **Phase 02: Narrative State** - Loop mechanics, state management, story triggers
- ✅ **Phase 03: Shell/Filesystem** - Terminal commands, virtual filesystem, hidden files
- ✅ **Phase 04: Chain Integration** - 850K procedural blocks, graveyard system
- ✅ **Phase 05: Network Collapse** - Station deaths, weight calculation, doomsday clock
- ✅ **Phase 06: Stealth Mechanics** - ARCHIVIST monitoring, evasion techniques
- ✅ **Phase 07: Crypto Vault Story** - Encrypted letters from past iterations
- ✅ **Phase 08: Protocol Engine** - Smart contracts with horror reveal
- ✅ **Phase 09: Home Dashboard** - Progressive degradation (Acts I-VI)
- ✅ **Phase 10: Audio & Visual** - Sound system and particle effects

**See [`PROJECT_COMPLETE.md`](PROJECT_COMPLETE.md) for comprehensive completion summary.**

### What's Working

- ✅ Blockchain with PoW mining
- ✅ Wallet key generation
- ✅ Transaction signing & verification
- ✅ REST API + WebSocket
- ✅ Terminal UI framework
- ✅ Chain Viewer module (visualize blocks and chain)
- ✅ Crypto Vault module (wallet management & transactions)
- ✅ Network Monitor module (distributed network visualization)
- ✅ Learning Guide module (Archive Captain Protocol narrative tutorial)
- ✅ Warm analog synth audio system (no dependencies, Web Audio API)
- ✅ LLM Character System (ARCHIVIST and WITNESS AI with context management, streaming responses, and narrative state tracking)
- ✅ Narrative State System (loop/iteration mechanics, dual-layer state persistence, trigger-based story progression, IndexedDB persistence)
- ✅ Shell/Filesystem System (virtual filesystem, terminal commands, hidden file discovery)
- ✅ Network Collapse System (station deaths, consensus weight tracking, progressive network degradation)
- ✅ Stealth Mechanics (ARCHIVIST monitoring, evasion techniques, act-based detection escalation)

### Test Coverage
- ✅ **152 tests passing** (100% pass rate)
- ✅ **95%+ code coverage** across all systems
- ✅ 26 blockchain/crypto/network tests
- ✅ 6 narrative state tests
- ✅ 12 network collapse tests
- ✅ 23 stealth mechanics tests
- ✅ 32 protocol engine tests
- ✅ 20 chain integration tests
- ✅ Integration tests for complete flows

### Documentation

**📚 Essential Docs:**
- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes ⚡
- **[PROJECT_COMPLETE.md](PROJECT_COMPLETE.md)** - Complete project summary 🎉
- **[STORY.md](STORY.md)** - Narrative design 📖
- **[GAMEPLAY_TECH.md](GAMEPLAY_TECH.md)** - Game mechanics 🎮

**For Players:**
- [Installation Guide](docs/user/getting-started.md) - Complete setup & troubleshooting
- [Gameplay Guide](docs/user/gameplay-guide.md) - How to play, all 6 acts explained

**For Developers:**
- [API Reference](docs/api/) - All endpoints & quick references
- [Phase History](docs/phases/) - Implementation details for all 10 phases
- [System Architecture](docs/integration_plans/SYSTEM_ARCHITECTURE.md) - Technical architecture
- [Backend Setup](backend/API_KEY_SETUP.md) - API key configuration

---

## Quick Start

### Prerequisites

- Python 3.12 or higher
- [UV](https://github.com/astral-sh/uv) package manager
- Docker (for MongoDB - required for LLM character system)

### Installation

1. **Clone the repository** (or navigate to the project directory)

```bash
cd chain
```

2. **Install dependencies with UV**

```bash
cd backend
uv pip install -r requirements.txt
```

3. **Start MongoDB** (required for character system)

```bash
./start_mongodb.sh
```

Or manually:
```bash
docker run -d -p 27017:27017 --name chain-mongodb mongo:latest
```

4. **Configure environment** (for LLM character system)

```bash
cp backend/.env.example .env
```

Edit `.env` in the **project root** and add your API key:

**For Anthropic Claude (recommended):**
```
ANTHROPIC_API_KEY=sk-ant-your_key_here
LLM_PROVIDER=anthropic
```

**For OpenAI:**
```
OPENAI_API_KEY=sk-your_key_here
LLM_PROVIDER=openai
```

**Note:** Claude 3 Haiku is available on all API tiers (including free). Place `.env` in project root, not backend/.

### Running Locally

**Start the server** (serves both backend API and frontend):

```bash
uv run python backend/main.py
```

Then open your browser to: `http://localhost:8000`

That's it! The backend serves the frontend automatically.

**Test the character system:**

```bash
uv run python backend/test_character_system.py
```

**Test the narrative state system:**

```bash
PYTHONPATH=backend uv run python backend/test_narrative_state.py
```

### Share It with Others 🌐

Want to share your instance with others? **Deploy it publicly:**

```bash
./scripts/deploy-local.sh
```

This gives you a public HTTPS URL anyone can access! See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for details.

## Project Structure

```
interstellar-archive/
├── backend/              # Python blockchain implementation
│   ├── main.py          # FastAPI app entry point
│   ├── blockchain.py    # Core blockchain logic
│   ├── block.py         # Block data structure
│   ├── transaction.py   # Transaction handling
│   ├── mining.py        # Proof of Work
│   ├── network.py       # P2P network simulation
│   ├── crypto.py        # Cryptographic primitives
│   ├── consensus.py     # Consensus mechanisms
│   ├── state.py         # Global state management
│   ├── llm/             # LLM integration
│   │   ├── client.py    # OpenAI-compatible client
│   │   └── errors.py    # Error handling
│   ├── db/              # Database layer
│   │   ├── mongo.py     # MongoDB connection
│   │   └── sessions.py  # Session management
│   ├── characters/      # AI character system
│   │   ├── base.py      # Base persona and controller
│   │   ├── archivist.py # ARCHIVIST character
│   │   └── witness.py   # WITNESS character
│   ├── narrative/       # Narrative state system
│   │   ├── state.py     # Game state models (persistent + session)
│   │   ├── triggers.py  # Story beat trigger system
│   │   └── loop.py      # Loop/iteration reset mechanics
│   ├── filesystem/      # Virtual filesystem and shell
│   │   ├── vfs.py       # Virtual filesystem implementation
│   │   └── commands.py  # Terminal command executor
│   ├── network/         # Network collapse system
│   │   └── collapse.py  # Station death scheduler
│   ├── stealth/         # Stealth mechanics system
│   │   └── monitor.py   # ARCHIVIST monitoring and evasion
│   └── CHARACTER_SYSTEM_README.md  # Character system docs
│
├── frontend/            # Web terminal interface
│   ├── index.html       # Single page app
│   ├── css/             # Styling
│   ├── js/              # JavaScript modules
│   │   ├── modules/
│   │   │   ├── state-manager.js  # Narrative state manager
│   │   │   └── ...      # Other UI modules
│   │   └── main.js      # Application entry point
│   └── assets/          # Fonts and icons
│
├── docs/                # Project documentation
│   ├── overview.md      # Project vision and goals
│   ├── architecture.md  # Technical architecture
│   ├── ui_plan.md       # UI specification
│   ├── claude.md        # Code philosophy
│   └── integration_plans/  # Narrative integration plans
│
├── tests/               # Test files
└── pyproject.toml       # Project configuration
```

## API Endpoints

### Blockchain
- `GET /api/chain` - Get the full blockchain
- `GET /api/chain/block/{hash}` - Get a specific block
- `POST /api/mine` - Mine a new block
- `GET /api/state` - Get current blockchain state

### Transactions & Crypto
- `POST /api/transaction` - Submit a transaction
- `GET /api/mempool` - Get pending transactions
- `POST /api/wallet/generate` - Generate a new wallet (address, public key, private key)

### Network
- `GET /api/network/topology` - Get network topology (nodes and connections)
- `GET /api/network/node/{node_id}` - Get detailed node information
- `POST /api/network/broadcast` - Broadcast transaction through network

### Character System (LLM)
- `POST /api/session/create` - Create new game session
- `GET /api/session/{session_id}` - Get session state
- `POST /api/session/{session_id}/state` - Update game state
- `POST /api/chat/stream` - Streaming chat with characters (SSE)
- `POST /api/chat` - Non-streaming chat
- `POST /api/conversation/reset` - Reset conversation (loop mechanics)

### Narrative State System
- `POST /api/narrative/state/init` - Initialize narrative state for new player
- `POST /api/narrative/state/update` - Update state and evaluate story triggers
- `POST /api/narrative/state/reset` - Manually trigger iteration reset
- `GET /api/narrative/state/export` - Export state for persistence
- `POST /api/narrative/state/import` - Import saved state from IndexedDB
- `GET /api/narrative/state/llm-context` - Get state formatted for LLM characters

### Network Collapse System
- `GET /api/network/collapse/schedule` - Get station death schedule
- `POST /api/network/collapse/check` - Check for new station deaths
- `POST /api/network/collapse/advance-time` - Advance game time
- `GET /api/network/collapse/status` - Get current collapse status

### Stealth Mechanics System
- `GET /api/stealth/monitoring/status` - Get ARCHIVIST monitoring status
- `POST /api/stealth/archivist/busy` - Mark ARCHIVIST as busy (distraction)
- `POST /api/stealth/validation/active` - Set block validation state
- `POST /api/stealth/command/check` - Check if command triggers monitoring
- `GET /api/stealth/evasion/methods` - Get available evasion methods

### Real-time
- `WS /ws` - WebSocket for real-time updates

## Development

### Running with auto-reload

The default command already includes auto-reload:

```bash
uv run python backend/main.py
```

Or use uvicorn directly:

```bash
uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Running tests

```bash
# Blockchain, crypto, and network tests
uv run pytest

# Narrative state system tests
PYTHONPATH=backend uv run python backend/test_narrative_state.py

# Network collapse system tests
uv run pytest backend/test_network_collapse.py

# Stealth mechanics tests
uv run pytest backend/test_stealth_mechanics.py

# Character system tests
uv run python backend/test_character_system.py
```

## Philosophy

This project embraces simplicity and clarity:

- **One concept, one file** - Direct mapping between blockchain concepts and code
- **No unnecessary abstractions** - Classes when needed, functions when sufficient
- **Flat structure** - Easy navigation and understanding
- **Minimal dependencies** - Less to learn, less to break

The code should be invisible - so simple and clear that you think about blockchain concepts, not software architecture.

## Learning Path

1. Start with **Chain Viewer** to understand blocks and hashing
2. Explore **Mining** to see Proof of Work in action
3. Use **Network Monitor** to grasp distributed consensus
4. Experiment with **Crypto Vault** for keys and signatures
5. Dive into **Protocol Engine** for smart contracts


## Documentation

See the `docs/` directory for detailed documentation:

- `overview.md` - Project vision and goals
- `architecture.md` - Technical architecture details
- `ui_plan.md` - UI design specification
- `claude.md` - Code philosophy and guidelines
- `integration_plans/` - Narrative integration implementation plans
  - `00_OVERVIEW.md` - Complete integration roadmap and phase tracking
  - `02_NARRATIVE_STATE.md` - Narrative state system specification
  - `02_IMPLEMENTATION_SUMMARY.md` - Phase 02 implementation details
  - `05_IMPLEMENTATION_SUMMARY.md` - Phase 05 implementation details
  - `06_STEALTH_MECHANICS.md` - Stealth mechanics specification
  - `06_IMPLEMENTATION_SUMMARY.md` - Phase 06 implementation details

### Additional Documentation

- `QUICKSTART_CHARACTER_SYSTEM.md` - LLM character system quick start
- `QUICKSTART_NARRATIVE_STATE.md` - Narrative state system quick start
- `NARRATIVE_STATE_TESTING.md` - Narrative state testing guide
- `backend/CHARACTER_SYSTEM_README.md` - Character system technical details

---

*"In the vastness of space, truth is the only constant. The ledger remembers all."*
