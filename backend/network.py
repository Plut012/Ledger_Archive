"""P2P network simulation for distributed nodes."""

from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from blockchain import Blockchain


@dataclass
class Node:
    """A node in the network."""

    id: str
    address: str
    label: str
    x: float  # Canvas position
    y: float  # Canvas position
    layer: int = 1  # Depth layer (1=foreground, 2=mid, 3=background)
    status: str = "synced"
    peers: List[str] = field(default_factory=list)
    blockchain: Blockchain = field(default_factory=Blockchain)
    mempool: List[dict] = field(default_factory=list)


class Network:
    """Manages network topology and node communication."""

    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.connections: List[Tuple[str, str]] = []

    def create_default_topology(self):
        """Create Imperium network with 50 nodes in layered helix topology."""
        import math

        # Network topology: 8 Core + 17 Sector + 25 Frontier = 50 nodes
        # Arranged in a 2.5D helix pattern with 3 depth layers

        nodes_data = []

        # Canvas center: 500, 300 (for 1000x600 canvas)
        center_x = 500
        center_y = 300

        # Layer 1 (Foreground - Core Archives): 8 nodes
        core_names = [
            ("Earth Prime Archive", "earth-prime.archive"),
            ("Mars Command Archive", "mars-cmd.archive"),
            ("Jupiter Central Archive", "jupiter-central.archive"),
            ("Saturn Nexus Archive", "saturn-nexus.archive"),
            ("Sol Hub Archive", "sol-hub.archive"),
            ("Terra Nova Archive", "terra-nova.archive"),
            ("Titan Core Archive", "titan-core.archive"),
            ("Neptune Archive", "neptune.archive")
        ]

        for i, (label, address) in enumerate(core_names):
            angle = (i / 8) * 2 * math.pi
            # Layer 1: innermost ring
            x = center_x + math.cos(angle) * 130
            y = center_y + math.sin(angle) * 100
            nodes_data.append(("node_" + str(i), address, label, x, y, 1))

        # Layer 2 (Mid - Sector Hubs): 17 nodes
        sector_prefixes = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon",
                          "Zeta", "Eta", "Theta", "Iota", "Kappa",
                          "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi", "Rho"]

        for i in range(17):
            angle = (i / 17) * 2 * math.pi + 0.3  # Offset angle for helix effect
            label = f"{sector_prefixes[i]} Sector Hub"
            address = f"{sector_prefixes[i].lower()}-sector.archive"
            # Layer 2: medium ring
            x = center_x + math.cos(angle) * 260
            y = center_y + math.sin(angle) * 200
            nodes_data.append((f"node_{i+8}", address, label, x, y, 2))

        # Layer 3 (Background - Frontier Stations): 25 nodes
        frontier_types = ["Relay", "Outpost", "Station", "Beacon", "Post"]

        for i in range(25):
            angle = (i / 25) * 2 * math.pi + 0.6  # Different offset for helix
            type_name = frontier_types[i % 5]
            label = f"Frontier {type_name} {i+1}"
            address = f"frontier-{i+1}.archive"
            # Layer 3: outermost ring
            x = center_x + math.cos(angle) * 400
            y = center_y + math.sin(angle) * 260
            nodes_data.append((f"node_{i+25}", address, label, x, y, 3))

        # Create node objects
        for node_id, address, label, x, y, layer in nodes_data:
            node = Node(node_id, address, label, x, y, layer)
            self.add_node(node)

        # Create connections in a helix pattern
        # Core nodes form a ring
        for i in range(8):
            self.connect_nodes(f"node_{i}", f"node_{(i+1) % 8}")

        # Each core connects to 2-3 sector hubs
        for i in range(8):
            self.connect_nodes(f"node_{i}", f"node_{8 + (i * 2) % 17}")
            self.connect_nodes(f"node_{i}", f"node_{8 + (i * 2 + 1) % 17}")

        # Sector hubs form a ring
        for i in range(17):
            self.connect_nodes(f"node_{8+i}", f"node_{8 + ((i+1) % 17)}")

        # Each sector hub connects to 1-2 frontier stations
        for i in range(17):
            frontier_idx = int(i * 1.47) % 25  # Distribute across frontier nodes
            self.connect_nodes(f"node_{8+i}", f"node_{25 + frontier_idx}")
            if i % 2 == 0:  # Every other sector gets a second connection
                frontier_idx2 = (frontier_idx + 3) % 25
                self.connect_nodes(f"node_{8+i}", f"node_{25 + frontier_idx2}")

        # Some frontier-to-frontier connections for redundancy
        for i in range(25):
            if i % 5 == 0 and i < 20:
                self.connect_nodes(f"node_{25+i}", f"node_{25+i+5}")

    def add_node(self, node: Node):
        """Add a node to the network."""
        self.nodes[node.id] = node

    def connect_nodes(self, node_id_1: str, node_id_2: str):
        """Create connection between two nodes."""
        if node_id_1 in self.nodes and node_id_2 in self.nodes:
            self.connections.append((node_id_1, node_id_2))
            self.nodes[node_id_1].peers.append(node_id_2)
            self.nodes[node_id_2].peers.append(node_id_1)

    def broadcast_transaction(self, tx: dict, origin_node_id: str = None) -> List[str]:
        """
        Broadcast transaction to all nodes.
        Returns propagation path.
        """
        if origin_node_id is None:
            origin_node_id = list(self.nodes.keys())[0]

        # Add to origin node's mempool
        if origin_node_id in self.nodes:
            self.nodes[origin_node_id].mempool.append(tx)

        # BFS propagation to all connected nodes
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

    def sync_chain(self, from_blockchain: Blockchain):
        """Sync all nodes to the same blockchain state."""
        for node in self.nodes.values():
            # Deep copy the chain
            node.blockchain.chain = [block for block in from_blockchain.chain]

    def get_node_details(self, node_id: str) -> dict:
        """Get detailed information about a specific node."""
        if node_id not in self.nodes:
            return None

        node = self.nodes[node_id]
        return {
            "id": node.id,
            "address": node.address,
            "label": node.label,
            "status": node.status,
            "height": len(node.blockchain.chain) - 1,
            "peers": [self.nodes[p].label for p in node.peers],
            "mempool_size": len(node.mempool),
        }

    def get_topology(self) -> dict:
        """Return network topology data."""
        return {
            "nodes": [
                {
                    "id": n.id,
                    "address": n.address,
                    "label": n.label,
                    "x": n.x,
                    "y": n.y,
                    "layer": n.layer,
                    "status": n.status,
                    "height": len(n.blockchain.chain) - 1,
                }
                for n in self.nodes.values()
            ],
            "connections": self.connections,
        }
