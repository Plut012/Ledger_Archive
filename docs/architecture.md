# Project Structure & Architecture
## Interstellar Archive Terminal

---

## Philosophy: Simplicity Through Constraint

The goal is to make the codebase **so simple that blockchain concepts are obvious**. We achieve this by:

1. **Minimal Layers** - No services, controllers, repositories, factories. Just: Models → Logic → API
2. **Flat is Better** - Few directories, obvious file purposes
3. **No Magic** - No decorators, metaclasses, or clever abstractions
4. **Direct Flow** - Request → Function → Response (traceable in 3 steps)
5. **Single Responsibility** - Each file does ONE thing related to blockchain

---

## The Anti-Pattern to Avoid

**Traditional Web App Structure (Too Complex):**
```
/backend
  /app
    /services
      /blockchain
        blockchain_service.py
        mining_service.py
        consensus_service.py
      /transaction
        transaction_service.py
        validation_service.py
    /controllers
      blockchain_controller.py
      transaction_controller.py
    /repositories
      blockchain_repository.py
    /models
      block_model.py
      transaction_model.py
    /utils
      hash_utils.py
      crypto_utils.py
    /config
      settings.py
```

**Problems:**
- Too many layers between concept and implementation
- Hard to find where blockchain logic actually lives
- Abstraction obscures learning
- Lots of boilerplate, little clarity

---

## Our Simplified Structure

```
interstellar-archive/
│
├── docs/                          # Project documentation
│   ├── PROJECT_OVERVIEW.md
│   ├── UI_SPECIFICATION.md
│   └── PROJECT_STRUCTURE.md
│
├── backend/                       # Python blockchain implementation
│   ├── main.py                    # FastAPI app entry point (30-50 lines)
│   ├── blockchain.py              # Core blockchain logic
│   ├── block.py                   # Block data structure
│   ├── transaction.py             # Transaction structure & validation
│   ├── mining.py                  # Proof of Work implementation
│   ├── network.py                 # P2P network simulation
│   ├── crypto.py                  # Cryptographic primitives
│   ├── consensus.py               # Consensus mechanisms
│   ├── vm.py                      # Smart contract virtual machine
│   └── state.py                   # Global blockchain state manager
│
├── frontend/                      # Web interface
│   ├── index.html                 # Single page app
│   ├── css/
│   │   ├── terminal.css           # Terminal styling
│   │   ├── modules.css            # Module-specific styles
│   │   └── animations.css         # All animations
│   ├── js/
│   │   ├── main.js                # App initialization
│   │   ├── terminal.js            # Terminal UI logic
│   │   ├── websocket.js           # Backend communication
│   │   └── modules/               # One file per learning module
│   │       ├── chain-viewer.js
│   │       ├── network-monitor.js
│   │       ├── crypto-vault.js
│   │       ├── protocol-engine.js
│   │       └── econ-simulator.js
│   └── assets/
│       ├── fonts/
│       └── icons/
│
├── tests/                         # Simple tests (optional initially)
│   ├── test_blockchain.py
│   ├── test_mining.py
│   └── test_consensus.py
│
├── requirements.txt               # Python dependencies
└── README.md                      # Quick start guide
```

**Total Files: ~25-30**
**Total Backend Python Files: ~10**

---

## Backend Architecture: Direct & Obvious

### Principle: "One Concept, One File"

Each Python file maps directly to a blockchain concept:

- **blockchain.py** → The chain itself (list of blocks, validation)
- **block.py** → What a block is (structure, hashing)
- **transaction.py** → How value moves (UTXO or account model)
- **mining.py** → Proof of Work (nonce finding, difficulty)
- **network.py** → Distributed nodes (gossip, sync)
- **crypto.py** → Keys, signatures, hashing
- **consensus.py** → How nodes agree (longest chain, etc.)
- **vm.py** → Smart contract execution (if included)
- **state.py** → Current state holder (singleton pattern)

### No Layers, Just Clear Classes

Instead of Service → Controller → Repository layers, we use **classes when they naturally encapsulate state and behavior**.

```python
# blockchain.py - All blockchain logic in one place

class Blockchain:
    """The complete chain with validation."""
    
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
    
    def add_block(self, block):
        """Add a block if valid."""
        if self.is_valid_block(block):
            self.chain.append(block)
            return True
        return False
    
    def is_valid_chain(self):
        """Validate the entire chain."""
        for i in range(1, len(self.chain)):
            if not self.is_valid_block(self.chain[i], self.chain[i-1]):
                return False
        return True
    
    def is_valid_block(self, block, previous_block=None):
        """Check if a single block is valid."""
        # Simple, clear validation logic
        if previous_block:
            if block.previous_hash != previous_block.hash:
                return False
        if block.hash != block.calculate_hash():
            return False
        return True
```

**Classes are great! We use them liberally for things like Blockchain, Block, Transaction, Network, etc. We just don't add unnecessary abstraction layers on top of them.**

**Use classes when:**
- You have state that belongs together (Blockchain has chain + pending_transactions)
- You have methods that operate on that state (add_block, validate_chain)
- The concept naturally groups data + behavior (Block has data + calculate_hash)

**Don't create:**
- Service classes that just wrap other classes
- Separate validator/factory/repository classes
- Abstract base classes without clear need
- Multiple layers between the API and the actual logic

### State Management: Simple Singleton

```python
# state.py - Single source of truth

class BlockchainState:
    """Global state for the entire application."""
    
    def __init__(self):
        self.blockchain = Blockchain()
        self.network = Network()
        self.mempool = []  # Pending transactions
        self.wallets = {}  # User wallets
    
    def reset(self):
        """Reset to genesis for experimentation."""
        self.__init__()

# Global instance
state = BlockchainState()
```

Everyone imports `state` and uses it directly. No dependency injection, no service locators.

### API Layer: Thin & Direct

```python
# main.py - FastAPI endpoints (the ONLY controller)

from fastapi import FastAPI, WebSocket
from state import state
from mining import mine_block
from transaction import Transaction

app = FastAPI()

@app.get("/api/chain")
def get_chain():
    """Return the full blockchain."""
    return {
        "chain": [block.to_dict() for block in state.blockchain.chain],
        "length": len(state.blockchain.chain)
    }

@app.post("/api/mine")
def mine_new_block():
    """Mine a new block with pending transactions."""
    block = mine_block(
        state.blockchain.chain[-1],
        state.mempool,
        difficulty=4
    )
    state.blockchain.add_block(block)
    state.mempool.clear()
    return {"block": block.to_dict()}

@app.post("/api/transaction")
def create_transaction(tx_data: dict):
    """Add a transaction to mempool."""
    tx = Transaction.from_dict(tx_data)
    if tx.is_valid():
        state.mempool.append(tx)
        return {"status": "added", "tx_id": tx.id}
    return {"status": "invalid"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Real-time updates."""
    await websocket.accept()
    while True:
        # Send state updates
        await websocket.send_json({
            "type": "state_update",
            "height": len(state.blockchain.chain),
            "pending": len(state.mempool)
        })
        await asyncio.sleep(1)
```

**That's it. No controllers, no services. Just endpoints calling functions.**

---

## Data Models: Dataclasses FTW

Use Python dataclasses for simplicity:

```python
# block.py

from dataclasses import dataclass, field
from typing import List
import hashlib
import json
from datetime import datetime

@dataclass
class Block:
    """A single block in the chain."""
    
    index: int
    timestamp: str
    transactions: List[dict]
    previous_hash: str
    nonce: int = 0
    hash: str = field(default="", init=False)
    
    def __post_init__(self):
        """Calculate hash after initialization."""
        if not self.hash:
            self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Generate SHA-256 hash of block contents."""
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create block from dictionary."""
        return cls(
            index=data["index"],
            timestamp=data["timestamp"],
            transactions=data["transactions"],
            previous_hash=data["previous_hash"],
            nonce=data["nonce"]
        )
```

**Clear, self-documenting, no hidden behavior.**

---

## Class and Function Organization: By Concept, Not Layer

Use **classes for entities with state and behavior** (Blockchain, Block, Network, Wallet).
Use **pure functions for stateless operations** (hashing utilities, difficulty calculations).

### Example: Mining Module

```python
# mining.py - Mining logic with both class and functions

import time
from block import Block
from typing import List

class Miner:
    """Handles proof-of-work mining operations."""
    
    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
        self.target = "0" * difficulty
    
    def mine_block(self, previous_block: Block, transactions: List[dict]) -> Block:
        """
        Mine a new block using Proof of Work.
        
        Args:
            previous_block: The last block in the chain
            transactions: List of transactions to include
        
        Returns:
            A mined block with valid proof of work
        """
        new_block = Block(
            index=previous_block.index + 1,
            timestamp=get_timestamp(),
            transactions=transactions,
            previous_hash=previous_block.hash,
            nonce=0
        )
        
        while not new_block.hash.startswith(self.target):
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()
        
        return new_block
    
    def adjust_difficulty(self, blockchain: 'Blockchain', target_time: int = 10):
        """
        Adjust mining difficulty based on recent block times.
        
        Args:
            blockchain: The current blockchain
            target_time: Target time between blocks in seconds
        """
        if len(blockchain.chain) < 10:
            return
        
        recent_blocks = blockchain.chain[-10:]
        time_taken = calculate_time_span(recent_blocks)
        
        if time_taken < target_time * 9:
            self.difficulty += 1  # Too fast, increase
            self.target = "0" * self.difficulty
        elif time_taken > target_time * 11:
            self.difficulty = max(1, self.difficulty - 1)  # Too slow, decrease
            self.target = "0" * self.difficulty

# Pure utility functions
def calculate_time_span(blocks: List[Block]) -> int:
    """Calculate time span between first and last block."""
    # Simple time calculation
    return len(blocks) * 10  # Simplified for now

def get_timestamp() -> str:
    """Get current timestamp in consistent format."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
```

**The Miner class has state (difficulty, target) and behavior (mine, adjust). Pure functions like `get_timestamp()` don't need classes.**

---

## Philosophy on Classes vs Functions

### When to Use Classes

**Use classes when you have state and related behavior:**
- `Blockchain` - has a chain, pending transactions, and methods to manipulate them
- `Block` - has block data and methods to hash/validate itself
- `Transaction` - has transaction data and validation methods
- `Network` - manages nodes and their connections
- `Wallet` - has keys and can sign/verify
- `Miner` - has difficulty settings and mining methods

**Example - Good use of a class:**
```python
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
    
    def add_block(self, block):
        # Method naturally operates on self.chain
        if self.is_valid_block(block):
            self.chain.append(block)
            return True
        return False
```

### When to Use Functions

**Use standalone functions for stateless operations:**
- Utility functions (hashing, formatting)
- Pure calculations (difficulty adjustments, time spans)
- One-off operations that don't need state

**Example - Good use of a function:**
```python
def get_timestamp() -> str:
    """Get current timestamp - no state needed."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

def calculate_merkle_root(transactions: List[dict]) -> str:
    """Pure function - same inputs always give same output."""
    # ... calculation ...
    return root_hash
```

### What to Avoid

**Don't create wrapper classes that add no value:**

```python
# ❌ Bad - unnecessary abstraction
class BlockchainService:
    def __init__(self, blockchain):
        self.blockchain = blockchain
    
    def add_block(self, block):
        return self.blockchain.add_block(block)  # Just passes through!

# ✅ Good - use the Blockchain class directly
blockchain = Blockchain()
blockchain.add_block(new_block)
```

**Don't split related logic into separate classes:**

```python
# ❌ Bad - validation separated from the thing being validated
class Block:
    def __init__(self, ...):
        # just data
        
class BlockValidator:
    def validate(self, block):
        # validation logic

# ✅ Good - validation is part of Block
class Block:
    def __init__(self, ...):
        # data
    
    def is_valid(self):
        # validation logic right here
```

### The Principle

**Use the simplest thing that works:**
- If you need state → class
- If you don't need state → function
- If you're wrapping something for "architecture" → stop, just use the thing directly

This keeps the code natural, readable, and focused on blockchain concepts rather than software patterns.

---

## Frontend Architecture: Module Pattern

```javascript
// js/main.js - App initialization

const App = {
    currentModule: null,
    ws: null,
    
    init() {
        this.ws = WebSocketClient.connect();
        this.setupNavigation();
        this.loadModule('chain-viewer');
    },
    
    loadModule(moduleName) {
        if (this.currentModule) {
            this.currentModule.cleanup();
        }
        this.currentModule = Modules[moduleName];
        this.currentModule.init();
    },
    
    setupNavigation() {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                this.loadModule(e.target.dataset.module);
            });
        });
    }
};

// Start the app
document.addEventListener('DOMContentLoaded', () => App.init());
```

```javascript
// js/modules/chain-viewer.js - Self-contained module

const ChainViewer = {
    blocks: [],
    selectedBlock: null,
    
    init() {
        this.render();
        this.attachEventListeners();
        this.fetchChain();
    },
    
    render() {
        const viewport = document.getElementById('viewport');
        viewport.innerHTML = `
            <div id="chain-visualization"></div>
            <div id="block-details"></div>
        `;
    },
    
    async fetchChain() {
        const response = await fetch('/api/chain');
        const data = await response.json();
        this.blocks = data.chain;
        this.renderChain();
    },
    
    renderChain() {
        // Simple canvas rendering
        const canvas = document.getElementById('chain-visualization');
        const ctx = canvas.getContext('2d');
        // Draw blocks...
    },
    
    cleanup() {
        // Remove event listeners, clear timers
    }
};
```

**Each module is independent, clear, and focused.**

---

## Dependency Management: Minimal

### Backend Requirements

```txt
# requirements.txt

fastapi==0.104.1
uvicorn==0.24.0
websockets==12.0
pydantic==2.5.0

# Optional for advanced features
cryptography==41.0.7  # For proper crypto (if not using hashlib)
```

**That's it. 4-5 packages maximum.**

### Frontend Dependencies

**Zero npm packages.** Vanilla JS, no build step.

Optional:
- Google Fonts (VT323) via CDN
- Nothing else

---

## Configuration: Environment Variables Only

```python
# No config directory, just a simple .env file

# .env
DEBUG=true
HOST=0.0.0.0
PORT=8000
GENESIS_TIMESTAMP=2347-01-01T00:00:00Z
```

Load with:

```python
# main.py
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", "false").lower() == "true"
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))
```

---

## Testing: Simple & Focused

```python
# tests/test_blockchain.py

from backend.blockchain import Blockchain
from backend.block import Block

def test_genesis_block_creation():
    """Genesis block should be created automatically."""
    chain = Blockchain()
    assert len(chain.chain) == 1
    assert chain.chain[0].index == 0
    assert chain.chain[0].previous_hash == "0"

def test_add_valid_block():
    """Valid blocks should be added to chain."""
    chain = Blockchain()
    new_block = Block(
        index=1,
        timestamp="2024-01-01 00:00:00",
        transactions=[],
        previous_hash=chain.chain[0].hash
    )
    assert chain.add_block(new_block) == True
    assert len(chain.chain) == 2

def test_reject_invalid_block():
    """Blocks with wrong previous_hash should be rejected."""
    chain = Blockchain()
    bad_block = Block(
        index=1,
        timestamp="2024-01-01 00:00:00",
        transactions=[],
        previous_hash="wrong_hash"
    )
    assert chain.add_block(bad_block) == False
    assert len(chain.chain) == 1  # Still just genesis
```

**No mocking, no fixtures, just direct function tests.**

---

## Development Workflow

### 1. Start Backend

```bash
cd backend
python main.py
# Or: uvicorn main:app --reload
```

### 2. Open Frontend

```bash
# Open frontend/index.html in browser
# Or serve with Python:
cd frontend
python -m http.server 8080
```

### 3. Make Changes

- Edit Python files → Auto-reload (with uvicorn --reload)
- Edit frontend files → Refresh browser
- No build step, no compilation

---

## Key Architectural Decisions

### ✅ DO: Keep It Simple

1. **Flat module structure** - Easy to find things
2. **Direct method/function calls** - No hidden layers
3. **Single global state** - One source of truth
4. **Classes for state + behavior** - Blockchain, Block, Network, Wallet, etc.
5. **Pure functions for utilities** - Hashing, timestamp formatting, calculations
6. **Dataclasses for simple data** - When you just need structure without much behavior
7. **Explicit over implicit** - No magic, no surprises

### ❌ DON'T: Add Complexity

1. **No service/controller layers** - Classes can call each other directly
2. **No ORMs** - We're not using a database (in-memory only)
3. **No dependency injection frameworks** - Direct imports are fine
4. **No abstract base classes without reason** - Inheritance when it clarifies, not for "architecture"
5. **No factories or builders** - Direct instantiation with `Block(...)` or `Blockchain()`
6. **No middleware chains** - Keep request flow simple
7. **No microservices** - It's all one simple app

---

## Why This Structure Works for Learning

### 1. Concept → Code is Direct

Want to understand mining? Open `mining.py`. That's it.

### 2. Easy to Experiment

Change difficulty in one place, see effects everywhere immediately.

### 3. Traceable Execution

Request comes in → endpoint called → function executes → response sent.
No magic, no hidden service layers.

### 4. Low Cognitive Load

~10 Python files total. You can hold the entire system in your head.

### 5. Invites Modification

Simple code is easy to modify. Want to try a different consensus algorithm? Just replace `consensus.py`.

---

## Example: Complete Flow

**User clicks "Mine Block" button:**

1. **Frontend** (`chain-viewer.js`):
   ```javascript
   fetch('/api/mine', { method: 'POST' })
   ```

2. **Backend** (`main.py`):
   ```python
   @app.post("/api/mine")
   def mine_new_block():
       block = mine_block(...)  # ← Direct call
   ```

3. **Mining Logic** (`mining.py`):
   ```python
   def mine_block(previous_block, transactions, difficulty):
       # ... PoW logic ...
       return new_block
   ```

4. **State Update** (`state.py`):
   ```python
   state.blockchain.add_block(block)
   ```

5. **Response** (back to frontend):
   ```json
   { "block": { ... } }
   ```

**Total files touched: 4**
**Total layers: 0 (just functions calling functions)**
**Lines of code to trace: ~50**

---

## Growth Path

As the project grows, maintain simplicity:

### If a file gets > 300 lines:
Split by concept (e.g., `crypto.py` → `crypto_keys.py`, `crypto_signatures.py`)

### If you need shared utilities:
Create `utils.py` with pure functions (no classes)

### If state management gets complex:
Consider adding `events.py` for event publishing (still simple)

### If you add databases:
Add `storage.py` with direct SQL (no ORM), but only if truly needed

---

## Comparison: Traditional vs Our Approach

### Traditional Web App Way:
```
Transaction request
  → TransactionController.create()
    → TransactionService.validate()
      → TransactionRepository.save()
        → DatabaseModel.insert()
          → ValidationService.check()
            → CryptoService.verify()
```
**7 layers to create a transaction**

### Our Way:
```
Transaction request
  → create_transaction() endpoint
    → Transaction.is_valid()
    → state.mempool.append(tx)
```
**3 steps to create a transaction**

---

## Summary: Simplicity Principles

1. **One file per blockchain concept** - Direct mapping
2. **Classes for state + behavior** - Blockchain, Block, Network, Wallet, etc.
3. **Functions for stateless operations** - Utilities, calculations, formatting
4. **No wrapper/service layers** - Classes call each other directly
5. **Global state is fine** - It's a learning tool, not production
6. **No hidden layers** - Every call is visible
7. **Flat structure** - Easy to navigate
8. **Minimal dependencies** - Less to learn, less to break
9. **No build tools** - Just run the code
10. **Tests are optional** - Start simple, add as needed

**Result:** You spend 90% of your time on blockchain concepts, 10% on infrastructure.

---

*"Simplicity is the ultimate sophistication." - Leonardo da Vinci*

