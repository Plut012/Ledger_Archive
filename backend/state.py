"""Global blockchain state management."""

from blockchain import Blockchain
from network import Network
from ledger import Ledger


class BlockchainState:
    """Global state for the entire application."""

    def __init__(self):
        self.blockchain = Blockchain()
        self.ledger = Ledger(self.blockchain)  # Track balances
        self.mempool = []  # Pending transactions
        self.wallets = {}  # User wallets
        self.network = Network()
        self.network.create_default_topology()
        # Sync all nodes to the main blockchain
        self.network.sync_chain(self.blockchain)

    def reset(self):
        """Reset to genesis for experimentation."""
        self.__init__()


# Global singleton instance
state = BlockchainState()
