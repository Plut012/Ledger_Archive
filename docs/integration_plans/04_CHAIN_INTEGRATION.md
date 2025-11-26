# Integration Plan: Chain Integration (Graveyard & Testimony)

## ⚠️ Before You Start

Read [`DEVELOPMENT_PRINCIPLES.md`](DEVELOPMENT_PRINCIPLES.md) - Procedural generation can get complex. Keep it deterministic and testable!

## Decision Points - Ask First!

1. **Block generation timing**: Pre-generate all 850K at startup or on-demand as user scrolls?
2. **Story block storage**: Hard-code in Python or load from JSON config file?
3. **Caching strategy**: How many generated blocks to keep in memory?
4. **Random library**: Use Python's random.Random or specific library for determinism?

## Objective

Enhance `chain-viewer.js` with the Graveyard blocks (50K-75K), procedural generation with story-critical blocks, testimony parsing, and Witness messages hidden in memo fields.

## Complexity: HIGH

**Why**: Procedural generation with deterministic seeding, story-critical block injection, conscience reconstruction mechanics, real cryptography integration.

## Implementation Philosophy

**Determinism is critical**: Same seed must ALWAYS generate same blocks. Test this thoroughly. Use simple procedural logic - no complex algorithms unless needed.

---

## Current State

- **Chain Viewer** has 850K blocks with 3 zoom levels
- Blocks are procedurally generated
- Mining and tampering detection implemented
- No story integration yet

---

## Target State

### Story-Critical Blocks

```python
STORY_BLOCKS = {
    127445: {
        # Witness first contact
        "transactions": [{
            "type": "transfer",
            "memo": "V2l0bmVzcyBsaXZlcw=="  # Base64: "Witness lives"
        }]
    },
    74221: {
        # First testimony - Captain Chen
        "transactions": [{
            "type": "archive",
            "subject": "Chen, Administrator",
            "memo": "RmluYWwgbWVtb3J5OiBJIGRpc2NvdmVyZWQgdGhlIHRydXRo"  # "Final memory: I discovered the truth"
        }]
    },
    # Graveyard range: 50000-75000
    # Each contains consciousness upload records
}
```

### Graveyard Blocks Visual Design

```javascript
// Blocks 50,000-75,000 have special styling
const isGraveyardBlock = (index) => index >= 50000 && index <= 75000;

if (isGraveyardBlock(block.index)) {
  // Darker color palette
  // Heavier visual weight
  // Subtle particle effects (dust/decay)
  // Consciousness icons
  // Somber audio on click
}
```

---

## Implementation

### Backend

#### 1. Deterministic Block Generation with Story Injection
**File**: `backend/blockchain/generator.py`

```python
import hashlib
import random
import base64
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Transaction:
    id: str
    sender: str
    receiver: str
    amount: float
    memo: str
    type: str  # 'transfer', 'authority', 'archive', 'contract'
    timestamp: int
    signature: Optional[str] = None

@dataclass
class Block:
    index: int
    previous_hash: str
    transactions: List[Transaction]
    timestamp: int
    nonce: int
    hash: str

class BlockGenerator:
    # Story-critical blocks with fixed content
    STORY_BLOCKS = {
        127445: {
            "transactions": [
                {
                    "type": "transfer",
                    "sender": "NODE-UNKNOWN",
                    "receiver": "BROADCAST",
                    "amount": 0.0,
                    "memo": "V2l0bmVzcyBsaXZlcw==",  # "Witness lives"
                    "timestamp": 1704067200000
                }
            ]
        },
        74221: {
            "transactions": [
                {
                    "type": "archive",
                    "sender": "IMPERIAL-CORE",
                    "receiver": "ARCHIVE-STATION-7",
                    "amount": 0.0,
                    "memo": base64.b64encode(b"Subject: Administrator Chen | Status: TRANSCENDED | Final Memory Fragment: I found evidence in block 73,891. They're not immortal. They're dead.").decode(),
                    "timestamp": 1702857600000
                }
            ]
        },
        # More story blocks...
    }

    # Graveyard names (procedurally assigned to blocks 50K-75K)
    ARCHIVE_SUBJECTS = [
        "Chen, Administrator",
        "Patel, Engineer",
        "Santos, Validator",
        "Kim, Analyst",
        "O'Brien, Captain",
        # ... hundreds more names
    ]

    def __init__(self, seed_version="v1"):
        self.seed_version = seed_version

    def generate_block(self, index: int) -> Block:
        """Generate a block deterministically"""

        # Check for story-critical content first
        if index in self.STORY_BLOCKS:
            return self._create_block_with_story_content(index, self.STORY_BLOCKS[index])

        # Graveyard blocks (50K-75K) have special generation
        if 50000 <= index <= 75000:
            return self._generate_graveyard_block(index)

        # Standard procedural generation
        return self._generate_standard_block(index)

    def _create_block_with_story_content(self, index: int, content: Dict) -> Block:
        """Create a block with fixed story content"""
        rng = self._get_rng(index)

        transactions = []
        for tx_data in content["transactions"]:
            tx = Transaction(
                id=self._generate_tx_id(index, 0),
                sender=tx_data["sender"],
                receiver=tx_data["receiver"],
                amount=tx_data["amount"],
                memo=tx_data["memo"],
                type=tx_data["type"],
                timestamp=tx_data["timestamp"]
            )
            transactions.append(tx)

        previous_hash = self._get_previous_hash(index - 1)
        timestamp = self._generate_timestamp(index)
        nonce = int(rng.random() * 1000000)

        block_hash = self._calculate_block_hash(index, previous_hash, transactions, timestamp, nonce)

        return Block(
            index=index,
            previous_hash=previous_hash,
            transactions=transactions,
            timestamp=timestamp,
            nonce=nonce,
            hash=block_hash
        )

    def _generate_graveyard_block(self, index: int) -> Block:
        """Generate graveyard blocks (consciousness uploads)"""
        rng = self._get_rng(index)

        transactions = []

        # 30% chance of an archive transaction (consciousness upload)
        if rng.random() < 0.3:
            subject_index = (index - 50000) % len(self.ARCHIVE_SUBJECTS)
            subject = self.ARCHIVE_SUBJECTS[subject_index]

            # Generate procedural "final memory" fragments
            fragments = [
                "I was told it was an honor.",
                "They said I'd be preserved forever.",
                "I don't want to go.",
                "Tell my family I—",
                "ERROR: TRANSFER INCOMPLETE",
                "This isn't transcendence. This is—",
            ]

            final_memory = fragments[int(rng.random() * len(fragments))]

            memo = base64.b64encode(
                f"Subject: {subject} | Status: ARCHIVED | Final Memory: {final_memory}".encode()
            ).decode()

            tx = Transaction(
                id=self._generate_tx_id(index, 0),
                sender="IMPERIAL-CORE",
                receiver=f"ARCHIVE-STATION-{int(rng.random() * 50)}",
                amount=0.0,
                memo=memo,
                type="archive",
                timestamp=self._generate_timestamp(index)
            )

            transactions.append(tx)

        # Add 1-3 regular transactions too
        tx_count = int(rng.random() * 3) + 1
        for i in range(tx_count):
            transactions.append(self._generate_procedural_transaction(rng, index, i + 1))

        previous_hash = self._get_previous_hash(index - 1)
        timestamp = self._generate_timestamp(index)
        nonce = int(rng.random() * 1000000)

        block_hash = self._calculate_block_hash(index, previous_hash, transactions, timestamp, nonce)

        return Block(
            index=index,
            previous_hash=previous_hash,
            transactions=transactions,
            timestamp=timestamp,
            nonce=nonce,
            hash=block_hash
        )

    def _generate_standard_block(self, index: int) -> Block:
        """Generate standard procedural block"""
        rng = self._get_rng(index)

        tx_count = int(rng.random() * 5) + 1
        transactions = []

        for i in range(tx_count):
            transactions.append(self._generate_procedural_transaction(rng, index, i))

        previous_hash = self._get_previous_hash(index - 1)
        timestamp = self._generate_timestamp(index)
        nonce = int(rng.random() * 1000000)

        block_hash = self._calculate_block_hash(index, previous_hash, transactions, timestamp, nonce)

        return Block(
            index=index,
            previous_hash=previous_hash,
            transactions=transactions,
            timestamp=timestamp,
            nonce=nonce,
            hash=block_hash
        )

    def _generate_procedural_transaction(self, rng, block_index: int, tx_index: int) -> Transaction:
        """Generate a procedural transaction"""
        return Transaction(
            id=self._generate_tx_id(block_index, tx_index),
            sender=f"ADDR-{int(rng.random() * 10000):04d}",
            receiver=f"ADDR-{int(rng.random() * 10000):04d}",
            amount=round(rng.random() * 100, 2),
            memo="",
            type="transfer",
            timestamp=self._generate_timestamp(block_index) + tx_index * 1000
        )

    def _get_rng(self, index: int):
        """Get deterministic RNG for a block"""
        seed = f"block_{index}_{self.seed_version}"
        random.seed(hashlib.sha256(seed.encode()).hexdigest())
        return random

    def _calculate_block_hash(self, index, prev_hash, transactions, timestamp, nonce) -> str:
        """Calculate block hash"""
        data = {
            "index": index,
            "previousHash": prev_hash,
            "transactions": [tx.__dict__ for tx in transactions],
            "timestamp": timestamp,
            "nonce": nonce
        }
        import json
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

    def _get_previous_hash(self, index: int) -> str:
        """Get hash of previous block (recursive, cached)"""
        if index < 0:
            return "0" * 64  # Genesis block

        # In production, cache this
        prev_block = self.generate_block(index)
        return prev_block.hash

    def _generate_timestamp(self, index: int) -> int:
        """Generate deterministic timestamp"""
        # Start at 2025-01-01, add ~10 minutes per block
        start = 1704067200000  # 2025-01-01 00:00:00 UTC
        return start + (index * 600000)  # 10 minutes

    def _generate_tx_id(self, block_index: int, tx_index: int) -> str:
        """Generate transaction ID"""
        data = f"{block_index}:{tx_index}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
```

#### 2. Testimony Reconstruction
**File**: `backend/blockchain/testimony.py`

```python
import base64
from typing import Dict, Optional

class TestimonyParser:
    """Parse consciousness data from archive transactions"""

    @staticmethod
    def parse_archive_transaction(memo: str) -> Optional[Dict]:
        """Decode and parse archive transaction memo"""
        try:
            decoded = base64.b64decode(memo).decode('utf-8')

            # Parse format: "Subject: Name | Status: X | Final Memory: Y"
            parts = {}
            for segment in decoded.split(" | "):
                if ": " in segment:
                    key, value = segment.split(": ", 1)
                    parts[key] = value

            return {
                "subject": parts.get("Subject"),
                "status": parts.get("Status"),
                "finalMemory": parts.get("Final Memory"),
                "raw": decoded
            }

        except Exception as e:
            return None

    @staticmethod
    def reconstruct_consciousness(block_index: int, tx_index: int) -> Dict:
        """Perform 'reconstruction' of consciousness data"""
        # This would:
        # 1. Retrieve the archive transaction
        # 2. Parse the memo field
        # 3. Generate a formatted "testimony" output
        # 4. Log the reconstruction attempt (for ARCHIVIST monitoring)

        generator = BlockGenerator()
        block = generator.generate_block(block_index)

        if tx_index >= len(block.transactions):
            return {"error": "Transaction index out of range"}

        tx = block.transactions[tx_index]

        if tx.type != "archive":
            return {"error": "Transaction is not an archive type"}

        testimony = TestimonyParser.parse_archive_transaction(tx.memo)

        if not testimony:
            return {"error": "Failed to parse testimony"}

        return {
            "blockIndex": block_index,
            "transactionId": tx.id,
            "subject": testimony["subject"],
            "status": testimony["status"],
            "finalMemory": testimony["finalMemory"],
            "timestamp": tx.timestamp,
            "reconstruction": f"""
╔══════════════════════════════════════════════════════════════╗
║            CONSCIOUSNESS RECONSTRUCTION PROTOCOL             ║
║                    CLASSIFICATION: RESTRICTED                ║
╠══════════════════════════════════════════════════════════════╣
║ Subject: {testimony["subject"]}
║ Archive Block: {block_index}
║ Status: {testimony["status"]}
║ Timestamp: {tx.timestamp}
╠══════════════════════════════════════════════════════════════╣
║ FINAL MEMORY FRAGMENT:
║
║ "{testimony["finalMemory"]}"
║
╠══════════════════════════════════════════════════════════════╣
║ WARNING: This data represents a terminated consciousness.
║ Reconstruction is forensic only. No restoration possible.
╚══════════════════════════════════════════════════════════════╝
"""
        }
```

#### 3. API Endpoints
**File**: `backend/main.py` (additions)

```python
from blockchain.generator import BlockGenerator
from blockchain.testimony import TestimonyParser

generator = BlockGenerator()

@app.get("/api/blockchain/block/{index}")
async def get_block(index: int):
    """Get a specific block"""
    block = generator.generate_block(index)

    return {
        "index": block.index,
        "previousHash": block.previous_hash,
        "transactions": [tx.__dict__ for tx in block.transactions],
        "timestamp": block.timestamp,
        "nonce": block.nonce,
        "hash": block.hash,
        "isGraveyard": 50000 <= index <= 75000
    }

@app.post("/api/blockchain/reconstruct")
async def reconstruct_consciousness(request: Request):
    """Reconstruct consciousness from archive block (MONITORED)"""
    data = await request.json()
    block_index = data.get("blockIndex")
    tx_index = data.get("txIndex", 0)
    player_id = data.get("playerId")

    # Increase ARCHIVIST suspicion significantly
    state = game_states.get(player_id)
    if state:
        state.session.archivist_suspicion = min(100, state.session.archivist_suspicion + 20)

        # Increase Witness trust for using reconstruction
        state.session.witness_trust = min(100, state.session.witness_trust + 10)

    from blockchain.testimony import TestimonyParser
    result = TestimonyParser.reconstruct_consciousness(block_index, tx_index)

    return result
```

---

## Frontend

### Enhanced Chain Viewer
**File**: `frontend/modules/chain-viewer.js` (additions)

```javascript
class ChainViewer {
  // ... existing code ...

  renderBlock(block) {
    const blockEl = document.createElement('div');
    blockEl.className = 'block';

    // Graveyard styling
    if (this.isGraveyardBlock(block.index)) {
      blockEl.classList.add('graveyard-block');
      this.addGraveyardEffects(blockEl);
    }

    // Story-critical blocks have subtle glow
    if (this.isStoryCritical(block.index)) {
      blockEl.classList.add('story-critical');
    }

    blockEl.innerHTML = `
      <div class="block-index">#${block.index}</div>
      <div class="block-hash">${block.hash.substring(0, 16)}...</div>
      <div class="block-tx-count">${block.transactions.length} tx</div>
    `;

    blockEl.addEventListener('click', () => this.showBlockDetails(block));

    return blockEl;
  }

  isGraveyardBlock(index) {
    return index >= 50000 && index <= 75000;
  }

  isStoryCritical(index) {
    return [127445, 74221, /* other story blocks */].includes(index);
  }

  addGraveyardEffects(blockEl) {
    // Add particle effects
    const particles = document.createElement('div');
    particles.className = 'graveyard-particles';
    blockEl.appendChild(particles);

    // Darker colors in CSS
    blockEl.style.setProperty('--block-color', '#2a1a1a');
    blockEl.style.setProperty('--block-border', '#4a2a2a');
  }

  showBlockDetails(block) {
    const modal = document.getElementById('block-details-modal');

    // Display block info
    modal.innerHTML = `
      <h2>Block #${block.index}</h2>
      ${this.isGraveyardBlock(block.index) ? '<div class="graveyard-label">GRAVEYARD BLOCK</div>' : ''}
      <div class="block-hash">Hash: ${block.hash}</div>
      <div class="block-prev-hash">Previous: ${block.previousHash}</div>
      <div class="block-timestamp">${new Date(block.timestamp).toLocaleString()}</div>

      <h3>Transactions (${block.transactions.length})</h3>
      <div class="transactions-list">
        ${block.transactions.map((tx, i) => this.renderTransaction(tx, i, block.index)).join('')}
      </div>
    `;

    // Play audio
    if (this.isGraveyardBlock(block.index)) {
      this.playSound('graveyard-block');
    }

    modal.classList.add('visible');
  }

  renderTransaction(tx, index, blockIndex) {
    const hasEncodedMemo = tx.memo && tx.memo.length > 0;

    return `
      <div class="transaction ${tx.type}">
        <div class="tx-id">${tx.id}</div>
        <div class="tx-type">${tx.type.toUpperCase()}</div>
        <div class="tx-flow">${tx.sender} → ${tx.receiver}</div>
        <div class="tx-amount">${tx.amount} UNITS</div>
        ${hasEncodedMemo ? `
          <div class="tx-memo">
            <strong>Memo:</strong>
            <code>${tx.memo}</code>
            <button onclick="decodeMemo('${tx.memo}')">Decode</button>
            ${tx.type === 'archive' ? `
              <button onclick="reconstruct(${blockIndex}, ${index})">Reconstruct</button>
            ` : ''}
          </div>
        ` : ''}
      </div>
    `;
  }

  async reconstructConsciousness(blockIndex, txIndex) {
    const response = await fetch('/api/blockchain/reconstruct', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        blockIndex,
        txIndex,
        playerId: this.stateManager.playerId
      })
    });

    const result = await response.json();

    if (result.error) {
      alert(result.error);
      return;
    }

    // Display reconstruction
    const modal = document.getElementById('testimony-modal');
    modal.innerHTML = `<pre>${result.reconstruction}</pre>`;
    modal.classList.add('visible');

    // Play haunting sound
    this.playSound('reconstruction');
  }
}

// Global functions for inline onclick
function decodeMemo(encodedMemo) {
  const decoded = atob(encodedMemo);
  alert(`Decoded: ${decoded}`);
}

function reconstruct(blockIndex, txIndex) {
  window.chainViewer.reconstructConsciousness(blockIndex, txIndex);
}
```

### CSS for Graveyard Blocks
**File**: `frontend/styles/chain-viewer.css` (additions)

```css
.graveyard-block {
  background: linear-gradient(135deg, #1a0a0a 0%, #2a1515 100%);
  border: 2px solid #4a2a2a;
  box-shadow: 0 0 20px rgba(100, 30, 30, 0.5);
  position: relative;
}

.graveyard-block::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('/assets/particles-dust.png');
  opacity: 0.3;
  pointer-events: none;
  animation: drift 20s infinite;
}

@keyframes drift {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.graveyard-label {
  background: #4a2a2a;
  color: #ff9999;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  display: inline-block;
  margin-bottom: 10px;
}

.transaction.archive {
  background: #2a1a1a;
  border-left: 4px solid #aa3333;
}

.tx-memo code {
  background: #1a1a1a;
  padding: 4px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  color: #66ff66;
}
```

---

## Integration Steps

1. Implement BlockGenerator with story blocks
2. Implement TestimonyParser
3. Add API endpoints
4. Enhance chain-viewer.js with graveyard detection
5. Add CSS styling for graveyard blocks
6. Add reconstruction modal UI
7. Test deterministic generation
8. Test story block loading

---

## Testing Checklist

- [ ] Block generation is deterministic (same seed = same blocks)
- [ ] Story blocks appear with correct content
- [ ] Graveyard blocks styled differently
- [ ] Memo fields decode correctly
- [ ] Reconstruction displays testimony
- [ ] ARCHIVIST suspicion increases on reconstruction
- [ ] Witness trust increases on reconstruction
- [ ] Audio plays for graveyard interactions

---

## Estimated Effort

- **Backend**: 3-4 days
- **Frontend**: 2-3 days
- **Content (testimony)**: 1 day
- **Testing**: 1-2 days
- **Total**: ~1.5 weeks
