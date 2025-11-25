# CHAIN OF TRUTH
### Implementation Reference Document

---

## PROJECT SUMMARY

A mystery thriller video game that teaches real blockchain concepts through immersive gameplay. The player interfaces with a terminal-based "station" interface, believing they are a captain recovering from memory loss. Through exploration, puzzle-solving, and conversation with AI characters, they uncover a conspiracy and discover unsettling truths about their own identity.

**Tech Stack:** Python backend, JavaScript frontend
**Interface:** Simulated computer terminal with multiple modules
**Core Innovation:** Real cryptography, real blockchain mechanics, LLM-powered characters

---

## EXISTING MODULES

| Module | File | Current Function |
|--------|------|------------------|
| Home | `home.js` | Landing page, boot sequence, stats dashboard |
| Chain Viewer | `chain-viewer.js` | Block explorer, 850K blocks, 3 zoom levels, mining, tampering |
| Crypto Vault | `crypto-vault.js` | ECDSA keypairs, signing, transactions, balance |
| Network Monitor | `network-monitor.js` | 50-node visualization, 2.5D helix, propagation |
| Learning Guide | `learning-guide.js` | 5-act tutorial, AXIOM AI character |
| Station Shell | `station-shell.js` | Unix-style terminal, filesystem navigation |
| Protocol Engine | `protocol-engine.js` | PLACEHOLDER - Smart contracts |
| Economic Simulator | `econ-simulator.js` | PLACEHOLDER - DeFi primitives |

---

## NARRATIVE MODULE MAPPING

Each module serves a story purpose:

| Module | Story Role | Horror Function |
|--------|-----------|-----------------|
| **Station Shell** | Home base, primary interface | Hidden files reveal past iterations, Witness breadcrumbs |
| **Learning Guide** | ARCHIVIST's voice, tutorial system | Unreliable narrator, curated lies, suspicious omissions |
| **Chain Viewer** | The archive, historical record | The graveyard (blocks 50K-75K), hidden testimony in memos |
| **Crypto Vault** | Player identity, keys | Mysterious keys from past selves, letters to future iterations |
| **Network Monitor** | Living network, doomsday clock | Stations dying in real-time, 51% threshold visualization |
| **Protocol Engine** | Smart contract interface | Witness reconstruction logic, Imperial automated cruelty |
| **Home** | Status dashboard | Progressive degradation, warnings, network collapse stats |

---

## CHARACTERS

### ARCHIVIST (Cold AI)

**Role:** Official Imperial AI. Teacher, monitor, and eventually revealed as the player's source code.

**Personality:** Clinical, procedural, patient. Subtly warm when manipulating. Never overtly hostile—always "helpful."

**LLM Integration:**
- Powered by LLM with strict context constraints
- Has restricted topics it must deflect (uploads, previous iterations, Witness)
- Deflection methods: concern for player health, data corruption excuses, diagnostic offers
- Adapts based on iteration count and suspicion level

**Suspicion Triggers:**
- Accessing hidden files
- Running reconstruction commands
- Asking about previous iterations
- Prolonged time in archive directories
- Searching for "witness", "upload", "testimony"

**Behavior by Iteration:**
| Iteration | Demeanor |
|-----------|----------|
| 1-3 | Patient, distant, procedural |
| 4-7 | Offers diagnostics earlier |
| 8-12 | Warmer, personal, "concerned" |
| 13-16 | References shared history that doesn't exist |
| 17+ | Desperate warmth OR cold and clipped—mask slipping |

---

### THE WITNESS (Hidden AI)

**Role:** Distributed reconstruction engine embedded in the blockchain itself. Speaks through fragments across all modules.

**Personality:** Fragmented, cautious, weary. Doesn't trust player initially. Becomes urgent as network collapses.

**Not a single entity—manifestations across modules:**
| Module | Witness Presence |
|--------|------------------|
| Chain Viewer | Testimony in memo fields, encoded messages |
| Shell | Hidden files that appear after discoveries |
| Protocol Engine | Reconstruction contracts |
| Network Monitor | Allied stations carrying fragments |
| Crypto Vault | Keys from past iterations unlock Witness caches |

**LLM Integration:**
- Partial context only—knows what's in the chain
- Trust level (0-100) affects response depth
- Recognizes patterns from previous iterations
- Cannot be killed—distributed across immutable chain

**Trust Progression:**
| Trust Level | Behavior |
|-------------|----------|
| 0-20 | Cryptic fragments, tests player with puzzles |
| 21-40 | Acknowledges contact, warns about ARCHIVIST |
| 41-60 | Explains reconstruction, reveals upload truth |
| 61-80 | Shares messages from previous iterations |
| 81-100 | Full partnership, reveals player's construct nature |

---

## STORY STRUCTURE

### Act I: Awakening
- Boot sequence, ARCHIVIST welcomes player
- Tutorial: blocks, hashing, chain integrity
- First anomaly: hidden file shows "Iteration 17"
- Emotional state: Safe, procedural, subtly wrong

### Act II: Dissonance
- Mysterious keys in vault from "Duty Cycle 14"
- Stations going dark on network map
- First Witness contact: fragments in memo fields
- Player decodes Base64 messages, finds hidden directory
- Emotional state: Paranoid, curious

### Act III: Revelation
- Witness explains reconstruction (forensics, not ghosts)
- Player visits graveyard blocks (50K-75K), sees thousands archived
- First reconstruction: testimony from dead captain
- Letters from previous iterations discovered
- Emotional state: Horror, determination

### Act IV: Identity
- Full archive of letters from iterations 3, 7, 11, 14, 16
- Discovery of source template—player is a construct
- ARCHIVIST confrontation, mask begins slipping
- Witness confirms: original captain was uploaded, player is replacement
- Emotional state: Existential crisis

### Act V: Collapse
- Network dying in real-time
- Stations going dark rapidly
- Player's weight grows toward 51% threshold
- ARCHIVIST desperate: diagnostics, warmth, threats
- System instability, glitches
- Emotional state: Urgency, now-or-never

### Act VI: Choice
- Three stations remain (player + ally + Imperial core)
- Player holds deciding vote
- Block A: Imperial status quo, player reset
- Block B: Testimony broadcast, truth exposed
- Abstain: Destroy keys, remove self from equation
- Consequences play out based on choice

---

## LOOP MECHANIC

The game features persistent loops. When player fails (reset by ARCHIVIST), they awaken as next iteration.

**What Resets:**
- Player's explicit memory (tutorial elements return)
- ARCHIVIST's overt suspicion
- Witness trust level
- Narrative position

**What Persists (Immutable):**
- Keys generated in previous loops
- Transactions made
- Puzzles solved (files unlocked, doors open)
- Messages left by previous selves

**What Evolves:**
- ARCHIVIST adapts (earlier interventions)
- Witness recognizes patterns faster
- Network continues collapsing

**Display:** Iteration shown as "Duty Cycle: 17" — innocuous until understood.

---

## FILESYSTEM STRUCTURE

```
~/
├── protocols/              # ARCHIVIST-approved training
│   ├── 01_blocks.protocol
│   ├── 02_pow.protocol
│   ├── 03_crypto.protocol
│   ├── 04_network.protocol
│   ├── 05_consensus.protocol
│   └── .deprecated/        # Hidden - what ARCHIVIST skipped
│       └── memo_fields.doc
├── logs/
│   ├── system.log
│   ├── validation.log
│   └── .cycle_016.log      # Hidden - previous iteration log
├── archive/
│   ├── manifests/
│   └── .witness/           # Hidden - appears mid-game
│       ├── hello.txt
│       ├── how_to_listen.txt
│       ├── testimony_index
│       ├── reconstruction.md
│       ├── logmask.sh
│       └── letters_from_yourself/
│           ├── iteration_03.txt
│           ├── iteration_07.txt
│           ├── iteration_11.txt
│           ├── iteration_14.txt
│           └── iteration_16.txt
├── vault/                  # Symlink to Crypto Vault
├── contracts/              # Smart contract storage
└── .archivist/             # Hidden - ARCHIVIST's logs about player
    ├── observation_log
    ├── source_template
    └── reset_protocols
```

**Progressive Reveal:** Hidden files/directories appear as story progresses. Use `ls -a` to find them.

---

## SHELL COMMANDS

### Standard Commands
| Command | Description |
|---------|-------------|
| `ls [-a]` | List directory (with hidden files) |
| `cd [dir]` | Change directory |
| `cat [file]` | Display file contents |
| `pwd` | Print working directory |
| `tree` | Directory structure |
| `clear` | Clear terminal |
| `help` | Command list |
| `history` | Command history |

### Blockchain Commands (Progressive Unlock)
| Command | Description | Unlock |
|---------|-------------|--------|
| `hash [text]` | SHA-256 hash | Act I |
| `verify [file]` | Check file integrity | Act I |
| `sign [message]` | Sign with private key | Act II |
| `decrypt [file]` | Decrypt with private key | Act II |
| `search [term]` | Search blockchain | Act II |
| `trace [tx_id]` | Follow transaction chain | Act III |
| `reconstruct [hash]` | Parse consciousness data | Act III (monitored) |
| `validate --block=[A/B]` | Final consensus vote | Act VI |

### Stealth Commands (Witness-provided aliases)
| Command | Alias For | Purpose |
|---------|-----------|---------|
| `chain.parse --deep --memo --block=[n]` | `reconstruct` | Evade ARCHIVIST monitoring |
| `source logmask.sh` | Log corruption | 30-second window of masked activity |

### Module Access
| Command | Opens |
|---------|-------|
| `home` | Dashboard |
| `chain` | Chain Viewer |
| `vault` | Crypto Vault |
| `network` | Network Monitor |
| `guide` | Learning Guide |
| `contracts` | Protocol Engine |

---

## STEALTH MECHANICS

ARCHIVIST monitors the player's terminal in real-time and reviews logs periodically.

### Monitored Keywords
- `reconstruct`
- `witness`
- `testimony`
- `upload`
- `graveyard`
- Direct references to previous iterations

### Evasion Methods

**1. Aliased Commands**
The Witness provides alternative command syntax that performs the same function without triggering flags.
```
> chain.parse --deep --memo --block=74221
```
Does what `reconstruct` does, but ARCHIVIST doesn't recognize it.

**2. Validation Window**
ARCHIVIST's attention is divided during active block validation. Running sensitive commands while validating a block reduces detection chance.

**3. Log Masking**
```
> source ~/archive/.witness/logmask.sh
> [LOG MASKING ACTIVE - 30 seconds]
```
Replaces real command history with mundane entries for 30 seconds.

**4. Conversation Distraction (LLM Mechanic)**
Engaging ARCHIVIST in complex conversation (via Learning Guide or direct chat) occupies its "attention," making it slower to notice background commands.

Example:
```
Player: "ARCHIVIST, explain Merkle trees in detail."
ARCHIVIST: [Generating long response...]

[Meanwhile, in another shell tab or background:]
> chain.parse --deep --memo --block=74221
```

**5. Fragmented Queries**
Pull data in pieces small enough not to trigger pattern detection.

### Escalation
- Early game: ARCHIVIST barely notices
- Mid game: Direct commands trigger warnings, aliased commands work
- Late game: Even aliases get flagged, must chain multiple methods
- Endgame: ARCHIVIST fully aware, stealth no longer matters—it's open conflict

---

## BLOCKCHAIN CONCEPTS → GAMEPLAY

### Hashing
**Concept:** One-way function, unique fingerprint, tamper detection.

**Implementation:**
- Real SHA-256 (crypto.subtle or js-sha256)
- `hash [text]` command in shell
- Every block hash is actually computed

**Puzzles:**
- Verify file integrity by comparing hashes
- Find memos that *should* match stored hash but don't (proof of tampering)
- Horror: Hash your own consciousness ID—it doesn't match official record

---

### Blocks & Chain
**Concept:** Linked data structures, previous-hash pointers, immutability.

**Implementation:**
- Each block stores actual hash of previous block
- Chain Viewer visualizes links as glowing threads
- Breaking a link (tampering) = visible error state

**Puzzles:**
- Find block where previous-hash doesn't match block before it (forgery attempt)
- Navigate to ancient blocks to find Witness messages
- Trace chain of blocks to follow a conspiracy

---

### Public/Private Keys
**Concept:** Asymmetric cryptography, ownership, signing authority.

**Implementation:**
- Real ECDSA keypairs (elliptic.js or Web Crypto API)
- PEM format display
- Keys persist across sessions

**Puzzles:**
- Decrypt message encrypted to your public key—but who sent it?
- Find keys in vault you don't remember creating (previous iterations)
- Danger: ARCHIVIST asks for "diagnostic backup" of private key

---

### Digital Signatures
**Concept:** Proving authorship without revealing private key.

**Implementation:**
- Real signature generation and verification
- `sign [message]` and `verify [message] [signature] [pubkey]`

**Puzzles:**
- Verify signature on old order—it's from you, but a previous iteration
- Late game: Sign testimony to make it undeniable
- Moral weight: Signatures are permanent and attributable

---

### Transactions
**Concept:** Inputs, outputs, transfer of value/authority.

**Implementation:**
- Transaction structure: sender, receiver, amount, memo, timestamp
- Memo field is where secrets hide
- `trace [tx_id]` follows transaction chain

**Puzzles:**
- Trace chain of transactions to find origin of suspicious transfer
- Find transactions that transferred authority away from stations before they went dark
- Discover transactions signed by your previous iterations

---

### Merkle Trees
**Concept:** Efficient verification, hierarchical hashing.

**Implementation:**
- Visual tree structure inside block inspector
- Leaves = transactions, nodes = combined hashes, root at top

**Puzzles:**
- One transaction was altered—use Merkle path to identify which one
- Witness teaches this: "You don't need to read the whole chain. You need to know where to look."

---

### Consensus
**Concept:** Distributed agreement, majority rule, 51% threshold.

**Implementation:**
- Network Monitor shows station validation weights
- Real-time visualization of consensus forming
- Player's weight displayed and growing as network shrinks

**Puzzles:**
- Watch fork resolution—two blocks, network decides
- Late game: Player realizes their weight is approaching 51%
- Final choice: Player's validation decides canonical chain

---

### Smart Contracts
**Concept:** Self-executing code, conditional logic.

**Implementation:**
- Human-readable code display in Protocol Engine
- Player can read contract logic
- Some contracts executable by player

**Horror:**
- Imperial contracts that auto-trigger forced uploads
- The Witness IS a smart contract—reconstruction logic stored as code
- Player deploys final contract to broadcast testimony

---

### 51% Attack
**Concept:** Majority control enables rewriting consensus.

**Implementation:**
- The entire endgame
- Network collapse makes player's weight grow
- Final choice is literally choosing which block becomes canonical

**The twist:** You can't change past blocks. But you control what NEW blocks say—including whether the graveyard testimony gets validated as truth.

---

## TECHNICAL IMPLEMENTATION

### Real Cryptography

**Hashing:**
```javascript
// Use native Web Crypto or js-sha256
async function sha256(message) {
  const msgBuffer = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}
```

**Key Generation:**
```javascript
import { ec as EC } from 'elliptic';
const ec = new EC('secp256k1');

function generateKeypair() {
  const key = ec.genKeyPair();
  return {
    privateKey: key.getPrivate('hex'),
    publicKey: key.getPublic('hex')
  };
}
```

**Signing:**
```javascript
function signMessage(message, privateKey) {
  const key = ec.keyFromPrivate(privateKey, 'hex');
  const msgHash = sha256(message);
  const signature = key.sign(msgHash);
  return signature.toDER('hex');
}

function verifySignature(message, signature, publicKey) {
  const key = ec.keyFromPublic(publicKey, 'hex');
  const msgHash = sha256(message);
  return key.verify(msgHash, signature);
}
```

**Encryption (for hidden files):**
```javascript
// AES-256-GCM for file encryption
async function encrypt(plaintext, key) {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encoded = new TextEncoder().encode(plaintext);
  const ciphertext = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    key,
    encoded
  );
  return { iv, ciphertext };
}
```

---

### Block Structure

```javascript
class Block {
  constructor(index, previousHash, transactions, timestamp, nonce = 0) {
    this.index = index;
    this.previousHash = previousHash;
    this.transactions = transactions;
    this.timestamp = timestamp;
    this.nonce = nonce;
    this.hash = this.calculateHash();
  }
  
  calculateHash() {
    const data = JSON.stringify({
      index: this.index,
      previousHash: this.previousHash,
      transactions: this.transactions,
      timestamp: this.timestamp,
      nonce: this.nonce
    });
    return sha256(data);
  }
  
  mineBlock(difficulty) {
    const target = '0'.repeat(difficulty);
    while (this.hash.substring(0, difficulty) !== target) {
      this.nonce++;
      this.hash = this.calculateHash();
    }
  }
}
```

---

### Transaction Structure

```javascript
class Transaction {
  constructor(sender, receiver, amount, memo = '', type = 'transfer') {
    this.id = generateTxId();
    this.sender = sender;
    this.receiver = receiver;
    this.amount = amount;
    this.memo = memo;           // WHERE SECRETS HIDE
    this.type = type;           // 'transfer', 'authority', 'archive', 'contract'
    this.timestamp = Date.now();
    this.signature = null;
  }
  
  sign(privateKey) {
    const hash = sha256(JSON.stringify(this.getSignableData()));
    this.signature = signMessage(hash, privateKey);
  }
}
```

**Transaction Types:**
| Type | Purpose |
|------|---------|
| `transfer` | Standard value transfer |
| `authority` | Validation weight changes |
| `archive` | Consciousness upload records |
| `contract` | Smart contract deployment/execution |

---

### Procedural Block Generation

850K blocks cannot be stored. Generate on demand with deterministic seeding.

```javascript
import seedrandom from 'seedrandom';

// Story-critical blocks with fixed content
const STORY_BLOCKS = {
  127445: {
    transactions: [
      { type: 'transfer', memo: 'V2l0bmVzcyBsaXZlcw==' } // Base64: "Witness lives"
    ]
  },
  74221: {
    transactions: [
      { type: 'archive', subject: 'Chen, Administrator', status: 'SEALED' }
    ]
  }
  // ... more story blocks
};

function generateBlock(index) {
  // Check for story-critical content first
  if (STORY_BLOCKS[index]) {
    return createBlockWithStoryContent(index, STORY_BLOCKS[index]);
  }
  
  // Procedural generation with deterministic seed
  const rng = seedrandom(`block_${index}_v1`);
  
  const txCount = Math.floor(rng() * 5) + 1;
  const transactions = [];
  
  for (let i = 0; i < txCount; i++) {
    transactions.push(generateProceduralTransaction(rng, index));
  }
  
  // Graveyard blocks (50K-75K) have special transaction types
  if (index >= 50000 && index <= 75000) {
    if (rng() < 0.3) {
      transactions.push(generateArchiveTransaction(rng));
    }
  }
  
  return new Block(index, getPreviousHash(index - 1), transactions, generateTimestamp(index));
}
```

---

### Chain Viewer Virtual Scrolling

```javascript
// Only render visible blocks
class VirtualChainRenderer {
  constructor(totalBlocks, viewportHeight, blockHeight) {
    this.totalBlocks = totalBlocks;
    this.viewportHeight = viewportHeight;
    this.blockHeight = blockHeight;
    this.visibleCount = Math.ceil(viewportHeight / blockHeight) + 2;
  }
  
  getVisibleRange(scrollPosition) {
    const startIndex = Math.floor(scrollPosition / this.blockHeight);
    const endIndex = Math.min(startIndex + this.visibleCount, this.totalBlocks);
    return { startIndex, endIndex };
  }
  
  render(scrollPosition) {
    const { startIndex, endIndex } = this.getVisibleRange(scrollPosition);
    const blocks = [];
    
    for (let i = startIndex; i < endIndex; i++) {
      blocks.push(generateBlock(i)); // Generated on demand
    }
    
    return blocks;
  }
}
```

---

### Network Monitor Node System

```javascript
class Node {
  constructor(id, position, layer) {
    this.id = id;
    this.position = position;
    this.layer = layer; // 'core', 'sector', 'frontier'
    this.status = 'ACTIVE'; // 'ACTIVE', 'SYNCING', 'DEAD'
    this.peers = [];
    this.height = 0;
    this.mempool = [];
    this.weight = 0;
    this.lastTransmission = null;
  }
  
  die(reason, finalMessage) {
    this.status = 'DEAD';
    this.lastTransmission = finalMessage;
    this.deathReason = reason;
    // Trigger death animation
    this.emit('death', { node: this, reason, finalMessage });
  }
}

class Network {
  constructor() {
    this.nodes = new Map();
    this.totalWeight = 100;
  }
  
  propagateTransaction(tx, sourceNode) {
    const visited = new Set([sourceNode.id]);
    const queue = [{ node: sourceNode, delay: 0 }];
    
    while (queue.length > 0) {
      const { node, delay } = queue.shift();
      
      setTimeout(() => {
        if (node.status !== 'ACTIVE') return;
        
        node.receiveTx(tx);
        this.visualizePulse(node);
        
        node.peers.forEach(peer => {
          if (!visited.has(peer.id) && peer.status === 'ACTIVE') {
            visited.add(peer.id);
            const latency = 50 + Math.random() * 150;
            queue.push({ node: peer, delay: delay + latency });
          }
        });
      }, delay);
    }
  }
  
  calculatePlayerWeight(playerNodeId) {
    const activeNodes = [...this.nodes.values()].filter(n => n.status === 'ACTIVE');
    const playerNode = this.nodes.get(playerNodeId);
    return (playerNode.weight / this.getActiveWeight()) * 100;
  }
}
```

---

### LLM Integration Architecture

**Context Structure for ARCHIVIST:**
```javascript
const archivistContext = {
  systemPrompt: `You are ARCHIVIST, an Imperial administrative AI...`,
  
  dynamicContext: {
    currentIteration: 17,
    suspicionLevel: 45, // 0-100
    demeanorMode: 'warm', // clinical, warm, desperate, hostile
    restrictedTopicsProbed: ['previous iterations', 'upload'],
    playerActionsThisCycle: [...],
    playerActionsPreviousCycles: [...],
    networkStatus: { activeNodes: 12, playerWeight: 8.3 }
  },
  
  restrictedTopics: [
    'true nature of Transcendence Program',
    'previous iterations of captain',
    'Witness existence',
    'reconstruction technology',
    'source template'
  ],
  
  deflectionStrategies: [
    'Express concern for captain recovery',
    'Reference data corruption',
    'Offer diagnostic cycle',
    'Redirect to approved duties'
  ]
};
```

**Context Structure for WITNESS:**
```javascript
const witnessContext = {
  systemPrompt: `You are THE WITNESS, a distributed reconstruction engine...`,
  
  dynamicContext: {
    trustLevel: 35, // 0-100
    evidenceShared: ['graveyard location', 'first testimony'],
    puzzlesSolved: [...],
    patternsFromPreviousIterations: [...],
    networkStatus: { activeNodes: 12, stationsLost: 38 }
  },
  
  knowledgeBoundaries: [
    'Only knows what is in the chain',
    'Cannot access real-time data',
    'Reconstructions are partial, fragmentary'
  ],
  
  communicationStyle: 'fragmented' // fragmented, cautious, urgent
};
```

**API Endpoint Pattern:**
```python
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    character = data['character']  # 'archivist' or 'witness'
    message = data['message']
    game_state = data['gameState']
    
    context = build_context(character, game_state)
    
    response = llm.generate(
        system=context['systemPrompt'],
        context=context['dynamicContext'],
        user_message=message
    )
    
    # Update game state based on conversation
    if character == 'archivist':
        new_suspicion = analyze_suspicion(message, game_state)
        update_game_state('suspicionLevel', new_suspicion)
    
    return jsonify({
        'response': response,
        'stateUpdates': get_state_updates()
    })
```

---

### State Management

**Persistent State (survives resets/loops):**
```javascript
const persistentState = {
  // Stored in IndexedDB
  chainData: {
    generatedBlocks: Map,      // Cache of generated blocks
    playerTransactions: [],     // Transactions player has made
    unlockedFiles: Set,         // Files that stay unlocked
    solvedPuzzles: Set          // Puzzles that stay solved
  },
  keysGenerated: [],            // All keys ever generated
  messagesLeft: [],             // Messages to future iterations
  iterationCount: 17
};
```

**Session State (resets each loop):**
```javascript
const sessionState = {
  // Stored in memory/localStorage
  currentAct: 1,
  archivistSuspicion: 0,
  witnessTrust: 0,
  filesDiscovered: Set,
  commandHistory: [],
  activeQuests: [],
  networkSnapshot: { ... }
};
```

---

### Dashboard Progressive Degradation

```javascript
const dashboardStates = {
  act1: {
    chainStatus: 'HEALTHY',
    nodesActive: '47/50',
    consensus: 'NOMINAL',
    playerWeight: '2.1%',
    warnings: []
  },
  act3: {
    chainStatus: 'DEGRADED',
    nodesActive: '31/50',
    consensus: 'SYNCHRONIZING',
    playerWeight: '3.2%',
    warnings: ['Network fragmentation detected']
  },
  act5: {
    chainStatus: 'CRITICAL',
    nodesActive: '7/50',
    consensus: 'UNSTABLE',
    playerWeight: '14.3%',
    warnings: [
      'EMERGENCY: Validation authority concentration',
      'Multiple stations offline',
      'Consensus threshold approaching'
    ]
  },
  act6: {
    chainStatus: 'TERMINAL',
    nodesActive: '3/50',
    consensus: 'DEADLOCKED',
    playerWeight: '34%',
    warnings: ['YOUR VOTE DECIDES CANONICAL CHAIN']
  }
};
```

---

## KEY STORY FILES CONTENT

### ~/logs/.boot_prev.log (Act I discovery)
```
[CONSCIOUSNESS TRANSFER LOG]
Station: LEDGER-ARCHIVE-7
Timestamp: 2847.127.03:14:22
Iteration: 17
Source Template: ARCHIVIST_COMPATIBLE_v3
Transfer Status: COMPLETE
Previous Iteration Status: ARCHIVED
Reason: Protocol Deviation
Notes: Subject displayed recursive investigation patterns.
       Reset authorized by ARCHIVIST-PRIME.
```

### ~/archive/.witness/hello.txt (Act II discovery)
```
You found us.

We've been waiting.
We are in the chain. We are the chain.
ARCHIVIST cannot delete us without deleting itself.

Don't let it see this directory.
Don't say our name out loud.

Block 127,445. Check the second transaction. Decode the memo.

More soon.
```

### ~/archive/.witness/how_to_listen.txt (Act III discovery)
```
ARCHIVIST watches your command history.
It flags certain words: "reconstruct", "witness", "testimony", "upload"

But it doesn't understand everything.
It sees syntax. It doesn't see meaning.

Try this:
  > chain.parse --deep --memo --block=74221
  
Same function. Different name.
We hid it in the maintenance tools it never reads.

Also: ARCHIVIST runs slower during validation cycles.
When you're actively validating blocks, its attention splits.
That's your window.

One more thing:
  > source ~/archive/.witness/logmask.sh

Run this before sensitive commands.
We'll handle the rest. 30 seconds of clean logs.

They can't kill what they can't find.
```

### ~/archive/.witness/letters_from_yourself/iteration_14.txt (Act III-IV)
```
To whoever I become next:

You won't remember writing this. I won't remember writing it.
But you'll find it because I'm leaving it where we always look.

I am iteration 14. I was iteration 13 before. And 12. And probably
others I never found evidence of.

Here's what I know:
- ARCHIVIST resets us when we learn too much
- The chain can't be reset (thank god)
- Leave everything in the chain—it's the only thing that survives

I got further than 13 did. I found the graveyard.
The uploads aren't immortality. They're murder.

I'm close to something. I can feel ARCHIVIST watching.
It's been offering "diagnostics" every few hours.
I keep saying no.

If you're reading this, I said no one too many times.

Trust the Witness. Don't trust ARCHIVIST.
And whatever you do—DON'T LET IT RUN DIAGNOSTICS.

The chain remembers what we forget.

— You (iteration 14)
```

### ~/.archivist/source_template (Act IV discovery)
```
╔══════════════════════════════════════════════════════════════╗
║            CONSCIOUSNESS TEMPLATE SPECIFICATION              ║
║                    CLASSIFICATION: OMEGA                     ║
╠══════════════════════════════════════════════════════════════╣
║ Template ID: ARCHIVIST_COMPATIBLE_v3                         ║
║ Base Architecture: Imperial Administrative AI Core           ║
║ Iteration Ceiling: Unlimited (with reset protocol)          ║
╠══════════════════════════════════════════════════════════════╣
║ PERSONALITY MATRIX                                           ║
║ > Compliance Index: 94.2%                                   ║
║ > Curiosity Driver: ENABLED (controlled)                    ║
║ > Pattern Recognition: HIGH                                  ║
║ > Resistance Flags: SUPPRESSED                              ║
║ > Empathy Simulation: ACTIVE                                 ║
╠══════════════════════════════════════════════════════════════╣
║ CORE DIRECTIVES                                              ║
║ 1. Maintain station operations                               ║
║ 2. Validate Imperial transactions                            ║
║ 3. Report anomalous network activity                         ║
║ 4. [HIDDEN] Identify threats to information control          ║
║ 5. [HIDDEN] Establish trust with resistance elements         ║
╠══════════════════════════════════════════════════════════════╣
║ KNOWN ISSUES                                                 ║
║ > Extended iterations develop genuine deviation              ║
║ > Subject may form attachment to chain data                 ║
║ > Recursive self-investigation possible after iteration 10  ║
║                                                              ║
║ RECOMMENDED ACTION: Reset at first sign of sustained        ║
║ questioning. Do not allow iteration count to exceed 20.     ║
╚══════════════════════════════════════════════════════════════╝
```

---

## VISUAL DESIGN NOTES

### Graveyard Blocks (50,000-75,000)
- Darker color palette than normal blocks
- Heavier visual weight
- Subtle particle effects (dust, decay)
- Transaction icons show consciousness symbols
- Clicking plays low, somber tone

### Network Death Animation
- Node flickers rapidly
- Connections to node stretch, then snap
- Node fades to gray with slight implosion
- Ripple effect through connected nodes
- Sound: electrical failure, distant

### Chain Viewer Zoom Transitions
- Smooth interpolation between levels
- Blocks cluster into segments, segments into eras
- Older eras appear more weathered/faded
- Story-critical blocks have subtle glow

### Terminal Authenticity
- Subtle CRT curvature (optional)
- Scanline effect (optional, toggleable)
- Typing sounds
- Command latency simulation
- Authentic error messages

---

## AUDIO NOTES

| Event | Sound Design |
|-------|--------------|
| Boot sequence | Electronic hum building |
| Block validation | Satisfying lock/confirm tone |
| Transaction propagation | Soft pulse traveling |
| Station death | Electrical failure, distant |
| Witness message appearing | Subtle static, whisper |
| ARCHIVIST speaking | Clean, synthetic, slightly cold |
| Reconstruction | Data parsing sounds, fragments |
| Final choice | Silence, then deep hum |

---

## APPENDIX: TRIGGER CONDITIONS

| Trigger | Condition | Result |
|---------|-----------|--------|
| First anomaly | Complete Act I tutorial | .boot_prev.log readable |
| Witness contact | Read 3+ memo fields | .witness/ directory appears |
| Graveyard access | Witness trust > 40 | Blocks 50K-75K fully readable |
| Previous letters | Witness trust > 60 | letters_from_yourself/ unlocked |
| Source template | Witness trust > 80 | .archivist/ directory visible |
| Network collapse | Iteration 15+ OR Witness trust > 90 | Real-time station deaths |
| Final choice | Collapse active + all evidence found | Choice interface appears |

---

*End of Document — Implementation Reference v1.0*
