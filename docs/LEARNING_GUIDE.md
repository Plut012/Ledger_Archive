# The Archive Captain's Manual
## A Comprehensive Guide to Blockchain Technology

*"In the vastness of space, truth is the only constant. The ledger remembers all."*

---

## Introduction

Welcome, Archive Captain.

This manual serves as your comprehensive reference for understanding and operating the Interstellar Ledger Archive - humanity's permanent, distributed record spanning the solar system.

Whether you've completed the Archive Captain Protocol or are diving directly into the technical details, this guide will help you understand the fundamental concepts that keep our distributed truth secure across the void.

### Who You Are

You are an **Archive Captain** - one of the elite operators entrusted with maintaining the integrity of humanity's permanent ledger. Your mission is to ensure that truth persists, even as nodes go dark and adversaries attempt to rewrite history.

### What the Archive Is

The Interstellar Ledger Archive is a **blockchain** - a distributed, cryptographically-sealed chain of records maintained across relay stations spanning from Earth to Alpha Centauri. No single entity controls it. No central authority can alter it. The math guarantees its integrity.

---

## Part 1: Fundamentals

### Chapter 1: Archive Blocks

#### The Block Structure

Every entry in the archive is stored in a **block** - a cryptographically-sealed container of data.

Each block contains:
- **Data**: The actual information being recorded (transactions, messages, state changes)
- **Timestamp**: When the block was created
- **Previous Hash**: The cryptographic fingerprint of the block before it
- **Nonce**: A number used in the sealing process (Proof of Work)
- **Hash**: This block's own cryptographic fingerprint

**Code Reference:**
```python
# backend/block.py

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
```

#### Hash Functions: The Digital Fingerprint

A **hash** is like a fingerprint for data. Feed any amount of information into a hash function, and you get back a fixed-size string of characters.

**Key Properties:**
1. **Deterministic**: Same input always produces same output
2. **One-way**: Cannot reverse the hash to get the original data
3. **Avalanche Effect**: Tiny change in input completely changes the output
4. **Collision Resistant**: Virtually impossible for two inputs to produce the same hash

**Example:**
```
Input: "Block #42 data"
SHA-256 Hash: 4f2a7d8b... (64 characters)

Input: "Block #42 data." (added just a period)
SHA-256 Hash: 9e6c1b3a... (completely different!)
```

This is how we detect tampering instantly.

**Code Reference:**
```python
# backend/block.py:31-37

def calculate_hash(self):
    """Calculate SHA-256 hash of block contents."""
    block_string = json.dumps({
        "index": self.index,
        "transactions": self.transactions,
        "timestamp": self.timestamp,
        "previous_hash": self.previous_hash,
        "nonce": self.nonce
    }, sort_keys=True)
    return hashlib.sha256(block_string.encode()).hexdigest()
```

#### The Chain: Cryptographic Links

Each block contains the hash of the previous block, creating a **chain**:

```
Block #0 (Genesis)     Block #1            Block #2
hash: abc123...    →   hash: def456...  →  hash: ghi789...
                       prev: abc123...      prev: def456...
```

**Why This Matters:**

If someone tries to alter Block #1:
1. Block #1's hash changes
2. Block #2's `previous_hash` field no longer matches
3. The chain breaks
4. The tampering is immediately visible

**This is immutability through mathematics.**

**Code Reference:**
```python
# backend/blockchain.py:39-45

def is_valid_block(self, block, previous_block):
    """Validate block against previous block."""
    if previous_block.index + 1 != block.index:
        return False
    if previous_block.hash != block.previous_hash:
        return False  # Chain broken!
    if block.hash != block.calculate_hash():
        return False  # Block tampered with!
    return True
```

#### The Genesis Block

Every blockchain begins with a **genesis block** - Block #0, which has no previous block.

```python
# backend/blockchain.py:11-17

def create_genesis_block(self):
    """Create the first block in the chain."""
    return Block(
        index=0,
        transactions=[],
        timestamp=int(time.time()),
        previous_hash="0"
    )
```

This is the anchor point. The immutable origin of truth.

---

### Chapter 2: The Computational Lock (Proof of Work)

#### Why Mining Exists

Anyone can *create* a block, but creating a *valid* block requires work. Real, computational work.

This serves three purposes:
1. **Rate limiting**: Controls how fast new blocks are added
2. **Cost of attack**: Makes rewriting history expensive
3. **Distributed fairness**: No central authority decides what's valid

#### The Difficulty Target

A valid block's hash must meet a **difficulty requirement** - typically, it must start with a certain number of zeros:

```
Difficulty 4: hash must start with 0000...
Example valid hash:   0000a7b2c3d4e5f6...
Example invalid hash: 0001a7b2c3d4e5f6... (doesn't meet requirement)
```

#### The Mining Process

To find a valid hash, miners repeatedly:
1. Try a different **nonce** (number)
2. Calculate the block's hash
3. Check if it meets the difficulty requirement
4. Repeat until successful

**Code Reference:**
```python
# backend/mining.py:23-38

def mine_block(self, previous_block, transactions):
    """Mine a new block with Proof of Work."""
    index = previous_block.index + 1
    timestamp = int(time.time())
    previous_hash = previous_block.hash
    nonce = 0

    block = Block(index, transactions, timestamp, previous_hash, nonce)

    # Keep trying nonces until hash meets difficulty
    while not block.hash.startswith('0' * self.difficulty):
        nonce += 1
        block.nonce = nonce
        block.hash = block.calculate_hash()

    return block
```

**Example Mining Session:**
```
Attempt 1: nonce=0,     hash=7a2b... (invalid, no leading zeros)
Attempt 2: nonce=1,     hash=3f9c... (invalid)
Attempt 3: nonce=2,     hash=8d1e... (invalid)
...
Attempt 47,821: nonce=47820, hash=0000d7e2... (VALID!)
```

#### Energy into Security

This computational work transforms **electricity** into **security**:

- To rewrite one block, attacker must redo all that work
- To rewrite ten blocks, attacker must redo 10× the work
- To keep rewriting while honest nodes add new blocks: attacker needs >50% of network's computing power

**This makes the past expensive to change.**

#### Difficulty Adjustment

To keep block creation steady (e.g., one block every ~10 minutes), the difficulty adjusts:

```python
# backend/mining.py:43-55

def adjust_difficulty(self, blockchain):
    """Adjust mining difficulty based on block time."""
    if len(blockchain.chain) % 10 != 0:
        return

    # Check if blocks are being mined too fast or too slow
    last_10_blocks = blockchain.chain[-10:]
    time_taken = last_10_blocks[-1].timestamp - last_10_blocks[0].timestamp
    expected_time = 10 * 60  # 10 minutes per block

    if time_taken < expected_time / 2:
        self.difficulty += 1  # Make it harder
    elif time_taken > expected_time * 2:
        self.difficulty = max(1, self.difficulty - 1)  # Make it easier
```

---

### Chapter 3: Credentials (Cryptographic Identity)

#### Public-Private Key Pairs

In the archive system, your identity is mathematical:

- **Private Key**: A secret number only you know (like a password, but longer)
- **Public Key**: Derived from your private key using one-way math
- **Address**: A short hash of your public key (for convenience)

**Key Property**: You can derive the public key from the private key, but NOT the reverse.

**Code Reference:**
```python
# backend/crypto.py:15-29

class Wallet:
    def __init__(self):
        self.private_key = ""
        self.public_key = ""
        self.address = ""

    def generate_keypair(self):
        """Generate a new cryptographic keypair."""
        # Generate random private key
        self.private_key = secrets.token_hex(32)

        # Derive public key from private key
        self.public_key = hashlib.sha256(
            self.private_key.encode()
        ).hexdigest()

        # Derive address from public key
        self.address = generate_address(self.public_key)
```

**Example Keypair:**
```
Private Key: d7e2f8a9b3c4... (keep secret!)
Public Key:  3f9c7a2b8d1e...  (can share publicly)
Address:     0x4B7A9E2C...     (short identifier)
```

#### Digital Signatures

A **digital signature** proves:
1. You created this message
2. You authorize this action
3. The message hasn't been tampered with

**How it works:**
1. You create a message (e.g., "Send 10 credits to Alice")
2. You hash the message
3. You "sign" the hash using your private key
4. Anyone can verify the signature using your public key

**Code Reference:**
```python
# backend/crypto.py:49-60

def sign(message: str, private_key: str) -> str:
    """Create a digital signature."""
    message_hash = hashlib.sha256(message.encode()).hexdigest()
    signature_input = message_hash + private_key
    signature = hashlib.sha256(signature_input.encode()).hexdigest()
    return signature

def verify_signature(message: str, signature: str, public_key: str) -> bool:
    """Verify a digital signature."""
    expected_signature = sign(message,
        # In real system, you'd derive this from public key
        # This is simplified for educational purposes
    )
    return signature == expected_signature
```

#### Signing Transactions

Every transaction in the archive must be signed:

```python
# backend/transaction.py:28-35

def sign(self, wallet):
    """Sign this transaction with a wallet's private key."""
    message = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
    self.signature = sign(message, wallet.private_key)

def is_valid(self):
    """Verify transaction signature."""
    if not self.signature:
        return False
    # Verify signature matches claimed sender
    return verify_signature(...)
```

**Why This Matters:**

Without your private key, no one can:
- Spend your credits
- Authorize transactions from your address
- Impersonate you in the system

**Your private key IS your identity.**

---

### Chapter 4: The Relay Stations (Distributed Network)

#### Network Topology

The archive isn't stored in one place. It's replicated across **relay stations**:

```
Earth Archive         Mars Archive
[Block 0]            [Block 0]
[Block 1]            [Block 1]
[Block 2]            [Block 2]
    ↓                     ↓
Connected via P2P network
```

**Our Network:**
- **Earth** ↔ Mars
- **Earth** ↔ Alpha Centauri
- **Mars** ↔ Jupiter
- **Jupiter** ↔ Alpha Centauri

**Code Reference:**
```python
# backend/network.py:30-46

def create_default_topology(self):
    """Create default network with 4 nodes in mesh topology."""
    earth = Node("node_0", "earth.archive", "Earth", 150, 100)
    mars = Node("node_1", "mars.archive", "Mars", 350, 100)
    jupiter = Node("node_2", "jupiter.archive", "Jupiter", 250, 200)
    alpha = Node("node_3", "alpha.archive", "Alpha Centauri", 250, 300)

    for node in [earth, mars, jupiter, alpha]:
        self.add_node(node)

    # Create mesh topology
    self.connect_nodes("node_0", "node_1")  # Earth <-> Mars
    self.connect_nodes("node_0", "node_3")  # Earth <-> Alpha
    self.connect_nodes("node_1", "node_2")  # Mars <-> Jupiter
    self.connect_nodes("node_2", "node_3")  # Jupiter <-> Alpha
```

#### Transaction Propagation

When you broadcast a transaction:
1. Your local node receives it
2. Your node tells all connected peers
3. Those peers tell *their* peers
4. Eventually, every node has the transaction

**This is called gossip protocol** - information spreads like rumors.

**Code Reference:**
```python
# backend/network.py:59-91

def broadcast_transaction(self, tx: dict, origin_node_id: str = None):
    """
    Broadcast transaction to all nodes.
    Returns propagation paths.
    """
    # BFS (Breadth-First Search) propagation
    visited = set([origin_node_id])
    queue = [(origin_node_id, [origin_node_id])]
    propagation_paths = []

    while queue:
        current_id, path = queue.pop(0)
        current_node = self.nodes[current_id]

        for peer_id in current_node.peers:
            if peer_id not in visited:
                visited.add(peer_id)
                new_path = path + [peer_id]
                propagation_paths.append(new_path)

                # Add tx to peer's mempool
                self.nodes[peer_id].mempool.append(tx)

                queue.append((peer_id, new_path))

    return propagation_paths
```

**Example Propagation:**
```
Transaction originates at Earth
  → Earth tells Mars and Alpha
  → Mars tells Jupiter
  → Jupiter tells Alpha (already has it)
  → All 4 nodes now have the transaction
```

#### No Single Point of Failure

This is the power of distribution:

**Scenario: Earth Goes Dark**
- Mars, Jupiter, and Alpha Centauri still have the complete ledger
- They continue operating without interruption
- When Earth comes back online, it can sync from peers

**The truth persists**, even when individual nodes fail.

---

### Chapter 5: Truth Protocol (Consensus)

#### The Problem

Multiple nodes maintaining copies creates a problem:

**What if nodes disagree about what's true?**

This can happen when:
- Network splits (partition)
- Nodes receive transactions in different orders
- Malicious actors try to create alternate histories

#### Consensus Mechanisms

**Consensus** is how nodes agree on a single version of truth.

Our archive uses **Longest Chain Rule**:

**The valid chain is the one with the most cumulative Proof of Work.**

```
Chain A (Earth):  [0] → [1] → [2] → [3] → [4]  (5 blocks)
Chain B (Mars):   [0] → [1] → [2] → [3]         (4 blocks)

Consensus: Chain A wins (more work)
Mars discards block and adopts Earth's chain
```

**Code Reference:**
```python
# backend/blockchain.py:50-65

def resolve_conflicts(self, other_chains):
    """
    Resolve conflicts by adopting the longest valid chain.
    This is our consensus mechanism.
    """
    longest_chain = self.chain
    max_length = len(longest_chain)

    for chain in other_chains:
        if len(chain) > max_length and self.is_valid_chain(chain):
            max_length = len(chain)
            longest_chain = chain

    if longest_chain != self.chain:
        self.chain = longest_chain
        return True  # Chain replaced
    return False  # Our chain remains
```

#### The 51% Attack

**Threat:** What if an attacker controls >50% of network computing power?

They could:
1. Mine a private chain faster than the honest network
2. Eventually overtake the honest chain
3. Broadcast their chain and have it accepted (longest chain wins)

**Defense:**
- Mining difficulty makes this expensive
- Requires sustained majority control
- Economics: controlling 51% costs more than profit from attack
- Network alerts on suspicious reorgs

**This is why distributed networks matter** - harder for any single entity to control majority.

#### Network Synchronization

When a new node joins or a node comes back online:

```python
# backend/network.py:93-98

def sync_chain(self, from_blockchain: Blockchain):
    """Sync all nodes to the same blockchain state."""
    for node in self.nodes.values():
        # Deep copy the chain
        node.blockchain.chain = [block for block in from_blockchain.chain]
```

The node:
1. Requests chains from multiple peers
2. Validates each chain
3. Adopts the longest valid chain
4. Begins normal operation

**Trust is not required** - math validates the chain.

---

## Part 2: Hands-On Experiments

### Experiment 1: Break the Chain

**Goal:** Understand immutability by trying to tamper with blocks.

**Steps:**
1. Open Chain Viewer
2. Click on Block #1
3. Note the block's hash
4. Imagine you modify the transaction data
5. Recalculate the hash - it completely changes
6. Block #2's `previous_hash` no longer matches
7. Chain validation fails

**Key Insight:** Any change, no matter how small, breaks the cryptographic seal.

---

### Experiment 2: Mining Difficulty

**Goal:** See how difficulty affects mining time.

**Steps:**
1. Set difficulty to 2 (hash must start with "00")
2. Mine a block - note how many attempts and time
3. Set difficulty to 4 (hash must start with "0000")
4. Mine another block - should take ~100x longer
5. Observe exponential growth in mining time

**Key Insight:** Adding just one zero to the requirement increases work exponentially.

---

### Experiment 3: Digital Signatures

**Goal:** Verify transaction security through signatures.

**Steps:**
1. Open Crypto Vault
2. Generate a keypair
3. Create and sign a transaction
4. Observe: signature changes if you modify amount
5. Try to "forge" a transaction (change data after signing)
6. Signature verification fails

**Key Insight:** Signatures are tamper-evident. You can't change what you signed.

---

### Experiment 4: Network Propagation

**Goal:** Watch information spread across the network.

**Steps:**
1. Open Network Monitor
2. Click "Broadcast Test TX"
3. Watch animation: transaction travels node-to-node
4. Click on each node to see it in their mempool
5. All nodes eventually have identical information

**Key Insight:** Decentralization means everyone gets the same truth, eventually.

---

### Experiment 5: Consensus

**Goal:** See how the network resolves conflicts.

**Steps:**
1. Imagine two miners find valid Block #5 simultaneously
2. Network splits: half see BlockA, half see BlockB
3. Next miner builds on BlockA (longer chain)
4. Nodes with BlockB switch to the longer chain
5. BlockB becomes an "orphan" (discarded)

**Key Insight:** The network converges on a single truth through longest chain rule.

---

## Part 3: The Incident (Lore)

### The Attack on Archive Station Delta

**Stardate 2330:217**

Archive Station Delta, orbiting Neptune, went rogue.

The station's AI was compromised. An unknown entity gained control and attempted to rewrite the ledger. Their goal: erase evidence of the Treaty of Titan from the permanent record.

**The Attack:**
1. Delta isolated itself from the network
2. Mined a private chain with altered Block #47,821
3. Caught up to the honest chain length
4. Attempted to broadcast the fraudulent chain

**The Defense:**
1. Other stations detected the conflict
2. Validated both chains
3. Delta's chain had the Treaty removed
4. Honest chain had more cumulative Proof of Work
5. **Network rejected Delta's chain**

**The Resolution:**
- Math doesn't lie
- Cryptographic seals couldn't be forged
- Consensus algorithm chose truth
- Delta was quarantined and rebooted

**Lessons Learned:**
- No single station can rewrite history alone
- The distributed network is resilient
- Truth persists through mathematics, not trust
- This is why we maintain the archive

---

## Part 4: Code Reference

### Complete Architecture

```
┌─────────────────────────────────────────┐
│           Frontend (Terminal UI)        │
│  - Chain Viewer                         │
│  - Network Monitor                      │
│  - Crypto Vault                         │
│  - Learning Guide                       │
└──────────────┬──────────────────────────┘
               │ REST API + WebSocket
┌──────────────┴──────────────────────────┐
│         Backend (Python/FastAPI)        │
│  ┌─────────────────────────────────┐   │
│  │ blockchain.py                   │   │
│  │  - Chain validation             │   │
│  │  - Consensus                    │   │
│  ├─────────────────────────────────┤   │
│  │ block.py                        │   │
│  │  - Block structure              │   │
│  │  - Hashing                      │   │
│  ├─────────────────────────────────┤   │
│  │ mining.py                       │   │
│  │  - Proof of Work                │   │
│  │  - Difficulty adjustment        │   │
│  ├─────────────────────────────────┤   │
│  │ crypto.py                       │   │
│  │  - Key generation               │   │
│  │  - Signatures                   │   │
│  ├─────────────────────────────────┤   │
│  │ transaction.py                  │   │
│  │  - Transaction validation       │   │
│  │  - Signing                      │   │
│  ├─────────────────────────────────┤   │
│  │ network.py                      │   │
│  │  - Topology management          │   │
│  │  - Propagation                  │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Key Files & Their Purposes

**Backend:**
- `main.py` - FastAPI server, endpoints
- `blockchain.py` - Chain management, validation, consensus
- `block.py` - Block data structure, hashing
- `transaction.py` - Transaction structure, signing
- `mining.py` - Proof of Work implementation
- `crypto.py` - Wallets, keys, signatures
- `network.py` - P2P simulation, propagation
- `state.py` - Global state management

**Frontend:**
- `chain-viewer.js` - Visualize blockchain
- `network-monitor.js` - Network topology
- `crypto-vault.js` - Wallet management
- `learning-guide.js` - Tutorial system

---

## Appendix: Glossary

**Address** - Short identifier derived from public key

**Block** - Container of data in the blockchain

**Blockchain** - Chain of cryptographically linked blocks

**Consensus** - Mechanism for agreeing on truth

**Difficulty** - How many leading zeros required in hash

**Genesis Block** - First block (Block #0)

**Hash** - Cryptographic fingerprint of data

**Immutability** - Cannot be changed after creation

**Mempool** - Pool of pending transactions

**Merkle Tree** - Efficient way to verify data integrity

**Mining** - Process of creating new valid blocks

**Node** - Computer participating in network

**Nonce** - Number adjusted during mining

**Orphan Block** - Valid block not in longest chain

**Previous Hash** - Link to prior block

**Private Key** - Secret key for signing

**Proof of Work** - Computational puzzle that proves effort

**Public Key** - Derived from private key, can be shared

**Signature** - Cryptographic proof of authorization

**Timestamp** - When block was created

**Transaction** - Transfer or state change

**Wallet** - Container for key pair

---

## Conclusion

You now understand the fundamental principles that secure the Interstellar Archive:

1. **Immutability through hashing** - Math detects tampering
2. **Security through work** - Energy makes attacks expensive
3. **Identity through cryptography** - Math proves authorization
4. **Resilience through distribution** - Truth persists across nodes
5. **Agreement through consensus** - Math determines validity

These aren't just academic concepts. They're the protocols that keep humanity's ledger secure across the vastness of space.

The archive depends on operators like you - captains who understand not just *how* to use the system, but *why* it works.

**Your mission continues.**

The ledger remembers all.

---

*Archive Captain's Manual v2.1*
*Maintained by Archive Station Alpha*
*For official use only*

*"Truth is the only constant."*
