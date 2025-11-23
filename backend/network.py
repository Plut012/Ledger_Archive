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
        """Create default network with 4 nodes in mesh topology."""
        # Create nodes with positions for visualization
        earth = Node("node_0", "earth.archive", "Earth", 150, 100)
        mars = Node("node_1", "mars.archive", "Mars", 350, 100)
        jupiter = Node("node_2", "jupiter.archive", "Jupiter", 250, 200)
        alpha = Node("node_3", "alpha.archive", "Alpha Centauri", 250, 300)

        # Add nodes
        for node in [earth, mars, jupiter, alpha]:
            self.add_node(node)

        # Create mesh topology connections
        self.connect_nodes("node_0", "node_1")  # Earth <-> Mars
        self.connect_nodes("node_0", "node_3")  # Earth <-> Alpha
        self.connect_nodes("node_1", "node_2")  # Mars <-> Jupiter
        self.connect_nodes("node_2", "node_3")  # Jupiter <-> Alpha

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
                    "status": n.status,
                    "height": len(n.blockchain.chain) - 1,
                }
                for n in self.nodes.values()
            ],
            "connections": self.connections,
        }
