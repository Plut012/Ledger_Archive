# UI Specification: Interstellar Archive Terminal

---

## Overview

The Interstellar Archive Terminal presents a single-window interface simulating a retro computer terminal. All interactions occur within this constrained viewport, creating an immersive experience of operating a workstation at Archive Station Alpha. The UI never "breaks" the terminal metaphor - no modern browser chrome, no breaking the fourth wall.

---

## Design Principles

### Visual Philosophy

1. **Terminal Authenticity**
   - Everything feels like it's happening on a real terminal
   - No modern UI paradigms (dropdowns, modals, etc.)
   - Text-based navigation with visual enhancements
   - Monospace fonts and grid-based layouts

2. **Minimalist Aesthetic**
   - Limited color palette (2-4 colors maximum)
   - Clean geometric shapes for visualizations
   - Generous whitespace (negative space)
   - No gradients, shadows, or effects (except CRT scanlines)

3. **Retro Pixel Style**
   - 8x8 or 16x16 pixel icons where needed
   - Crisp, aliased edges (no anti-aliasing on graphics)
   - Low-resolution "blocky" aesthetic
   - ASCII art for decorative elements

4. **Information Density**
   - Pack information efficiently without clutter
   - Multiple panels showing different data streams
   - Clear visual hierarchy through spacing and boxing
   - Essential information always visible

---

## Layout Structure

### Main Terminal Window

```
┌─────────────────────────────────────────────────────────────────────┐
│ ◉ ARCHIVE STATION ALPHA :: INTERSTELLAR LEDGER TERMINAL v2.1       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────┐  ┌──────────────────────────────────────┐  │
│  │   NAVIGATION       │  │        MAIN VIEWPORT                 │  │
│  │                    │  │                                      │  │
│  │  > Chain Viewer    │  │                                      │  │
│  │    Network Monitor │  │                                      │  │
│  │    Crypto Vault    │  │      (Context-Dependent Content)    │  │
│  │    Protocol Engine │  │                                      │  │
│  │    Econ Simulator  │  │                                      │  │
│  │                    │  │                                      │  │
│  │  [SYSTEM STATUS]   │  │                                      │  │
│  │  Network: ████░    │  │                                      │  │
│  │  Sync: 100%        │  │                                      │  │
│  │  Height: #1337     │  │                                      │  │
│  └────────────────────┘  └──────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ CONSOLE                                                       │  │
│  │ > _                                                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  [HELP] [CLEAR] [RESET]                    Station Time: 2347:142  │
└─────────────────────────────────────────────────────────────────────┘
```

### Layout Regions

**1. Header Bar**
- Station identifier and software version
- Always visible, establishes context
- Minimal decoration (just text and border)

**2. Navigation Panel (Left)**
- Module selector
- System status indicators
- Connection info
- 20-25% of width

**3. Main Viewport (Center-Right)**
- Primary interaction area
- Changes based on active module
- 75-80% of width
- Can be subdivided into sub-panels

**4. Console (Bottom)**
- Command input area
- Output log for operations
- 3-5 lines tall
- Scrollable history

**5. Footer**
- Quick action buttons
- System time/date
- Minimal status info

---

## Color Schemes

### Primary Options

**Scheme 1: Classic Amber**
- Background: `#1a0f00` (dark brown-black)
- Primary Text: `#ffb000` (amber)
- Highlights: `#ffd700` (bright amber)
- Dimmed: `#8b6914` (dark amber)

**Scheme 2: Phosphor Green**
- Background: `#0a0f0a` (near black)
- Primary Text: `#33ff33` (bright green)
- Highlights: `#66ff66` (lighter green)
- Dimmed: `#1a5c1a` (dark green)

**Scheme 3: Archive Blue** (Recommended)
- Background: `#0a0e1a` (deep space blue)
- Primary Text: `#4af2ff` (cyan)
- Highlights: `#80ffff` (bright cyan)
- Accents: `#ff6b35` (orange for warnings/alerts)
- Dimmed: `#1a4d5c` (dark cyan)

**Scheme 4: Dual-Tone**
- Background: `#000000` (true black)
- Primary Text: `#00ff00` (green)
- Secondary Text: `#ffff00` (yellow)
- Alerts: `#ff0000` (red)

### CRT Effects (Optional, Subtle)

- Scanline overlay: 1-2px horizontal lines at 10-20% opacity
- Phosphor glow: 2-4px text-shadow in matching color at 20% opacity
- Screen curve: Very subtle border-radius on terminal container
- Flicker: Extremely subtle (5-10ms) opacity animation on page load only

---

## Typography

### Font Selection

**Primary Font: Monospace Required**

Options:
1. **"Courier New", monospace** - Universal, authentic
2. **"Consolas", monospace** - Modern but clean
3. **"IBM Plex Mono"** - Open source, excellent readability
4. **"VT323"** (Google Font) - Authentic retro terminal look
5. **"Press Start 2P"** (Google Font) - Pixel/arcade style (maybe too stylized)

**Recommended: VT323 or IBM Plex Mono**

### Font Sizing

- Base terminal text: 14-16px
- Headers: 18-20px (just slightly larger, or use ASCII art)
- Console: 13-14px (slightly smaller, more data density)
- Minimum for readability: 12px

### Text Rendering

- Letter-spacing: 0-1px (monospace needs tight spacing)
- Line-height: 1.4-1.6 (breathing room for readability)
- Text-rendering: optimize-legibility
- Font-smoothing: none (keeps it crisp and pixelated)

---

## Module-Specific Layouts

### 1. Archive Chain Viewer

```
┌──────────────────────────────────────────────────────────┐
│ ARCHIVE CHAIN VIEWER                                     │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  [CHAIN VISUALIZATION - Horizontal scrolling]            │
│  ┌───┐    ┌───┐    ┌───┐    ┌───┐    ┌───┐             │
│  │ 0 │───→│ 1 │───→│ 2 │───→│ 3 │───→│ 4 │             │
│  └───┘    └───┘    └───┘    └───┘    └───┘             │
│                              ↑ selected                   │
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │ BLOCK #3 DETAILS                                │    │
│  │                                                  │    │
│  │ Hash:      0x4f2a8b1c...                        │    │
│  │ Prev Hash: 0x8d3c9e2f...                        │    │
│  │ Timestamp: 2347.142.08:42:13                    │    │
│  │ Nonce:     187432                                │    │
│  │ Difficulty: ████████░░ (8/10)                   │    │
│  │ Tx Count:  42                                    │    │
│  │                                                  │    │
│  │ [INSPECT] [MODIFY] [VALIDATE CHAIN]             │    │
│  └─────────────────────────────────────────────────┘    │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### 2. Network Lattice Monitor

```
┌──────────────────────────────────────────────────────────┐
│ NETWORK LATTICE MONITOR                                  │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  [NETWORK TOPOLOGY]                                      │
│                                                           │
│         ●────────────●                                   │
│        Earth      Mars                                   │
│          │          │                                    │
│          │    ●─────┴──●                                │
│          │   Jupiter  Saturn                             │
│          │               │                               │
│          ●───────────────●                               │
│        Alpha       Proxima                               │
│        Centauri                                          │
│                                                           │
│  [NODE DETAILS]              [TRANSACTION POOL]          │
│  Selected: Earth             3 pending transmissions     │
│  Status: ◉ SYNCED            ┌────────────────────┐     │
│  Height: 1337                │ tx_4f2a... 0.5 ARC │     │
│  Peers: 4/6                  │ → Jupiter          │     │
│  Latency: 8ms                └────────────────────┘     │
│                                                           │
│  [SIMULATE PARTITION] [FORCE SYNC] [ADD NODE]            │
└──────────────────────────────────────────────────────────┘
```

### 3. Cryptographic Vault

```
┌──────────────────────────────────────────────────────────┐
│ CRYPTOGRAPHIC VAULT                                      │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  [KEY MANAGEMENT]                                        │
│  ┌────────────────────────────────────────────────┐     │
│  │ Active Keypair: #1                             │     │
│  │                                                 │     │
│  │ Public Key:                                     │     │
│  │ 04a1b2c3d4e5f6...                              │     │
│  │                                                 │     │
│  │ Address:                                        │     │
│  │ 0x742d35Cc6634C0532925a3b844Bc9e7595f0aAc7    │     │
│  │                                                 │     │
│  │ [GENERATE NEW] [EXPORT] [SIGN MESSAGE]         │     │
│  └────────────────────────────────────────────────┘     │
│                                                           │
│  [TRANSACTION BUILDER]                                   │
│  From:    0x742d...                                      │
│  To:      0x891f...                                      │
│  Amount:  1.5 ARC                                        │
│  Gas:     21000                                          │
│                                                           │
│  [CREATE TX] [SIGN] [BROADCAST]                          │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### 4. Protocol Execution Engine

```
┌──────────────────────────────────────────────────────────┐
│ PROTOCOL EXECUTION ENGINE                                │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  [CONTRACT CODE]           [EXECUTION TRACE]             │
│  ┌──────────────────┐     ┌────────────────────────┐   │
│  │ contract Storage │     │ Step 1: PUSH 0x01      │   │
│  │ {                │     │ Stack: [1]             │   │
│  │   uint counter;  │     │                        │   │
│  │                  │     │ Step 2: PUSH 0x02      │   │
│  │   function inc() │     │ Stack: [1, 2]          │   │
│  │   {             │     │                        │   │
│  │     counter++;   │     │ Step 3: ADD            │   │
│  │   }              │     │ Stack: [3]             │   │
│  │ }                │     │                        │   │
│  └──────────────────┘     │ Gas Used: 142          │   │
│                            └────────────────────────┘   │
│  [STATE VISUALIZATION]                                   │
│  Storage Slot 0: 0x0000...0003 (counter = 3)            │
│                                                           │
│  [DEPLOY] [CALL FUNCTION] [STEP THROUGH]                 │
└──────────────────────────────────────────────────────────┘
```

### 5. Economic Simulator

```
┌──────────────────────────────────────────────────────────┐
│ ECONOMIC SIMULATOR                                       │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  [LIQUIDITY POOL - ARC/ETH]                              │
│                                                           │
│         ARC                    ETH                       │
│      ┌────────┐             ┌────────┐                  │
│      │ 1000.0 │◄────────────►│  10.0  │                  │
│      └────────┘             └────────┘                  │
│                                                           │
│  Price: 100 ARC per ETH                                  │
│  K (constant product): 10,000                            │
│                                                           │
│  [SWAP INTERFACE]                                        │
│  Input:  [ 1.0 ] ETH                                     │
│  Output: [ 90.9 ] ARC (estimated)                        │
│  Price Impact: 9.09%                                     │
│  Slippage: 0.5%                                          │
│                                                           │
│  [EXECUTE SWAP] [ADD LIQUIDITY] [VIEW ANALYTICS]         │
└──────────────────────────────────────────────────────────┘
```

---

## Interactive Elements

### Buttons

```
Standard: [BUTTON TEXT]
Selected: [◉ BUTTON TEXT]
Disabled: [░ BUTTON TEXT]
Loading:  [● BUTTON TEXT]
```

### Input Fields

```
Active:   Field Label: [user input here_]
Inactive: Field Label: [..................]
```

### Progress Bars

```
Empty:     [░░░░░░░░░░] 0%
Partial:   [████░░░░░░] 40%
Complete:  [██████████] 100%
```

### Status Indicators

```
Good:    ◉ SYNCED
Warning: ◐ SYNCING
Error:   ○ DISCONNECTED
Working: ● MINING
```

### Lists/Tables

```
┌────────────────────────────────────┐
│ ID    │ Status  │ Value          │
├────────────────────────────────────┤
│ #001  │ ◉ CONF  │ 1.5 ARC       │
│ #002  │ ◐ PEND  │ 0.3 ARC       │
│ #003  │ ◉ CONF  │ 2.1 ARC       │
└────────────────────────────────────┘
```

---

## Animation & Feedback

### Principles

- **Immediate Feedback:** Every action gets instant visual response
- **Purposeful Animation:** Only animate to show state change or process
- **Subtle Motion:** No bouncing, spinning, or excessive movement
- **Performance:** 60fps, no jank

### Specific Animations

1. **Transaction Propagation**
   - Dots moving along network edges
   - Speed: ~500px/second
   - Style: Dashed line that fills

2. **Block Mining**
   - Progress bar filling
   - Hash attempts counter incrementing
   - Completion: Brief flash/highlight

3. **Chain Validation**
   - Blocks highlight in sequence (green = valid)
   - If invalid: Red highlight at break point
   - Speed: 100ms per block

4. **Loading States**
   - Spinning dots: ● ○ ○ → ○ ● ○ → ○ ○ ●
   - No spinners, just tasteful ellipsis

5. **Text Typing Effect** (Optional)
   - New console messages type out character by character
   - Fast (50ms per char), skippable
   - Only for dramatic moments, not every message

---

## Technical Implementation

### Frontend Stack

**Core Technologies:**
- **HTML5** - Semantic structure
- **CSS3** - All styling, grid/flexbox layouts, animations
- **Vanilla JavaScript** - Interactivity, no frameworks initially
- **Canvas API** - Complex visualizations (network graphs, chain viewer)

**Optional Enhancements:**
- **Web Audio API** - Retro sound effects (beeps, boops)
- **LocalStorage** - Save user progress/state
- **Service Workers** - Offline capability (stretch goal)

### Frontend Architecture

```
/frontend
  /css
    main.css          # Base styles, layout
    terminal.css      # Terminal-specific styling
    modules.css       # Module-specific styles
    animations.css    # All animations
  /js
    main.js           # App initialization, routing
    terminal.js       # Terminal UI logic
    websocket.js      # Real-time communication
    /modules
      chain-viewer.js
      network-monitor.js
      crypto-vault.js
      protocol-engine.js
      econ-simulator.js
  /assets
    /fonts
    /icons          # Pixel art icons
  index.html        # Single-page app
```

### CSS Approach

**Structure:**
- CSS Grid for main layout (terminal regions)
- Flexbox for component internal layouts
- CSS Variables for theming
- No preprocessors (SASS/LESS) - keep it simple

**Example Variable Structure:**
```css
:root {
  --color-bg: #0a0e1a;
  --color-primary: #4af2ff;
  --color-highlight: #80ffff;
  --color-accent: #ff6b35;
  --color-dim: #1a4d5c;
  
  --font-main: 'VT323', monospace;
  --font-size-base: 16px;
  --font-size-large: 20px;
  --font-size-small: 14px;
  
  --spacing-unit: 8px;
  --border-width: 2px;
  --border-radius: 0px;
}
```

### JavaScript Approach

**Philosophy:**
- Vanilla JS, no frameworks (React/Vue) initially
- Module pattern for organization
- Event-driven architecture
- Minimal DOM manipulation

**Key Components:**
1. **TerminalUI** - Manages terminal display, navigation
2. **WebSocketClient** - Handles real-time backend communication
3. **ModuleLoader** - Dynamically loads/unloads modules
4. **StateManager** - Centralized state (blockchain data)
5. **Visualizers** - Canvas-based rendering utilities

### Backend Communication

**WebSocket Events:**
```javascript
// Frontend sends:
{
  "type": "mine_block",
  "data": { "transactions": [...] }
}

// Backend responds:
{
  "type": "block_mined",
  "data": {
    "block": { ... },
    "height": 1338,
    "timestamp": "2347.142.08:42:13"
  }
}
```

**REST API Endpoints:**
- `GET /api/chain` - Full blockchain
- `GET /api/chain/block/:hash` - Single block
- `GET /api/network/nodes` - Network topology
- `POST /api/transaction` - Submit transaction
- `GET /api/state` - Current blockchain state

---

## Responsive Considerations

**Primary Target:** Desktop browser, 1280x720 minimum

**Approach:**
- Terminal metaphor works best on larger screens
- Mobile: Consider read-only "monitoring" mode
- Tablets: Simplified single-panel view

**Not prioritized for MVP:** Full mobile responsive design

---

## Accessibility

**Basic Support:**
- Semantic HTML structure
- Keyboard navigation (tab, arrow keys, enter)
- High contrast text (inherent in retro design)
- Clear focus indicators
- Screen reader labels for interactive elements

**Future Enhancements:**
- Zoom support without breaking layout
- Alternative themes (high contrast, larger text)
- Command-line alternative to GUI interactions

---

## Performance Targets

- Initial load: < 2 seconds
- Module switching: < 200ms
- Animation frame rate: 60fps
- WebSocket latency: < 50ms
- Canvas rendering: 60fps for visualizations

---

## Browser Support

**Target:**
- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions

**No support needed:**
- Internet Explorer
- Mobile browsers (initially)

---

## Development Tools

**Recommended Setup:**
- **Code Editor:** VS Code with Live Server extension
- **Browser DevTools:** Chrome DevTools for debugging
- **Version Control:** Git
- **Local Server:** Python's `http.server` or FastAPI dev server

**Testing:**
- Manual testing in browser
- Console logging for debugging
- No automated test framework initially (keep it simple)

---

## Implementation Phases

### Phase 1: Terminal Shell
- Basic HTML structure
- CSS styling (colors, fonts, layout)
- Navigation system
- Console input/output

### Phase 2: Backend Integration
- WebSocket connection
- REST API calls
- State management
- Real-time updates

### Phase 3: First Module (Chain Viewer)
- Block visualization
- Block details display
- Interactive chain manipulation
- Validation feedback

### Phase 4: Remaining Modules
- One module at a time
- Iterative refinement
- Integration with shared state

### Phase 5: Polish
- Animations
- Sound effects (optional)
- Performance optimization
- Bug fixes and UX improvements

---

## Success Metrics

**The UI succeeds when:**
1. First-time users understand they're in a terminal immediately
2. Navigation is intuitive without instructions
3. Visual feedback is clear and immediate
4. The retro aesthetic enhances rather than hinders usability
5. Complex blockchain data is made comprehensible through visualization
6. Users can experiment freely without fear of "breaking" things

---

*"The interface is not the obstacle, but the window through which understanding flows."*
