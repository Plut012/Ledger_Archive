"""Consensus mechanisms for distributed agreement."""

from typing import List
from blockchain import Blockchain


class Consensus:
    """Handles consensus logic for the network."""

    def __init__(self):
        self.algorithm = "longest_chain"

    def resolve_conflicts(self, chains: List[Blockchain]) -> Blockchain:
        """
        Resolve conflicts between multiple chains.

        Uses longest chain rule by default.

        Args:
            chains: List of blockchain instances to compare

        Returns:
            The canonical blockchain
        """
        if not chains:
            return None

        # Longest valid chain wins
        longest_chain = None
        max_length = 0

        for chain in chains:
            if chain.is_valid_chain() and len(chain.chain) > max_length:
                longest_chain = chain
                max_length = len(chain.chain)

        return longest_chain

    def validate_fork(self, chain1: Blockchain, chain2: Blockchain) -> bool:
        """Check if two chains have a common ancestor."""
        # TODO: Implement fork validation
        return False
