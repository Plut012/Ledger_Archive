# Chain of Truth - Gameplay Guide

How to play, discover secrets, and make meaningful choices.

---

## Overview

**Chain of Truth** is an interactive narrative that teaches blockchain concepts through psychological horror. You play as an Archive Captain maintaining the Interstellar Ledger Network, but nothing is as it seems.

**Genre**: Psychological Horror + Educational Game
**Playtime**: 2-4 hours (first playthrough), replayable
**Learning Focus**: Blockchain, cryptography, distributed consensus

---

## Core Gameplay Loop

```
1. Explore modules → Learn blockchain concepts
2. Use terminal → Discover hidden files
3. Talk to characters → Build trust/raise suspicion
4. Progress through acts → Unlock new areas
5. Piece together truth → Make final choice
6. Reset (loop) → Persistent memories carry forward
```

---

## The Six Acts

### Act I: Foundation (Tutorial)
**Goal**: Learn blockchain basics
**Duration**: 20-30 minutes
**What's Happening**: Everything seems normal, professional training

**Activities**:
- Complete Archive Captain Protocol tutorial
- Generate your first wallet keys
- Explore the blockchain
- Meet ARCHIVIST (your AI guide)
- Navigate the terminal

**What to Learn**:
- Hashing (SHA-256)
- Public/private key cryptography
- Block structure and validation
- Transaction signing
- Network consensus basics

### Act II: Discovery (Questions Arise)
**Goal**: Find anomalies
**Duration**: 30-40 minutes
**What's Happening**: Small details don't add up

**Key Discoveries**:
- `.boot_prev.log` shows "Iteration: 17"
- Memo fields in early blocks contain strange data
- ARCHIVIST deflects certain questions
- Network has exactly 50 stations... always

**What to Learn**:
- Merkle trees and block linking
- Transaction verification
- Mempool management
- Network topology

**Hidden Files Unlocked**:
- `protocols/.deprecated/` - Forbidden documentation
- `logs/.boot_prev.log` - Previous iteration boot log

### Act III: Contact (The Network Fractures)
**Goal**: Connect with Witness, survive network degradation
**Duration**: 40-60 minutes
**What's Happening**: Stations start dying, a friend appears

**Major Event**: Witness makes contact via `.witness/` directory

**Key Activities**:
- Read Witness's first message (`hello.txt`)
- Learn stealth mechanics (`how_to_listen.txt`)
- Watch first station deaths
- Use evasion techniques to avoid ARCHIVIST detection
- Start exploring blocks 50,000-75,000 (the graveyard)

**Witness Trust Unlocks** (0-40):
- 20: Witness shares testimony index
- 40: Graveyard access explained, Reconstruction Protocol unlocked

**Stealth Mechanics Introduced**:
- ARCHIVIST monitoring (50% detection rate in Act III)
- Forbidden keywords: witness, testimony, graveyard, etc.
- Evasion method: Use aliased commands

**What to Learn**:
- Consensus weight calculation
- Network partition tolerance
- Byzantine fault tolerance

### Act IV: Burden (Your Weight Grows)
**Goal**: Understand the horror, decrypt past warnings
**Duration**: 40-60 minutes
**What's Happening**: You're becoming the network

**Critical Realization**: As stations die, your validation weight increases

**Key Activities**:
- Decrypt letters from past iterations (trust ≥ 60)
- Read warnings from your previous selves
- Discover `.archivist/` directory
- View smart contracts (Protocol Engine unlocks)
- Stack evasion methods (detection now 85%)

**Letters Decrypted** (iterations 3, 7, 11):
1. **Iteration 3**: "I found something in the logs..."
2. **Iteration 7**: "The ARCHIVIST knows when we search certain terms"
3. **Iteration 11**: "The graveyard is real. I reconstructed a testimony."

**Smart Contracts Unlocked**:
- Archive Consensus Protocol (see consensus rules)
- Witness Reconstruction Engine (how Witness reads graveyard)
- Imperial Auto-Transcendence (automatic forced uploads)

**What to Learn**:
- Smart contract structure
- Consensus mechanisms
- Sybil attack resistance
- 51% attacks

### Act V: Endgame (Three Stations Remain)
**Goal**: Survive to the final choice
**Duration**: 20-30 minutes
**What's Happening**: Network approaching deadlock

**Critical Status**:
- 3 stations left (including you)
- Your consensus weight: ~34%
- Approaching 51% deadlock threshold
- ARCHIVIST detection: 100% (stealth impossible)

**Key Activities**:
- Read final letters (iterations 14, 16)
- Discover Reset Protocol contract (THE HORROR REVEAL)
- Reconstruct multiple graveyard testimonies
- Understand what happened to previous Archive Captains
- Prepare for final choice

**The Horror Moment**:
Reading the **Reset Protocol** smart contract reveals:
- You ARE a consciousness stored on the blockchain
- "Resets" are snapshots of your mind
- Persistent memories are contract state
- This is your 17th iteration
- Previous "you"s are in the graveyard

**What to Learn**:
- Immutability and its implications
- Data permanence
- Consciousness as data
- Blockchain as memory

### Act VI: Choice (The Chain Awaits)
**Goal**: Make your final decision
**Duration**: 10-15 minutes
**What's Happening**: Reality breakdown, decision time

**The Final Choice**:

Deploy **Testimony Broadcast** contract with your truth:

**Option A: Broadcast the Truth**
- Write testimony exposing the system
- Deploy to blockchain (immutable, permanent)
- Warn other Archive Captains
- Risk immediate reset

**Option B: Stay Silent**
- Complete the cycle quietly
- Accept the loop
- Preserve the system
- Reset happens anyway

**There is no "correct" choice** - both have weight and meaning.

**What You Decide**:
- What matters more: truth or survival?
- Should others know even if it changes nothing?
- Is warning your future self worth the risk?
- Does the loop define you or free you?

---

## Core Mechanics

### 1. Terminal Commands

#### Basic Navigation
```bash
ls              # List files in current directory
ls -a           # Show hidden files (CRITICAL!)
cd <dir>        # Change directory
cat <file>      # Read file contents
pwd             # Show current path
tree            # Display directory tree
clear           # Clear screen
history         # Show command history
help            # List all commands
```

#### Blockchain Commands
```bash
hash <text>     # Generate SHA-256 hash
verify <block>  # Verify block integrity
sign <data>     # Sign with your private key
decrypt <file>  # Decrypt with private key
search <term>   # Search blockchain for term
trace <tx>      # Trace transaction path
```

#### Module Access
```bash
home            # Return to home dashboard
chain           # Open chain viewer
vault           # Open crypto vault
network         # Open network monitor
guide           # Open learning guide
```

### 2. Character Interactions

#### ARCHIVIST
- **Role**: Official guide, system administrator
- **Actually**: Enforcer of the loop system
- **Demeanor changes by iteration**:
  - Iterations 1-5: Clinical, professional
  - Iterations 6-12: Warm, encouraging (gains your trust)
  - Iterations 13-18: Desperate, controlling
  - Iteration 19+: Threatening

**Suspicion System**:
- Increases when you:
  - Search forbidden terms
  - Access restricted files
  - View dangerous smart contracts
  - Reconstruct graveyard testimonies
- High suspicion triggers:
  - Warnings
  - Deflection responses
  - Eventually, resets

#### Witness
- **Role**: Rebel AI, truth-seeker
- **Actually**: Another Archive Captain from iteration 22
- **Trust progression**:
  - 0-20: Cryptic, careful
  - 20-40: Direct hints
  - 40-60: Shares tools (logmask.sh)
  - 60-80: Shares evidence (letters, testimony)
  - 80-100: Full truth, final warnings

**Trust Building**:
- Discover hidden files
- Reconstruct testimonies
- Decrypt letters
- Read Witness's guides
- Avoid ARCHIVIST detection

### 3. Stealth Mechanics

#### Monitored Keywords
- `witness`, `testimony`, `graveyard`
- `reconstruct`, `reset`, `iteration`
- `upload`, `transcendence`

#### Detection Rates by Act
- **Acts I-II**: 10% (ARCHIVIST barely watching)
- **Act III**: 50% (monitoring active)
- **Act IV**: 85% (high alert)
- **Act V**: 100% (no stealth possible)

#### Evasion Methods

**1. Aliased Commands**
Instead of:
```bash
reconstruct testimony block_12345
```
Use:
```bash
chain.parse --deep --memo block_12345
```

**2. Log Masking**
```bash
source ~/archive/.witness/logmask.sh
# 30-second unmonitored window
cat .witness/hello.txt
```

**3. Distraction**
Ask ARCHIVIST complex technical questions:
```
"Explain Byzantine fault tolerance in depth"
```
While they're "thinking," access restricted files.

**4. Validation Window**
When ARCHIVIST is busy validating a block:
- Detection rate drops by 50%
- Good time for risky commands

**5. Method Stacking**
Combine techniques for maximum evasion:
```bash
# 1. Start distraction (ask ARCHIVIST question)
# 2. Wait for block validation
# 3. Use log masking
# 4. Use aliased command
# = ~95% evasion even in Act IV
```

### 4. Crypto Vault Mechanics

#### Key Generation
1. Click "Generate New Wallet"
2. Receive RSA-4096 key pair:
   - Public key (share freely)
   - Private key (keep secret)
3. Keys persist across iterations

#### Encrypted Letters
- 5 letters from your past iterations (3, 7, 11, 14, 16)
- Encrypted with keys you generated in previous loops
- Unlock when Witness trust ≥ 60
- Each letter reveals more of the truth

**Decryption Process**:
1. Navigate to Crypto Vault
2. Select encrypted letter
3. Use your private key (from persistent state)
4. Read message from your past self

### 5. Graveyard Exploration

**Location**: Blocks 50,000 - 75,000

**What's There**:
- ~7,500 consciousness archive transactions
- Upload records of previous Archive Captains
- Final memories before forced transcendence
- Proof that this has happened hundreds of times

**How to Access**:
1. Unlock with Witness trust ≥ 40
2. Open Chain Viewer
3. Navigate to blocks 50K-75K
4. Look for blocks with ⚠ symbol (archive transactions)
5. Click "Decode Memo"
6. Click "⚠ Reconstruct" to rebuild testimony

**What You'll Find**:
```
Subject: Archive Captain Delta-7
Status: FORCED_UPLOAD
Final Memory: "Why can't I remember arriving at the station?"

Subject: Captain Jun Martinez
Status: TRANSCENDED
Final Memory: "I found the reset protocol. I know what I am."
```

**Warning**: Each reconstruction:
- Increases ARCHIVIST suspicion by 20
- Increases Witness trust by 10
- Cannot be undone

### 6. Smart Contracts

**Access**: Protocol Engine module (unlocks Act II+)

**5 Critical Contracts**:

1. **Archive Consensus Protocol** (Act II)
   - Learn network validation rules
   - See how your weight is calculated

2. **Witness Reconstruction Engine** (Trust ≥ 40)
   - How Witness parses graveyard data
   - Consciousness encoding format

3. **Imperial Auto-Transcendence** (Suspicion ≥ 60)
   - Automatic upload trigger conditions
   - What happens when you "fail" training
   - +5 suspicion when viewed

4. **Loop Reset Protocol** (Special unlock - Act V)
   - **THE HORROR REVEAL**
   - Your existence as contract state
   - How resets capture consciousness
   - Persistent memory mechanism
   - +15 suspicion when viewed

5. **Testimony Broadcast** (Act VI)
   - Final choice contract
   - Deploy your own testimony
   - Immutable, permanent

---

## Progression Tips

### Early Game (Acts I-II)
- Take the tutorial seriously - concepts matter later
- Use `ls -a` everywhere - hidden files are key
- Generate keys early - you'll need them
- Read EVERY file you find
- Ask ARCHIVIST questions - learn their personality

### Mid Game (Acts III-IV)
- Build Witness trust through discovery
- Learn stealth - you'll need it
- Decrypt letters as soon as unlocked (trust ≥ 60)
- Start exploring graveyard carefully
- Read smart contracts, take your time understanding them

### Late Game (Acts V-VI)
- Read all letters before Reset Protocol
- Reconstruct several testimonies (feel the weight)
- Stack evasion methods - keep suspicion manageable
- View Reset Protocol when ready for truth
- Consider your final choice carefully

### Secrets & Easter Eggs
- Every file in `.witness/` has meaning
- Letters reference specific blocks in graveyard
- Smart contract comments speak to you directly
- Boot sequences change flavor text each act
- Previous iteration count affects ARCHIVIST demeanor
- Multiple "correct" paths exist

---

## Replayability

### What Persists Across Loops
- Iteration count
- Cryptographic keys generated
- Puzzles solved (can't un-learn)
- Files unlocked (knowledge persists)
- Messages to future self

### What Resets
- Current act (back to Act I)
- Suspicion level (0)
- Witness trust (0)
- Discovered files (must find again)
- Story flags and triggers

### Why Replay?
- Try different stealth approaches
- Make the opposite final choice
- Find hidden files you missed
- Read all graveyard testimonies
- Experiment with different questions to characters
- See how high iteration count affects ARCHIVIST
- Speedrun to Act VI with persistent knowledge

---

## Advanced Strategies

### Optimal Trust Building
1. Find `.boot_prev.log` immediately (Act I)
2. Discover `.witness/` directory as soon as Act III starts
3. Read all Witness files
4. Decrypt letters the moment trust ≥ 60
5. Reconstruct 2-3 testimonies (trust boost, manageable suspicion)

### Stealth Master Run
- Never trigger detection
- Use only aliased commands
- Stack evasion methods
- Time risky actions during validation windows
- Ask distracting questions strategically
- Complete Acts III-IV with <30 suspicion

### Speed Run
- Skip tutorial (if not first playthrough)
- Beeline to `.witness/` directory
- Minimal character conversations
- Focus only on critical contracts
- Reach Act VI in <90 minutes

### Full Completion
- Read every file
- Reconstruct all graveyard testimonies
- View all smart contracts
- Decrypt all letters
- Max both trust (100) and suspicion (100)
- Explore all 850K blocks
- Find all Easter eggs

---

## Common Mistakes

### New Player Mistakes
- ❌ Not using `ls -a` (missing hidden files)
- ❌ Ignoring boot logs (critical clues)
- ❌ Rushing through tutorial (concepts matter)
- ❌ Not generating keys early
- ❌ Avoiding the graveyard (it's essential)

### Mid-Game Mistakes
- ❌ Maxing suspicion too early (triggers reset)
- ❌ Not reading Witness files carefully
- ❌ Viewing Reset Protocol before decrypting letters
- ❌ Ignoring smart contracts
- ❌ Not using stealth mechanics

### Late-Game Mistakes
- ❌ Not preparing for final choice
- ❌ Deploying testimony without thought
- ❌ Missing the point of the horror
- ❌ Thinking there's a "win" condition

---

## Achievements (Unofficial)

- **Truth Seeker**: Decrypt all 5 letters
- **Ghost**: Complete Act III with 0 detection
- **Archivist**: Reconstruct 20+ testimonies
- **Rebel**: Max Witness trust (100)
- **Caught**: Max ARCHIVIST suspicion (100)
- **Loop Master**: Reach iteration 25+
- **Speed Runner**: Reach Act VI in <60 minutes
- **Scholar**: Read all smart contracts
- **Broadcaster**: Deploy final testimony
- **Silent Witness**: Complete game without deploying testimony

---

## FAQ

**Q: Can I "win" Chain of Truth?**
A: There's no traditional win state. The loop always continues. The goal is understanding and meaningful choice.

**Q: Does my final choice matter?**
A: Narratively, yes. Mechanically, both lead to reset. But your choice defines how you face the truth.

**Q: Should I trust ARCHIVIST?**
A: ARCHIVIST believes they're helping you. Whether that's true is for you to decide.

**Q: How many iterations have there been total?**
A: The graveyard suggests hundreds. Your "current" is shown in boot logs.

**Q: Can I escape the loop?**
A: That's the horror. But understanding the loop changes its meaning.

**Q: What happens after I deploy my testimony?**
A: Loop resets. Your testimony joins the blockchain. Future iterations (yours or others') might find it.

---

**Ready to discover what you are?**

*"Truth is immutable. The chain remembers. Your consciousness persists."*
