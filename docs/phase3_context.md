# Phase 3 Context: Network Monitor Module

## Quick Orientation

**Your Task:** Build Network Monitor - visualize the distributed blockchain network

**Expected Duration:** 3-4 work sessions

**Phase Status:** 🔄 READY TO START

---

## What You Inherit from Previous Phases

### ✅ Phase 1: Cryptography
- Real key generation
- Digital signatures
- Transaction signing/verification
- All crypto tests passing

### ✅ Phase 2: Crypto Vault
- Interactive wallet UI
- Transaction creation
- Signature broadcasting
- Transaction history

### ✅ Existing Infrastructure
- Terminal UI framework
- Two working modules (Chain Viewer, Crypto Vault)
- WebSocket real-time updates
- REST API

---

## Your Goal: Build Network Monitor

### What You're Building

A visual network monitor showing distributed blockchain:

```
┌────────────────────────────────────────────────────────┐
│ NETWORK LATTICE MONITOR                                │
├────────────────────────────────────────────────────────┤
│                                                         │
│        ●────────────●                                  │
│       Earth       Mars                                 │
│         │           │                                  │
│         │      ●────┴────●                             │
│         │    Jupiter  Saturn                           │
│         │                │                             │
│         ●────────────────●                             │
│       Alpha         Proxima                            │
│                                                         │
│  Selected: Earth          Mempool: 3 tx                │
│  Height: #42              ┌──────────────────┐        │
│  Peers: 3/4              │ tx_4f2a... → Jupiter       │
│  Status: ◉ SYNCED         └──────────────────┘        │
│                                                         │
│  [Broadcast TX] [Add Node] [Remove Node]               │
└────────────────────────────────────────────────────────┘
```

---

## Implementation Plan

### Part A: Backend Network Topology

**File:** `backend/network.py`

**Currently:** Placeholder with basic Node class

**Tasks:**
- [ ] Create default network topology (4-5 nodes)
- [ ] Implement broadcast_transaction() simulation
- [ ] Add sync_chain() for node synchronization
- [ ] Track propagation paths

**Default Network:**
```
Earth ←→ Mars
  ↕        ↕
Alpha ←→ Jupiter ←→ Saturn
  ↕
Proxima
```

**Implementation:**
```python
class Network:
    def __init__(self):
        self.nodes = {}
        self.connections = []
        self.create_default_topology()

    def create_default_topology(self):
        # Create 4-5 relay stations
        self.add_node(Node("earth", "Earth Station"))
        self.add_node(Node("mars", "Mars Station"))
        # ... etc

        # Connect them
        self.connect_nodes("earth", "mars")
        self.connect_nodes("earth", "alpha")
        # ... etc
```

---

### Part B: API Endpoints

**File:** `backend/main.py`

**New endpoints to add:**

```python
@app.get("/api/network/topology")
def get_topology():
    """Return nodes and connections."""
    return state.network.get_topology()

@app.get("/api/network/node/{node_id}")
def get_node_details(node_id: str):
    """Get specific node info."""
    return {
        "id": node_id,
        "status": "synced",
        "height": len(state.blockchain.chain),
        "peers": state.network.nodes[node_id].peers
    }

@app.post("/api/network/broadcast")
def broadcast_transaction(tx_data: dict):
    """Simulate transaction propagation."""
    path = state.network.broadcast(tx_data)
    return {"path": path}
```

---

### Part C: Canvas Visualization

**File:** `frontend/js/modules/network-monitor.js`

**Tasks:**
- [ ] Setup canvas element
- [ ] Define node positions (hardcoded is fine)
- [ ] Draw nodes as circles with labels
- [ ] Draw connections as lines
- [ ] Handle click events on nodes

**Node Positions (example):**
```javascript
const nodePositions = {
    earth: {x: 100, y: 150},
    mars: {x: 300, y: 150},
    jupiter: {x: 200, y: 300},
    alpha: {x: 100, y: 450},
    // ... etc
};
```

**Drawing:**
```javascript
drawNodes() {
    this.nodes.forEach(node => {
        const pos = nodePositions[node.id];

        // Draw circle
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, 20, 0, Math.PI * 2);
        ctx.strokeStyle = colors.primary;
        ctx.stroke();

        // Draw label
        ctx.fillStyle = colors.primary;
        ctx.fillText(node.label, pos.x, pos.y + 40);
    });
}
```

---

### Part D: Transaction Propagation Animation

**Animation sequence:**
1. Transaction originates at random node
2. Dot travels along edges
3. Each connected node receives it
4. Nodes flash when receiving
5. All nodes eventually have the transaction

**Implementation approach:**
```javascript
animatePropagation(tx, path) {
    // path = ["earth", "mars", "jupiter"]
    let currentEdge = 0;
    let progress = 0;

    const animate = () => {
        progress += 0.02;  // Animation speed

        if (progress >= 1) {
            // Reached next node - flash it
            this.flashNode(path[currentEdge + 1]);
            currentEdge++;
            progress = 0;
        }

        if (currentEdge < path.length - 1) {
            // Draw moving dot
            this.drawDot(path[currentEdge], path[currentEdge + 1], progress);
            requestAnimationFrame(animate);
        }
    };

    animate();
}
```

---

### Part E: Node Details Panel

**Show when node selected:**
- Node name
- Status (synced/syncing)
- Current blockchain height
- Connected peers
- Pending transactions

**Implementation:**
```javascript
selectNode(nodeId) {
    this.selectedNode = nodeId;

    // Fetch node details
    fetch(`/api/network/node/${nodeId}`)
        .then(r => r.json())
        .then(data => {
            this.renderNodeDetails(data);
        });
}

renderNodeDetails(node) {
    const panel = document.getElementById('node-details');
    panel.innerHTML = `
        Selected: ${node.id}
        Status: ${node.status}
        Height: #${node.height}
        Peers: ${node.peers.length}
    `;
}
```

---

## Files You'll Modify

```
Backend:
backend/network.py     ← Enhance network topology
backend/state.py       ← Add network to state
backend/main.py        ← Add network endpoints

Frontend:
frontend/js/modules/network-monitor.js  ← Main implementation

Estimated LOC: 250-300 total
```

---

## Success Criteria

### Phase 3 is complete when:

**Functionality:**
- [ ] Network topology displays with 4-5 nodes
- [ ] Nodes and connections are clearly visible
- [ ] Can click on node to see details
- [ ] "Broadcast TX" animates propagation
- [ ] Transaction reaches all connected nodes
- [ ] Animation is smooth (60fps)

**Code Quality:**
- [ ] Canvas code is organized
- [ ] Animation uses requestAnimationFrame
- [ ] No memory leaks (cleanup on module switch)
- [ ] Code follows project philosophy

**User Experience:**
- [ ] Network is visually clear
- [ ] Node names are thematic (Earth, Mars, etc.)
- [ ] Animation speed is appropriate (~200px/sec)
- [ ] Interactions are responsive

---

## Canvas Setup Template

```javascript
const NetworkMonitor = {
    canvas: null,
    ctx: null,
    nodes: [],
    edges: [],
    selectedNode: null,

    init(container) {
        this.render(container);
        this.setupCanvas();
        this.fetchTopology();
        this.setupEventListeners();
    },

    render(container) {
        container.innerHTML = `
            <div class="module-header">NETWORK LATTICE MONITOR</div>

            <div class="network-viz">
                <canvas id="network-canvas" width="800" height="600"></canvas>
            </div>

            <div class="network-panels">
                <div id="node-details"></div>
                <div id="tx-pool"></div>
            </div>

            <div class="action-buttons">
                <button id="btn-broadcast">Broadcast TX</button>
            </div>
        `;
    },

    setupCanvas() {
        this.canvas = document.getElementById('network-canvas');
        this.ctx = this.canvas.getContext('2d');

        // Handle clicks
        this.canvas.addEventListener('click', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            this.handleClick(x, y);
        });
    },

    async fetchTopology() {
        const res = await fetch('/api/network/topology');
        const data = await res.json();
        this.nodes = data.nodes;
        this.edges = data.connections;
        this.draw();
    },

    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.drawEdges();
        this.drawNodes();
    },

    cleanup() {
        // Stop any running animations
        // Clear canvas
    }
};
```

---

## Animation Best Practices

### Use requestAnimationFrame

```javascript
// ❌ Don't use setInterval
setInterval(() => this.draw(), 16);

// ✅ Use requestAnimationFrame
const animate = () => {
    this.draw();
    this.animationFrame = requestAnimationFrame(animate);
};
animate();

// Remember to cancel on cleanup
cleanup() {
    if (this.animationFrame) {
        cancelAnimationFrame(this.animationFrame);
    }
}
```

### Smooth Movement

```javascript
// Linear interpolation for smooth movement
function lerp(start, end, t) {
    return start + (end - start) * t;
}

// Use in animation:
const x = lerp(nodeA.x, nodeB.x, progress);
const y = lerp(nodeA.y, nodeB.y, progress);
```

---

## Testing Your Work

### Manual Testing Checklist

- [ ] Network topology displays correctly
- [ ] Can identify each node by name
- [ ] Click on node → details panel updates
- [ ] Click "Broadcast TX" → animation starts
- [ ] Dot moves smoothly along edges
- [ ] Nodes flash when receiving transaction
- [ ] Animation completes at all nodes
- [ ] No lag or stuttering
- [ ] Module switch → cleanup works

### Visual Testing

**Check these visually:**
- Node circles are evenly sized
- Labels are readable
- Connection lines are clear
- Selected node is highlighted
- Animation is at good speed
- Colors match terminal theme

---

## Common Pitfalls to Avoid

❌ **Don't** use complex graph layout algorithms (hardcode positions)
❌ **Don't** implement full P2P protocol (it's a simulation)
❌ **Don't** forget to cleanup animations on module switch
❌ **Don't** make animation too fast or too slow

✅ **Do** use thematic names (Earth, Mars, not node_1, node_2)
✅ **Do** keep network topology simple (4-5 nodes)
✅ **Do** make propagation visual and clear
✅ **Do** cancel animations in cleanup()

---

## Phase 3 Completion Checklist

*Fill this out when done - see docs/phase3_handoff.md*

---

## Need Help?

**Read these first:**
- `docs/phase3_plan.md` - Full detailed plan
- `docs/phase2_handoff.md` - What Phase 2 delivered
- `docs/ui_plan.md` - UI design specification

**Reference implementations:**
- `frontend/js/modules/chain-viewer.js` - Module structure
- Canvas API docs - For drawing reference

**Network concepts:**
- `backend/network.py` - Current network stub
- `docs/architecture.md` - System design

---

**Ready to visualize the network!** Start with `backend/network.py`

*The ledger is distributed. Truth is everywhere.* 🌌
