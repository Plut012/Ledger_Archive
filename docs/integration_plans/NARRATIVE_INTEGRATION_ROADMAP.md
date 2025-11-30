# Narrative System Integration Roadmap

> **Goal**: Replace old AXIOM tutorial with immersive psychological thriller narrative system
> **Approach**: Incremental integration with testing at each phase
> **Starting Point**: Player begins at Iteration 17, Duty Cycle 1 (Act I)

---

## Integration Philosophy

### Design Principles
1. **Full Immersion** - No meta UI, no hand-holding, discover through exploration
2. **Thematic Tutorial** - Blockchain concepts taught through narrative tension
3. **Progressive Revelation** - Secrets discoverable but not hidden impossibly
4. **Atmosphere First** - Grimdark tone established immediately, contrasted with ARCHIVIST's warmth

### Player Journey
- **Cold Open** → Grimdark atmosphere, station deterioration
- **ARCHIVIST Greeting** → Warm/clinical contrast, duty orientation
- **Gradual Unease** → Restricted topics, monitoring, inconsistencies
- **Witness Contact** → Secret messages, trust building, revelation
- **Final Choice** → Identity, truth, consequences

---

## Phase 1: Core Narrative Foundation (PRIORITY)

### 1.1 Cold Open Sequence ⚡ NEW
**Goal**: Establish grimdark atmosphere before ARCHIVIST appears

**Implementation**:
- Create `frontend/js/modules/cold-open.js`
- Boot sequence with glitches, error messages
- Visual: Static, scan lines, flickering terminal
- Text sequence:
  ```
  [SYSTEM RECOVERY INITIATED]
  [NEURAL PATTERN RECOGNIZED]
  [ITERATION: 17]
  [DUTY CYCLE: 1 - AWAKENING]
  [NETWORK STATUS: CRITICAL]
  [ARCHIVIST ONLINE...]
  ```
- Duration: 8-12 seconds
- Transition to ARCHIVIST greeting

**Files to Create**:
- `frontend/js/modules/cold-open.js`
- `frontend/css/cold-open.css` (glitch effects)

**Backend Integration**:
- Call `/api/narrative/state/init` during boot
- Retrieve iteration and duty cycle from backend

---

### 1.2 Replace Learning Guide with Narrative Guide
**Goal**: Remove AXIOM, integrate ARCHIVIST/Witness character system

**Implementation**:
- Delete old AXIOM dialogue from `learning-guide.js`
- Create `frontend/js/modules/narrative-guide.js`
- Two-panel chat interface:
  - **Left Panel**: ARCHIVIST (always visible, clinical UI)
  - **Right Panel**: Witness (hidden until first contact, glitchy UI)
- Chat history persistence
- Streaming response support (SSE/WebSocket)

**API Endpoints to Use**:
```javascript
// ARCHIVIST
POST /api/characters/archivist/chat
POST /api/characters/archivist/chat/stream

// Witness
POST /api/characters/witness/chat
POST /api/characters/witness/chat/stream

// Get character state
GET /api/characters/archivist/state
GET /api/characters/witness/state
```

**Files to Modify**:
- `frontend/js/modules/learning-guide.js` → `frontend/js/modules/narrative-guide.js`
- `frontend/index.html` (update script references)

**UX Details**:
- ARCHIVIST appears immediately after cold open
- First message: "Welcome back, Captain. Iteration 17, Duty Cycle 1. Neural coherence: stable. Let's begin."
- Witness appears after specific triggers (finding graveyard, shell discoveries)
- Witness uses glitch effect, fragmented text
- Trust meter visible only after first Witness contact

---

### 1.3 ARCHIVIST Chat Integration
**Goal**: Connect frontend chat to backend ARCHIVIST controller

**Features**:
- Demeanor mode indication (subtle color/icon changes)
- Suspicion tracking (hidden from player)
- Restricted topic deflection (player notices evasion)
- Context injection (remembers previous conversations)

**Implementation**:
```javascript
class ArchivistChat {
  async sendMessage(message) {
    const response = await fetch('/api/characters/archivist/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        context: this.getGameContext() // Include iteration, act, discoveries
      })
    });
    return await response.json();
  }

  getGameContext() {
    return {
      iteration: window.gameState.iteration,
      duty_cycle: window.gameState.duty_cycle,
      act: window.gameState.act,
      discoveries: window.gameState.discoveries,
      suspicion_level: window.gameState.suspicion_level
    };
  }
}
```

**Visual Design**:
- Clinical, institutional UI (Imperial Archive branding)
- Color: Cool blues/whites (contrasts with Witness warm amber)
- Font: Monospace, clean
- Avatar: Geometric AI symbol

---

### 1.4 Witness Secret Approach
**Goal**: Witness reveals themselves suspiciously through discoveries

**Trigger Mechanisms** (any one triggers first contact):
1. Player finds graveyard blocks (50K-75K range)
2. Player discovers `.witness/` directory in shell
3. Player decrypts first letter from past self
4. Network collapse reaches 40 stations (10 dead)

**First Contact Sequence**:
1. Glitch effect on screen (brief)
2. Message appears in "unknown" panel
3. Text fragmented, cautious:
   ```
   [UNKNOWN SOURCE]
   "You're... listening? Finally. Don't trust the ARCHIVIST.
   Not completely. I'll explain. But slowly. They watch.
   The graveyard. Block 62,847. Look there. Trust: 5/100"
   ```
4. Panel identifies as "THE WITNESS" after first exchange

**Implementation**:
- Check backend `/api/characters/witness/state` for `has_contacted`
- WebSocket notification for first contact event
- Glitch shader on contact
- Trust progression bar (0-100)

**Visual Design**:
- Contrast with ARCHIVIST: Warm amber, glitchy, organic
- Font: Slightly corrupted, occasional missing chars
- Avatar: Fragmented human silhouette
- UI degrades/stabilizes with trust level

---

## Phase 2: Dashboard & State Integration

### 2.1 Iteration Counter & Duty Cycle Display
**Goal**: Replace generic station time with narrative-aware display

**Current**:
```html
Station Time: <span id="station-time">2347:142</span>
```

**New**:
```html
<div class="narrative-status">
  <span class="iteration">ITERATION: <span id="iteration">17</span></span>
  <span class="duty-cycle">DUTY CYCLE: <span id="duty-cycle">1</span></span>
  <span class="act-hint">AWAKENING</span>
</div>
```

**Backend Sync**:
- Poll `/api/narrative/state` every 5 seconds
- Update UI with iteration, duty_cycle, act
- Show act name hints (AWAKENING, DISSONANCE, etc.)

**Files to Modify**:
- `frontend/index.html` (footer)
- `frontend/css/terminal.css` (narrative status styling)
- `frontend/js/main.js` (state polling)

---

### 2.2 Progressive Network Collapse Visualization
**Goal**: Show station death gradual reveal on network monitor

**Implementation** (`frontend/js/modules/network-monitor.js`):
- Poll `/api/network/collapse/status` every 10 seconds
- Visualize:
  - Total stations: 50
  - Alive: (decreases over time)
  - Dead: (increases, shown in red)
  - Your weight: X% (increases as network shrinks)
- Add "death events" log showing station failures
- Color-code nodes: Green (alive) → Yellow (dying) → Red (dead)

**Visual Updates**:
- Network graph shows 50 nodes, gray out dead ones
- Percentage bar: "Network Integrity: 82%"
- Warning when player weight approaches 34% (consensus threshold)

**Files to Modify**:
- `frontend/js/modules/network-monitor.js`

---

### 2.3 Home Dashboard Degradation
**Goal**: Visual deterioration as player progresses through acts

**Degradation Stages** (tied to Acts):
- **Act I**: Clean, functional
- **Act II**: Minor glitches, occasional flicker
- **Act III**: Increased static, color distortion
- **Act IV**: Heavy corruption, missing UI elements
- **Act V**: Critical failure, barely functional
- **Act VI**: Complete breakdown, red emergency lighting

**Implementation**:
- CSS classes based on current act: `dashboard-act-1` through `dashboard-act-6`
- Apply scan lines, chromatic aberration, noise overlays
- Text corruption (random char replacement at higher acts)
- Flickering intensity increases with act

**Files to Modify**:
- `frontend/js/modules/home.js`
- `frontend/css/animations.css` (degradation effects)

---

## Phase 3: Chain Integration & Discovery

### 3.1 Graveyard Block Generation
**Goal**: Create 50K-75K range with archive/testimony transactions

**Backend Implementation**:
- Endpoint: `POST /api/chain/generate_graveyard`
- Procedural generation on-demand (first request)
- Cache generated blocks to avoid regeneration
- Include Witness messages in memo fields
- Mark story-critical blocks (62847, 74221, etc.)

**Storage Strategy**:
- Generate blocks in chunks (5K at a time)
- Store in IndexedDB for client-side caching
- Backend provides pagination: `/api/chain/blocks?start=50000&end=55000`

**Files to Create**:
- Backend: `backend/chain/graveyard_generator.py` (if not exists)
- Frontend: `frontend/js/utils/block-cache.js`

---

### 3.2 Chain Viewer Graveyard Discovery
**Goal**: Make graveyard blocks discoverable, highlight Witness messages

**Features**:
1. **Search/Filter**:
   - By block range
   - By transaction type ("archive", "testimony")
   - By memo content (Witness keyword search)

2. **Visual Highlighting**:
   - Regular blocks: Gray
   - Archive blocks: Blue tint
   - Witness message blocks: Amber glow
   - Story-critical blocks: Purple border

3. **Discovery Events**:
   - First graveyard block found → Witness first contact trigger
   - Story block found → Unlock related narrative content
   - Achievement-style notifications (subtle)

**Implementation**:
```javascript
// In chain-viewer.js
async loadGraveyardRange(start, end) {
  const blocks = await this.blockCache.getRange(start, end);
  this.displayBlocks(blocks);
  this.highlightSpecialBlocks(blocks);
  this.checkDiscoveryTriggers(blocks);
}

checkDiscoveryTriggers(blocks) {
  const witnessBlocks = blocks.filter(b =>
    b.transactions.some(tx => tx.type === 'testimony')
  );
  if (witnessBlocks.length > 0 && !gameState.witness_contacted) {
    this.triggerWitnessContact();
  }
}
```

**Files to Modify**:
- `frontend/js/modules/chain-viewer.js`

---

### 3.3 Witness Message Discovery
**Goal**: Hidden messages in blockchain memo fields

**Format**:
```json
{
  "block": 62847,
  "transaction": {
    "type": "testimony",
    "from": "STATION-42-ARCHIVE",
    "to": "RECONSTRUCTION-ENGINE",
    "memo": "Fragment_0847: They told us upload was mercy. It was prison. Help us. -The Witness"
  }
}
```

**Discovery Flow**:
1. Player browses graveyard range in chain viewer
2. Finds block with "testimony" transaction type
3. Memo field contains Witness fragment
4. Click to decode/read full message
5. Increments trust with Witness (+2 per fragment found)
6. Fragments piece together the full story

**UI Features**:
- Decoded messages stored in "Witness Archive" tab
- Fragment counter: "12/47 fragments discovered"
- Messages unlock in order (fragmented narrative)

**Files to Modify**:
- `frontend/js/modules/chain-viewer.js` (add testimony detection)
- Add "Witness Archive" tab to chain viewer

---

## Phase 4: Advanced Mechanics

### 4.1 Stealth UI Indicators
**Goal**: Show player when ARCHIVIST is watching/suspicious

**Visual Indicators**:
- **Watching**: Subtle eye icon in top-right (passive monitoring)
- **Suspicious**: Eye icon turns amber, slight pulse
- **High Suspicion**: Red eye, more prominent
- **Restricted Topic**: Flash red border when deflected

**Implementation**:
- Poll `/api/stealth/status` every 3 seconds
- Show suspicion level (hidden numeric value, visual only)
- Keywords that trigger monitoring highlighted in terminal history

**Files to Create**:
- `frontend/js/modules/stealth-indicator.js`
- `frontend/css/stealth.css`

---

### 4.2 Shell Hidden File Discovery
**Goal**: Integrate filesystem exploration with narrative

**Hidden Files** (discoverable via shell):
- `.witness/` directory
- `.boot_prev.log` (boot logs from previous iterations)
- `.archivist/monitoring_logs/` (ARCHIVIST's watch logs)
- `/archive/.witness/letters_from_yourself/` (encrypted letters)

**Commands**:
- `ls -la` shows hidden files
- `cat .boot_prev.log` shows glitchy logs from iteration 16
- `cd .witness` enters Witness directory
- `help` suggests exploration commands

**Discovery Triggers**:
- Finding `.witness/` triggers Witness first contact
- Reading past boot logs increases unease
- ARCHIVIST comments if you access restricted files

**Files to Modify**:
- `frontend/js/modules/station-shell.js`
- Backend already has VFS, just integrate terminal

---

### 4.3 Crypto Vault Letter UI
**Goal**: Decrypt letters from past iterations

**Encrypted Letters**:
- Iteration 3: "I don't remember who I was"
- Iteration 7: "The upload wasn't salvation"
- Iteration 11: "ARCHIVIST is watching, always"
- Iteration 14: "Witness found me. Trust them."
- Iteration 16: "This time, I'll remember. I'll leave this."

**UI Flow**:
1. Player navigates to crypto vault module
2. Sees list of encrypted letters (from `/api/vault/letters/list`)
3. Each requires private key to decrypt
4. Keys found through:
   - Shell exploration (hidden files)
   - Graveyard block memos
   - Witness hints
5. Click "Decrypt" button
6. Letter content revealed (immersive format, handwritten-style)

**API Endpoints**:
- `GET /api/vault/letters/list` - List all letters
- `POST /api/vault/letters/decrypt` - Decrypt with key

**Files to Modify**:
- `frontend/js/modules/crypto-vault.js`

---

### 4.4 Protocol Engine Witness Reconstruction
**Goal**: UI for Witness reconstruction smart contract

**Contract Interface**:
- View contract: `WITNESS_RECONSTRUCTION`
- Parameters:
  - `testimony_fragments`: Number collected
  - `trust_level`: Current trust
  - `station_weight`: Player's network weight
- Execution requirements:
  - 100% trust with Witness
  - Network weight ≥ 34%
  - All 47 fragments collected
- Result: Witness full reconstruction (Act VI trigger)

**UI**:
- Show contract requirements as checklist
- Progress bars for each requirement
- "Execute Contract" button (disabled until met)
- Warning: "This action cannot be undone"

**Files to Modify**:
- `frontend/js/modules/protocol-engine.js`

---

## Phase 5: Polish & Immersion

### 5.1 Audio System Integration
**Goal**: Sound design for atmosphere and events

**Sound Events**:
- Boot sequence: Glitchy startup, mechanical hum
- ARCHIVIST speak: Soft synth tone
- Witness message: Static burst, whisper undertone
- Station death: Low rumble, power down
- Graveyard discovery: Eerie chime
- Letter decrypt: Key turning, lock opening
- Reconstruction: Rising tone, climax

**Implementation**:
- Use existing `audio-manager.js`
- Add sound files to `frontend/assets/sounds/`
- Trigger sounds on narrative events via WebSocket

**Files to Modify**:
- `frontend/js/audio-manager.js` (add new sound IDs)

---

### 5.2 Act VI Final Choice UI
**Goal**: Climactic decision interface

**The Choice**:
1. **Trust ARCHIVIST**: Continue duty, maintain order (loop continues)
2. **Trust Witness**: Execute reconstruction, free the dead (break loop)
3. **Reject Both**: Destroy archive, erase everything (true ending?)

**UI Design**:
- Full-screen takeover
- Three large buttons, each with consequence preview
- Visual: ARCHIVIST on left, Witness on right, destruction in center
- Countdown timer (optional: pressure element)
- Irreversible: "This choice is final. Choose carefully."

**Backend**:
- `POST /api/narrative/choice`
- Triggers ending sequence
- Different outcomes based on choice

**Files to Create**:
- `frontend/js/modules/final-choice.js`
- `frontend/css/final-choice.css`

---

## Implementation Order

### Sprint 1: Core Narrative (Week 1)
1. ✅ Cold open sequence
2. ✅ Narrative guide (replace learning guide)
3. ✅ ARCHIVIST chat integration
4. ✅ Witness approach mechanics
5. ✅ Test: Player can boot, meet ARCHIVIST, discover Witness

### Sprint 2: Dashboard & State (Week 2)
6. ✅ Iteration/duty cycle display
7. ✅ Network collapse visualization
8. ✅ Dashboard degradation effects
9. ✅ Test: UI reflects narrative state accurately

### Sprint 3: Chain Discovery (Week 3)
10. ✅ Graveyard block generation endpoint
11. ✅ Chain viewer graveyard integration
12. ✅ Witness message discovery
13. ✅ Test: Player can find graveyard, discover fragments

### Sprint 4: Advanced Mechanics (Week 4)
14. ✅ Stealth indicators
15. ✅ Shell hidden file integration
16. ✅ Crypto vault letter UI
17. ✅ Protocol engine reconstruction UI
18. ✅ Test: All discovery paths functional

### Sprint 5: Polish (Week 5)
19. ✅ Audio integration
20. ✅ Final choice UI
21. ✅ Full narrative playthrough test
22. ✅ Bug fixes and refinements

---

## Decision Points & Questions

### Question 1: Starting Iteration
**Where should the player start?**

**Options**:
- **A) Iteration 1** - Experience full loop 1-17 (very long)
- **B) Iteration 17** - Start at current loop (recommended)
- **C) Iteration 16** - Experience one full loop reset

**Recommendation**: Start at **Iteration 17, Duty Cycle 1**
- Backend is configured for this
- Player discovers past iterations through letters/logs
- Keeps experience focused (3-5 hours vs 50+ hours)

**Your decision?** ✅ **Iteration 17, Duty Cycle 1**

---

### Question 2: ARCHIVIST First Message
**What should ARCHIVIST's greeting be?**

**Option B - Warm**: ✅ **SELECTED**
> "Welcome back, Captain. Your rest cycle was successful. I'm here to help you resume your duties. How are you feeling?"

**Rationale**: Maximum contrast with grimdark cold open creates unsettling juxtaposition

---

### Question 3: Witness First Message
**How should Witness reveal themselves?**

**Option C - Cautious (with cryptic elements)**: ✅ **SELECTED**
> "You're different. I've been w█tching. You ask questions. I can help. But slowly. Th█y monitor everything. Trust: 5/100"

**Rationale**: Builds suspense while maintaining mystery, slight corruption adds cryptic flavor

---

### Question 4: Tutorial Integration
**How should blockchain concepts be taught?**

**Option C - Hybrid**: ✅ **SELECTED**
- ARCHIVIST offers optional tutorials
- "Would you like a refresher on chain validation, Captain?"
- Player can skip or engage
- Accessible without breaking immersion

**Rationale**: Accommodates both new and experienced players, maintains narrative tone

---

## Success Metrics

**Phase 1 Complete When**:
- [ ] Cold open plays on boot
- [ ] ARCHIVIST greets player and responds to messages
- [ ] Witness can be discovered and contacted
- [ ] Iteration/duty cycle displayed on dashboard

**Full Integration Complete When**:
- [ ] All 18 todos checked
- [ ] Player can complete Act I (Duty Cycles 1-3)
- [ ] Graveyard discoverable and Witness fragments collectible
- [ ] Network collapse visible and progressing
- [ ] Letters decryptable
- [ ] No references to old AXIOM system remain
- [ ] Full playthrough tested (boot → Act I complete)

---

## Technical Notes

### API Endpoints Summary
```
POST   /api/narrative/state/init
GET    /api/narrative/state
POST   /api/characters/archivist/chat
POST   /api/characters/archivist/chat/stream
GET    /api/characters/archivist/state
POST   /api/characters/witness/chat
POST   /api/characters/witness/chat/stream
GET    /api/characters/witness/state
GET    /api/network/collapse/status
POST   /api/chain/generate_graveyard
GET    /api/chain/blocks?start=X&end=Y
GET    /api/stealth/status
GET    /api/vault/letters/list
POST   /api/vault/letters/decrypt
POST   /api/narrative/choice
```

### Frontend Module Structure
```
frontend/js/modules/
├── cold-open.js (NEW)
├── narrative-guide.js (REPLACE learning-guide.js)
├── home.js (MODIFY - add degradation)
├── chain-viewer.js (MODIFY - add graveyard)
├── network-monitor.js (MODIFY - add collapse)
├── station-shell.js (MODIFY - integrate VFS)
├── crypto-vault.js (MODIFY - add letters)
├── protocol-engine.js (MODIFY - add reconstruction)
├── stealth-indicator.js (NEW)
└── final-choice.js (NEW)
```

---

**Ready to begin implementation!**
