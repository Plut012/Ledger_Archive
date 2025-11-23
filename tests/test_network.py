"""Tests for network topology and propagation."""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import pytest
from network import Network, Node
from blockchain import Blockchain


def test_node_creation():
    """Test creating a node."""
    node = Node("node_0", "earth.archive", "Earth", 100, 100)
    assert node.id == "node_0"
    assert node.address == "earth.archive"
    assert node.label == "Earth"
    assert node.x == 100
    assert node.y == 100
    assert node.status == "synced"
    assert len(node.peers) == 0
    assert isinstance(node.blockchain, Blockchain)


def test_network_initialization():
    """Test creating an empty network."""
    network = Network()
    assert len(network.nodes) == 0
    assert len(network.connections) == 0


def test_add_node():
    """Test adding a node to the network."""
    network = Network()
    node = Node("node_0", "earth.archive", "Earth", 100, 100)
    network.add_node(node)

    assert len(network.nodes) == 1
    assert "node_0" in network.nodes
    assert network.nodes["node_0"].label == "Earth"


def test_connect_nodes():
    """Test connecting two nodes."""
    network = Network()
    node1 = Node("node_0", "earth.archive", "Earth", 100, 100)
    node2 = Node("node_1", "mars.archive", "Mars", 200, 100)

    network.add_node(node1)
    network.add_node(node2)
    network.connect_nodes("node_0", "node_1")

    assert len(network.connections) == 1
    assert ("node_0", "node_1") in network.connections
    assert "node_1" in network.nodes["node_0"].peers
    assert "node_0" in network.nodes["node_1"].peers


def test_create_default_topology():
    """Test creating the default 4-node mesh topology."""
    network = Network()
    network.create_default_topology()

    # Check nodes
    assert len(network.nodes) == 4
    assert "node_0" in network.nodes
    assert "node_1" in network.nodes
    assert "node_2" in network.nodes
    assert "node_3" in network.nodes

    # Check labels
    assert network.nodes["node_0"].label == "Earth"
    assert network.nodes["node_1"].label == "Mars"
    assert network.nodes["node_2"].label == "Jupiter"
    assert network.nodes["node_3"].label == "Alpha Centauri"

    # Check connections (mesh topology)
    assert len(network.connections) == 4
    assert ("node_0", "node_1") in network.connections  # Earth <-> Mars
    assert ("node_0", "node_3") in network.connections  # Earth <-> Alpha
    assert ("node_1", "node_2") in network.connections  # Mars <-> Jupiter
    assert ("node_2", "node_3") in network.connections  # Jupiter <-> Alpha


def test_broadcast_transaction():
    """Test broadcasting a transaction through the network."""
    network = Network()
    network.create_default_topology()

    tx = {
        "sender": "alice",
        "recipient": "bob",
        "amount": 100,
        "timestamp": 1234567890,
        "signature": "test_sig"
    }

    paths = network.broadcast_transaction(tx, "node_0")

    # Should have 3 propagation paths from node_0
    assert len(paths) == 3

    # All nodes should have the transaction in their mempool
    for node_id in ["node_0", "node_1", "node_2", "node_3"]:
        assert len(network.nodes[node_id].mempool) == 1
        assert network.nodes[node_id].mempool[0]["sender"] == "alice"


def test_sync_chain():
    """Test syncing blockchain to all nodes."""
    network = Network()
    network.create_default_topology()

    # Create a blockchain with some blocks
    main_chain = Blockchain()
    # The genesis block already exists

    # Sync to all nodes
    network.sync_chain(main_chain)

    # All nodes should have the same chain length
    for node in network.nodes.values():
        assert len(node.blockchain.chain) == len(main_chain.chain)


def test_get_node_details():
    """Test getting node details."""
    network = Network()
    network.create_default_topology()

    details = network.get_node_details("node_0")

    assert details is not None
    assert details["id"] == "node_0"
    assert details["label"] == "Earth"
    assert details["address"] == "earth.archive"
    assert details["status"] == "synced"
    assert details["height"] == 0  # Genesis block
    assert len(details["peers"]) == 2  # Earth connects to Mars and Alpha
    assert "Mars" in details["peers"]
    assert "Alpha Centauri" in details["peers"]


def test_get_node_details_invalid():
    """Test getting details for a non-existent node."""
    network = Network()
    network.create_default_topology()

    details = network.get_node_details("invalid_node")
    assert details is None


def test_get_topology():
    """Test getting network topology."""
    network = Network()
    network.create_default_topology()

    topology = network.get_topology()

    assert "nodes" in topology
    assert "connections" in topology
    assert len(topology["nodes"]) == 4
    assert len(topology["connections"]) == 4

    # Check node data includes visualization coordinates
    earth = next(n for n in topology["nodes"] if n["id"] == "node_0")
    assert earth["x"] == 150
    assert earth["y"] == 100
    assert earth["label"] == "Earth"


def test_propagation_paths():
    """Test that propagation follows BFS and reaches all nodes."""
    network = Network()
    network.create_default_topology()

    tx = {"sender": "test", "recipient": "test", "amount": 1, "timestamp": 0, "signature": ""}
    paths = network.broadcast_transaction(tx, "node_0")

    # Verify all paths start from node_0
    for path in paths:
        assert path[0] == "node_0"

    # Verify all other nodes are reached
    reached_nodes = set()
    for path in paths:
        reached_nodes.add(path[-1])

    assert "node_1" in reached_nodes
    assert "node_2" in reached_nodes
    assert "node_3" in reached_nodes
