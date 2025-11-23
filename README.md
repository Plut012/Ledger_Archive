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

## Current Status

**All phases complete!** 🎉 Fully functional blockchain learning platform

- ✅ Phase 0: Project skeleton complete
- ✅ Phase 1: Cryptography implementation complete
- ✅ Phase 2: Crypto Vault UI complete
- ✅ Phase 3: Network Monitor complete
- ✅ Phase 4: Archive Captain Protocol complete

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

### Test Coverage
- ✅ 26 tests passing (4 blockchain + 11 crypto + 11 network)

### Learning Resources
- **Interactive Tutorial**: Open Learning Guide module for the Archive Captain Protocol
- **Reference Manual**: See `docs/LEARNING_GUIDE.md` for comprehensive guide
- **Code Documentation**: Inline comments and docstrings throughout

**New here?** Start with the Archive Captain Protocol tutorial in the Learning Guide module, or read `docs/START_HERE.md`

---

## Quick Start

### Prerequisites

- Python 3.12 or higher
- [UV](https://github.com/astral-sh/uv) package manager

### Installation

1. **Clone the repository** (or navigate to the project directory)

```bash
cd chain
```

2. **Install dependencies with UV**

```bash
uv sync
```

### Running Locally

**Start the server** (serves both backend API and frontend):

```bash
uv run python backend/main.py
```

Then open your browser to: `http://localhost:8000`

That's it! The backend serves the frontend automatically.

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
│   └── state.py         # Global state management
│
├── frontend/            # Web terminal interface
│   ├── index.html       # Single page app
│   ├── css/             # Styling
│   ├── js/              # JavaScript modules
│   └── assets/          # Fonts and icons
│
├── docs/                # Project documentation
│   ├── overview.md      # Project vision and goals
│   ├── architecture.md  # Technical architecture
│   ├── ui_plan.md       # UI specification
│   └── claude.md        # Code philosophy
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
uv run pytest
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

---

*"In the vastness of space, truth is the only constant. The ledger remembers all."*
