# Feedback & Bug Tracker

## 📁 Project Context

**Project**: Interstellar Archive Terminal - A blockchain learning platform with retro terminal UI

**Tech Stack**:
- Backend: Python/FastAPI (serves both API + static frontend)
- Frontend: Vanilla JS (no framework), Web Audio API for sounds
- Philosophy: Simple, direct, minimal dependencies

**Key Files**:
- `backend/main.py` - Unified server (API + static files)
- `frontend/js/main.js` - App initialization, module loading
- `frontend/js/modules/*.js` - Individual modules (home, chain-viewer, crypto-vault, network-monitor, learning-guide)
- `backend/blockchain.py`, `crypto.py`, `network.py` - Core blockchain logic
- `tests/` - Pytest test suite (26 tests)

**Running**:
```bash
uv run python backend/main.py  # Starts server at http://localhost:8000
uv run pytest -v               # Run tests
```

**Documentation**:
- `docs/START_HERE.md` - Quick context for Claude
- `docs/WORKFLOW.md` - Bug fix workflow
- `docs/archive/completed_feedback.md` - Resolved issues archive
- `README.md` - User-facing docs

---

## How to Use This File
1. **Add your feedback below** under "Open Issues"
2. **Use this format**:
   ```

### Example Format:
#### [BUG/TWEAK/FEATURE]
- **Priority**: -
- **Details**: -
- **Steps to reproduce**:
  1. 
  2. 
  3. 
- **Desired behavior**: -

   ```
3. **Run the slash command** (when we create it): `/process-feedback`
4. Claude will:
   - Ask clarifying questions if needed
   - Create a plan with TodoWrite
   - Implement the fix
   - Run tests to verify nothing broke
   - Move the item to "Completed" section

---

## Open Issues

---

### CRITICAL INFRASTRUCTURE: Moving Toward Real Blockchain

*These features are foundational for a production-grade blockchain. They complete the core infrastructure while maintaining our philosophy of simplicity and robustness.*

#### [CRITICAL] Real Cryptographic Signature Verification
- **Priority**: CRITICAL
- **Current State**: `crypto.py:90-136` always returns `True` - signatures aren't actually verified
- **Educational Impact**: Students learn crypto "works" when it doesn't - dangerous misconception
- **Details**:
  - Current implementation: Hash-based signatures that can't be verified without private key
  - Need: Implement ECDSA (Elliptic Curve Digital Signature Algorithm) using standard libraries
  - This is what Bitcoin/Ethereum use - essential for real blockchain
- **Implementation Path**:
  1. Use Python's `cryptography` library (industry standard, well-documented)
  2. Replace hash-based signatures with SECP256k1 curve (Bitcoin's curve)
  3. Update `Wallet.sign()` to use ECDSA signing
  4. Update `Wallet.verify()` to actually verify signatures mathematically
  5. Update all tests to verify signatures truly work
- **Why Critical**: Without this, transactions can be forged. The blockchain is fundamentally insecure.
- **Philosophy Alignment**: Simple to use (same API), robust (actually secure), educational (teaches real crypto)
- **Reference**: backend/crypto.py:90-136

#### [CRITICAL] Fix WebSocket Real-Time Communication
- **Priority**: CRITICAL
- **Current State**: WebSocket implementation broken - infinite blocking loop, no message handling
- **Details**:
  - Current: Sends updates forever, `receive_json()` blocks infinitely on same socket
  - Need: Async loop with timeout, bidirectional message handling
  - Use case: Network Monitor needs real-time transaction propagation visualization
- **Implementation Path**:
  1. Add `asyncio.wait_for()` with timeout for receiving messages
  2. Implement message routing (subscribe to events, broadcast updates)
  3. Send updates only when state changes (new block, new transaction)
  4. Handle client disconnection gracefully
- **Why Critical**: Real-time visualization is core to learning about distributed systems
- **Philosophy Alignment**: Robust error handling, clear async patterns
- **Reference**: backend/main.py:234-254

#### [HIGH] Persistent Storage (Simple Database)
- **Priority**: HIGH
- **Current State**: All state is in-memory - lost on restart
- **Details**:
  - Real blockchains persist to disk
  - Don't need PostgreSQL - use SQLite (single file, built into Python)
  - Or even simpler: JSON file storage for educational purposes
- **Implementation Path**:
  1. Create `storage.py` module with load/save methods
  2. Serialize blockchain to JSON on each new block
  3. Load on startup
  4. Keep it simple: single `blockchain.json` file
- **Why Important**: Students need to understand blockchain permanence
- **Philosophy Alignment**: Minimal dependencies (built-in libraries), simple file format
- **Educational Value**: Shows why "immutable ledger" means "permanent record"

#### [HIGH] Transaction Pool (Mempool) Management
- **Priority**: HIGH
- **Current State**: Mempool exists but lacks proper lifecycle management
- **Details**:
  - Need: Remove mined transactions from mempool
  - Need: Handle transaction conflicts (same sender, insufficient funds)
  - Need: Prioritize transactions (by fee, though we don't have fees yet)
- **Implementation Path**:
  1. Create `mempool.py` module (extract from state.py)
  2. Add `remove_transactions()` method (called after mining)
  3. Add `validate_transaction()` method (check conflicts)
  4. Add transaction expiration (timestamp-based)
- **Why Important**: Core to how real blockchains manage pending transactions
- **Philosophy Alignment**: "One concept, one file" - mempool deserves its own module
- **Reference**: backend/state.py:28, backend/main.py:109

#### [HIGH] Fork Resolution and Chain Reorganization
- **Priority**: HIGH
- **Current State**: Consensus uses "longest chain" but fork validation is stubbed
- **Details**:
  - `consensus.py:39-42` - `validate_fork()` always returns False
  - Need to handle competing chains from different nodes
  - Need "reorg" logic to switch to longer valid chain
- **Implementation Path**:
  1. Implement `validate_fork()` - find common ancestor block
  2. Add `reorganize_chain()` - switch to longer chain, return conflicting transactions to mempool
  3. Add tests for 2-block, 3-block forks
  4. Visualize in Network Monitor (show competing chains)
- **Why Important**: Fork resolution is core to distributed consensus
- **Educational Value**: Students see how decentralized systems reach agreement
- **Philosophy Alignment**: Clear algorithm, observable behavior
- **Reference**: backend/consensus.py:39-42

#### [MEDIUM] Proof of Work Difficulty Adjustment
- **Priority**: MEDIUM
- **Current State**: Mining difficulty is static (4 leading zeros). Adjustment code exists but isn't called.
- **Details**:
  - `mining.py:57-82` has difficulty adjustment logic but it's never used
  - Need: Adjust difficulty based on actual mining time (target 10 seconds per block)
  - Bitcoin adjusts every 2016 blocks; we can adjust every 10 blocks for faster learning
- **Implementation Path**:
  1. Fix `calculate_time_span()` to use real timestamps (not stub multiplication)
  2. Call `adjust_difficulty()` every N blocks during mining
  3. Store difficulty in block header
  4. Show difficulty changes in Chain Viewer
- **Why Important**: Keeps block time consistent as hashpower changes
- **Educational Value**: Shows how Bitcoin maintains 10-minute blocks despite fluctuating miners
- **Philosophy Decision**: Either implement fully or delete (don't leave half-done)
- **Reference**: backend/mining.py:57-82

#### [MEDIUM] Transaction Fees and Miner Incentives
- **Priority**: MEDIUM
- **Current State**: Coinbase rewards exist (50 CREDITS), but no transaction fees
- **Details**:
  - Real blockchains: miners earn block reward + transaction fees
  - Need: Add optional `fee` field to transactions
  - Miners collect fees from transactions in their block
- **Implementation Path**:
  1. Add `fee` field to Transaction class
  2. Modify coinbase transaction to include sum of all fees
  3. Update transaction validation to ensure `amount + fee <= sender_balance`
  4. Show fee economics in UI (higher fees = faster inclusion)
- **Why Important**: Core economic incentive mechanism
- **Educational Value**: Students understand why miners prioritize high-fee transactions
- **Philosophy Alignment**: Simple addition to existing Transaction class
- **Reference**: backend/transaction.py, backend/mining.py

#### [MEDIUM] Merkle Tree for Transaction Verification
- **Priority**: MEDIUM
- **Current State**: Blocks store full transaction list
- **Details**:
  - Real blockchains use Merkle trees for efficient verification
  - Allows "SPV" (Simple Payment Verification) - prove transaction is in block without downloading all transactions
- **Implementation Path**:
  1. Create `merkle.py` module
  2. Implement `build_merkle_tree()` and `get_merkle_root()`
  3. Store merkle root in block header (instead of full transaction list)
  4. Implement `verify_transaction_in_block()` with merkle proof
- **Why Important**: Scalability - light clients can verify without full blockchain
- **Educational Value**: Elegant data structure showing crypto in action
- **Philosophy Alignment**: "One concept, one file" - merkle.py teaches tree-based verification
- **Difficulty**: More advanced - could be "Act 6" content

#### [LOW] Network Peer Discovery and Gossip Protocol
- **Priority**: LOW (current simulation sufficient for learning)
- **Current State**: Network topology is hardcoded (50 nodes in helix)
- **Details**:
  - Real blockchains: nodes discover peers dynamically
  - Current: Good enough for visualization and learning
- **Future Enhancement**: Add `/api/network/peers` endpoint, node connection/disconnection
- **Philosophy Decision**: Current implementation teaches the concept well - defer this

---

### ROBUSTNESS & POLISH

#### [HIGH] Consistent API Error Handling
- **Priority**: HIGH
- **Details**: API returns errors in 3 different formats - confusing for learners
- **Current State**:
  - Some endpoints: `{"error": "...", "available": ..., "required": ...}`
  - Others: `{"status": "invalid", "message": "..."}`
  - No HTTP status codes (returns 200 even on errors)
- **Desired Behavior**:
  ```python
  # Success: HTTP 200
  {"status": "success", "data": {...}}

  # Error: HTTP 400/404/500
  {
    "status": "error",
    "code": "insufficient_funds",  # machine-readable
    "message": "Sender has 50 CREDITS, needs 100 CREDITS",  # human-readable
    "details": {"available": 50, "required": 100}  # optional context
  }
  ```
- **Implementation Path**:
  1. Create `errors.py` with standard error response builder
  2. Update all API endpoints to use consistent format
  3. Add proper HTTP status codes using FastAPI's `HTTPException`
- **Why Important**: Professional API design, easier to debug
- **Reference**: backend/main.py (all endpoints)

#### [MEDIUM] Block Immutability Enforcement
- **Priority**: MEDIUM
- **Details**: Blocks store raw dicts, hash is recalculated constantly - fragile design
- **Current State**: Works but relies on re-hashing; modifying block data makes hash stale
- **Desired Behavior**:
  - Store Transaction objects (not dicts)
  - Make Block dataclass frozen (immutable)
  - Cache hash, never recalculate
- **Implementation Path**:
  1. Update Block to store List[Transaction] instead of List[dict]
  2. Add `frozen=True` to Block dataclass
  3. Remove hash recalculation from validation
- **Why Important**: Enforces immutability at code level
- **Reference**: backend/block.py, backend/blockchain.py

---

### NARRATIVE & UX ENHANCEMENTS

#### [FEATURE]
- **Priority**: high
- **Details**: extension of the chain viewer. create imperiums default node network
- **Desired behavior**: discuss with developer new ideas for how we could create a super cool chain viewer demonstrating the strength and vast size of the imperium. Keeping in mind our philosophy of simple and robust. (side note: even the name: chain viewer could be thematically refactored)

---

## In Progress

<!-- Items Claude is currently working on -->

---

## Completed

**Recent completions are moved to**: `docs/archive/completed_feedback.md`

This keeps the active feedback file clean and focused. Check the archive for full history of resolved issues.

