# Phase 3: Network Monitor Module

## Goal
Visualize the distributed nature of blockchain by showing nodes, connections, and transaction propagation across the network.

---

## What We're Building

A visual network monitor that shows:
- Nodes (archive stations) scattered across the network
- Connections between nodes
- Transaction propagation in real-time
- Sync status and block propagation

---

## Visual Design

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

## Backend Tasks

### 1. Enhance `network.py`

**Current state:** Basic Node dataclass and topology

**What to add:**

```python
class Network:
    - create_default_topology()  # Create 4-5 default nodes
    - broadcast_transaction(tx)  # Propagate to all peers
    - sync_chain(node_id)        # Sync blockchain to node
    - get_propagation_path(tx)   # Track tx route
```

**Default nodes:**
- Earth (node_0)
- Mars (node_1)
- Jupiter (node_2)
- Alpha Centauri (node_3)

**Connections:**
- Earth ↔ Mars
- Earth ↔ Alpha Centauri
- Mars ↔ Jupiter
- Jupiter ↔ Alpha Centauri

Creates a mesh topology (no single point of failure).

---

### 2. Add Network Endpoints

**File:** `main.py`

```python
@app.get("/api/network/topology")
def get_topology():
    # Return nodes and connections

@app.get("/api/network/node/{node_id}")
def get_node(node_id):
    # Return node details + its blockchain

@app.post("/api/network/broadcast")
def broadcast_transaction(tx):
    # Simulate transaction propagation
    # Return propagation path
```

---

## Frontend Tasks

### 1. Update `network-monitor.js`

**Three main sections:**

#### A) Network Visualization (Canvas)

```javascript
class NetworkViz {
    nodes: []      // {id, x, y, label}
    edges: []      // {from, to}

    drawNodes()    // Draw circles for each node
    drawEdges()    // Draw lines between nodes
    drawTxPath()   // Animate transaction traveling
    handleClick()  // Select node on click
}
```

**Rendering:**
- Canvas 2D context
- Nodes as circles with labels
- Edges as lines
- Selected node highlighted

---

#### B) Node Details Panel

**When node selected:**
```
Selected: Earth
Status: ◉ SYNCED
Height: #42
Peers: 3 (Mars, Alpha, Jupiter)
Latency: 12ms avg
```

---

#### C) Transaction Propagation

**Animation sequence:**
```
1. User clicks "Broadcast TX"
2. Show transaction originating from random node
3. Animate dot traveling along edges
4. Each node "receives" the tx (flash effect)
5. All nodes end up with tx in mempool
```

**Animation details:**
- Dot moves at ~200px/sec
- Each node flashes when tx arrives
- Use requestAnimationFrame for smooth movement

---

## Implementation Steps

### Step 1: Backend Network Setup

```
1. Create default network topology
2. Add network state to state.py
3. Implement broadcast simulation
4. Add API endpoints
5. Test with manual API calls
```

---

### Step 2: Basic Canvas Rendering

```
1. Setup canvas element
2. Define node positions (hardcoded is fine)
3. Draw nodes as circles
4. Draw edges as lines
5. Test rendering
```

---

### Step 3: Interactivity

```
1. Add click detection on canvas
2. Highlight selected node
3. Fetch and display node details
4. Update panel on selection
```

---

### Step 4: Transaction Animation

```
1. Create transaction propagation simulator
2. Animate dot along edges
3. Flash nodes as tx arrives
4. Update mempool displays
5. Test end-to-end
```

---

## Files Modified

```
backend/network.py          - Enhanced network logic
backend/state.py            - Add network state
backend/main.py             - Add network endpoints
frontend/js/modules/
  network-monitor.js        - Main implementation
```

**Total files:** 4
**Lines of code:** ~250-300

---

## Success Criteria

✅ Network topology displays with 4-5 nodes
✅ Nodes and connections are clearly visible
✅ Click on node shows its details
✅ "Broadcast TX" animates propagation
✅ Transaction reaches all connected nodes
✅ Sync status updates correctly

---

## User Flow

```
1. User opens Network Monitor
   → Sees 4 nodes connected in mesh

2. User clicks on "Earth" node
   → Details panel shows:
     - Height: #42
     - Peers: Mars, Alpha, Jupiter
     - Status: SYNCED

3. User clicks "Broadcast TX"
   → Animated dot appears on Mars
   → Travels to Jupiter
   → Jupiter flashes (received)
   → Continues to other nodes
   → All nodes flash in sequence

4. User switches to Chain Viewer
5. Clicks "Mine Block"
   → Block propagates through network
   → Heights update across all nodes
```

---

## Advanced Features (Optional)

**If time permits:**
- Add "Create Partition" button (disconnect nodes)
- Show fork when network splits
- Visualize fork resolution on reconnect
- Add latency simulation (delay propagation)

---

## Notes

- **Static layout:** Hardcode node positions (no graph layout algorithm needed)
- **Simulation only:** Network doesn't actually run multiple instances
- **Visual clarity:** Thematic names (Earth, Mars) > generic (node_1, node_2)
- **Keep simple:** Don't implement full P2P protocol, just visual simulation
