"""Core blockchain logic and validation."""

from typing import List
from block import Block, get_timestamp


class Blockchain:
    """The complete blockchain with validation."""

    def __init__(self):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.pending_transactions: List[dict] = []

    def create_genesis_block(self) -> Block:
        """Create the first block in the chain."""
        return Block(
            index=0,
            timestamp=get_timestamp(),
            transactions=[],
            previous_hash="0"
        )

    def add_block(self, block: Block) -> bool:
        """Add a block if valid."""
        if self.is_valid_block(block, self.chain[-1]):
            self.chain.append(block)
            return True
        return False

    def is_valid_chain(self) -> bool:
        """Validate the entire chain."""
        for i in range(1, len(self.chain)):
            if not self.is_valid_block(self.chain[i], self.chain[i-1]):
                return False
        return True

    def is_valid_block(self, block: Block, previous_block: Block = None) -> bool:
        """Check if a single block is valid."""
        if previous_block:
            if block.previous_hash != previous_block.hash:
                return False
            if block.index != previous_block.index + 1:
                return False

        if block.hash != block.calculate_hash():
            return False

        return True

    def get_latest_block(self) -> Block:
        """Return the most recent block."""
        return self.chain[-1]
