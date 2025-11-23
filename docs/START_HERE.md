# Quick Context for Claude

## What This Is

**Interstellar Archive Terminal** - A blockchain learning platform with a retro terminal UI.

- **Purpose:** Teach blockchain concepts through hands-on exploration
- **Theme:** Space archive stations maintaining humanity's distributed ledger
- **Style:** Minimal, clean code that prioritizes learning and clarity

---

## Current State

```
Phase 0: ✅ Complete - Project skeleton
Phase 1: ✅ Complete - Cryptography implementation
Phase 2: ✅ Complete - Crypto Vault UI
Phase 3: ✅ Complete - Network Monitor
Phase 4: ✅ Complete - Archive Captain Protocol (narrative tutorial)
Phase 5: ✅ Complete - Balance Tracking & Economic Incentives
```

### What Works Now

✅ Basic blockchain with blocks and chain validation
✅ Proof of Work mining
✅ REST API + WebSocket
✅ Terminal UI framework
✅ Chain Viewer module (fully functional)
✅ Crypto Vault module (fully functional)
✅ Network Monitor module (fully functional)
✅ Wallet key pair generation
✅ Transaction signing and verification
✅ Transaction creation and broadcasting
✅ Digital signatures with SHA-256
✅ Address derivation from public keys
✅ Client-side transaction signing
✅ Transaction history (pending + confirmed)
✅ Wallet export functionality
✅ Network topology visualization
✅ P2P node simulation (4 nodes in mesh)
✅ Transaction propagation animation
✅ Node details and status tracking
✅ Archive Captain Protocol (narrative tutorial)
✅ Learning Guide companion documentation
✅ Interactive 5-act tutorial system
✅ Typewriter text effects and animations
✅ Warm analog synth audio effects (Web Audio API)

### What Works Now (Phase 5)

✅ Account balance tracking
✅ Transaction validation with funds
✅ Mining rewards (50 CREDITS per block)
✅ Coinbase transactions
✅ Balance display in Crypto Vault
✅ Insufficient funds prevention
✅ Economic concepts in tutorial

### Recent Improvements

✅ Act 1 tamper demo: AXIOM demonstrates (no player interaction required)
✅ Emoji removal for cleaner aesthetic
✅ Tutorial flag system for UI components

### Optional Future Enhancements

💡 Act 5 fork split mechanic (design discussion required - see act5_fork_extension.md)
💡 Protocol Engine (smart contracts)
💡 Economic Simulator (DeFi primitives)
💡 Advanced consensus mechanisms
💡 Network partition simulation
💡 Transaction fees and gas
💡 Merkle trees for efficiency

---

## Phase 1: ✅ COMPLETED

**Cryptographic operations implemented successfully**

### What Was Implemented
1. ✅ Wallet key pair generation (private key, public key, address)
2. ✅ Digital signature creation using SHA-256
3. ✅ Signature verification
4. ✅ Transaction signing with `Transaction.sign(wallet)`
5. ✅ Transaction validation with signature verification
6. ✅ API endpoint: `POST /api/wallet/generate`
7. ✅ Comprehensive test suite (11 tests, all passing)

### Files Modified
```
backend/crypto.py         ✅ Wallet class fully implemented
backend/transaction.py    ✅ Added sign() and updated is_valid()
backend/main.py           ✅ Added wallet generation endpoint
tests/test_crypto.py      ✅ 11 comprehensive tests
```

### Implementation Details
📄 See: `docs/phase1_plan.md` for original plan

---

## Phase 2: ✅ COMPLETED

**Crypto Vault UI module built successfully**

### What Was Implemented
1. ✅ Interactive wallet management UI
2. ✅ Wallet key generation (Generate Keypair button)
3. ✅ Transaction creation form with validation
4. ✅ Client-side transaction signing (SHA-256)
5. ✅ Transaction broadcasting to mempool
6. ✅ Transaction history (pending + confirmed)
7. ✅ Wallet export to JSON file
8. ✅ API endpoint: `POST /api/wallet/generate`
9. ✅ API endpoint: `GET /api/mempool`

### Files Modified
```
frontend/js/modules/crypto-vault.js  ✅ Complete implementation (366 lines)
backend/main.py                      ✅ Added wallet & mempool endpoints
```

### Implementation Details
📄 See: `docs/phase2_plan.md` for full details

---

## Phase 3: ✅ COMPLETED

**Network Monitor module built successfully**

### What Was Implemented
1. ✅ Network topology visualization with Canvas 2D
2. ✅ 4-node mesh topology (Earth, Mars, Jupiter, Alpha Centauri)
3. ✅ Interactive node selection and details panel
4. ✅ Transaction propagation animation
5. ✅ BFS-based broadcast simulation
6. ✅ Activity logging
7. ✅ API endpoints: `/api/network/topology`, `/api/network/node/{id}`, `/api/network/broadcast`

### Files Modified
```
backend/network.py                   ✅ Enhanced with full Network class
backend/state.py                     ✅ Added network instance
backend/main.py                      ✅ Added 3 network endpoints
frontend/js/modules/network-monitor.js  ✅ Complete implementation (325 lines)
```

### Implementation Details
📄 See: `docs/phase3_plan.md` for full details

---

## Phase 4: ✅ COMPLETED

**Archive Captain Protocol built successfully**

### What Was Implemented
1. ✅ Complete 5-act narrative tutorial system
2. ✅ Typewriter text effects and animations
3. ✅ Action validation and progress tracking
4. ✅ Interactive module integration
5. ✅ LocalStorage save/load system
6. ✅ Comprehensive Learning Guide documentation (800+ lines)
7. ✅ Tutorial overlay UI with progress indicators

### Files Created/Modified
```
frontend/js/modules/learning-guide.js  ✅ Complete narrative engine (894 lines)
frontend/css/tutorial.css              ✅ Tutorial styling (351 lines)
docs/LEARNING_GUIDE.md                 ✅ Companion documentation (801 lines)
frontend/index.html                    ✅ Added tutorial integration
frontend/js/main.js                    ✅ Module registration + global state
```

### The Five Acts
1. **Act 1: AWAKENING** - Blocks, Hashing, Immutability
2. **Act 2: COMPUTATIONAL LOCKS** - Proof of Work, Mining
3. **Act 3: CREDENTIALS** - Keys, Signatures, Identity
4. **Act 4: RELAY STATIONS** - Distributed Networks, Propagation
5. **Act 5: TRUTH PROTOCOL** - Consensus, Attack Resistance

### Implementation Details
📄 See: `docs/phase4_plan.md` for full details

---

## Phase 5: ✅ COMPLETED

**Balance Tracking & Economic Incentives built successfully**

### What Was Implemented
1. ✅ Account balance tracking system (Ledger class)
2. ✅ Transaction validation with balance checking
3. ✅ Block rewards for miners (50 CREDITS per block)
4. ✅ Coinbase transactions (special TX type)
5. ✅ Balance display in Crypto Vault UI
6. ✅ Coinbase highlighting in Chain Viewer
7. ✅ Tutorial updates with economic concepts
8. ✅ 27 comprehensive tests (all passing)

### Files Modified
```
backend/constants.py           ✅ Economic constants
backend/ledger.py              ✅ Balance tracking (165 lines)
backend/transaction.py         ✅ Coinbase support
backend/mining.py              ✅ Create rewards
backend/state.py               ✅ Ledger integration
backend/main.py                ✅ Balance API endpoints
frontend/js/modules/crypto-vault.js   ✅ Balance display
frontend/js/modules/chain-viewer.js   ✅ Coinbase display
frontend/js/modules/learning-guide.js ✅ Tutorial updates
tests/test_ledger.py           ✅ 9 tests
tests/test_coinbase.py         ✅ 10 tests
tests/test_balance_validation.py ✅ 8 tests
```

### Implementation Details
📄 See: `docs/phase5_plan.md` for plan
📄 See: `docs/phase5_handoff.md` for completion notes

---

## Code Philosophy

**Read:** `docs/claude.md` for full philosophy

**Key Principles:**
- **Simple** - Direct implementations, no clever tricks
- **Flat** - One concept = one file, minimal nesting
- **Clear** - Code should be obvious at a glance
- **Classes for state** - Use when you have state + behavior together
- **Functions for utilities** - Use for stateless operations
- **No layers** - Direct calls, no service/controller/repository patterns

**Example:**
```python
# ✅ Good - Direct and clear
class Wallet:
    def __init__(self):
        self.private_key = ""
        self.public_key = ""

    def generate_keypair(self):
        # Generate keys here
        pass

# ❌ Avoid - Unnecessary abstraction
class WalletService:
    def __init__(self, wallet):
        self.wallet = wallet

    def generate_keypair(self):
        return self.wallet.generate_keypair()  # Just wrapping!
```

---

## Project Structure

```
interstellar-archive/
├── backend/              # Python blockchain implementation
│   ├── main.py          # FastAPI entry point
│   ├── blockchain.py    # Chain logic & validation
│   ├── block.py         # Block structure & hashing
│   ├── transaction.py   # Transaction handling
│   ├── mining.py        # Proof of Work
│   ├── crypto.py        # Wallet & signatures
│   ├── network.py       # P2P simulation (✅ Complete)
│   ├── consensus.py     # Consensus logic (stub)
│   └── state.py         # Global state singleton
│
├── frontend/            # Terminal UI
│   ├── index.html
│   ├── css/
│   ├── js/
│   │   ├── main.js
│   │   └── modules/
│   │       ├── chain-viewer.js      (✅ Complete)
│   │       ├── crypto-vault.js      (✅ Complete)
│   │       ├── network-monitor.js   (✅ Complete)
│   │       ├── learning-guide.js    (✅ Complete - 894 lines)
│   │       ├── protocol-engine.js   (⏸️ Placeholder)
│   │       └── econ-simulator.js    (⏸️ Placeholder)
│   └── assets/
│
├── tests/               # Test files
│   ├── test_blockchain.py  (✅ 4 tests passing)
│   ├── test_crypto.py      (✅ 11 tests passing)
│   └── test_network.py     (✅ 11 tests passing)
│
└── docs/                # Documentation
    ├── overview.md          # Project vision
    ├── architecture.md      # Technical details
    ├── claude.md            # Code philosophy
    ├── ui_plan.md           # UI specification
    ├── LEARNING_GUIDE.md    # Comprehensive blockchain guide
    ├── phase1_plan.md       # Cryptography (completed)
    ├── phase2_plan.md       # Crypto Vault (completed)
    ├── phase3_plan.md       # Network Monitor (completed)
    ├── phase4_plan.md       # Archive Captain Protocol (completed)
    ├── phase1_handoff.md    # Phase 1 completion notes
    ├── phase2_handoff.md    # Phase 2 completion notes
    ├── phase3_handoff.md    # Phase 3 completion notes
    └── IMPLEMENTATION_ROADMAP.md
```

---

## Quick Commands

### Setup
```bash
uv sync                    # Install dependencies
```

### Development
```bash
uv run python backend/main.py     # Start server (serves both backend + frontend)
# Then open http://localhost:8000 in your browser
```

### Testing
```bash
uv run pytest                     # Run all tests
uv run pytest tests/test_crypto.py  # Run specific test
uv run pytest -v                  # Verbose output
```

### Check what's installed
```bash
uv pip list
```

---

## Dependencies

**Core dependencies (in pyproject.toml):**
- fastapi>=0.104.1
- uvicorn>=0.24.0
- websockets>=12.0
- pydantic>=2.5.0
- pytest (dev dependency)

**Built-in modules used:**
- `hashlib` - Cryptographic hashing
- `secrets` - Secure random number generation
- `json` - Data serialization
- `dataclasses` - Clean data structures

---

## Need More Context?

- **Project vision:** `docs/overview.md`
- **Architecture details:** `docs/architecture.md`
- **Code philosophy:** `docs/claude.md`
- **All phases:** `docs/IMPLEMENTATION_ROADMAP.md`
- **Phase 1 (completed):** `docs/phase1_plan.md`
- **Phase 2 (completed):** `docs/phase2_plan.md`
- **Phase 3 (next):** `docs/phase3_plan.md`

---

## Questions to Ask

Before starting Phase 3, verify:
- [ ] Have you read `docs/phase3_plan.md`?
- [ ] Do you understand the P2P network architecture?
- [ ] Are you clear on how to simulate network behavior?
- [ ] Do you know which frontend/backend files to modify?

If unclear, ask! Better to clarify than to build wrong.

---

**Let's build something simple, clear, and educational.** 🚀

*"In the vastness of space, truth is the only constant. The ledger remembers all."*
