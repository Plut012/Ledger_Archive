"""Proof of Work mining implementation."""

from typing import List
from block import Block, get_timestamp
from transaction import Transaction
from constants import BLOCK_REWARD


class Miner:
    """Handles proof-of-work mining operations."""

    def __init__(self, difficulty: int = 4, block_reward: float = BLOCK_REWARD):
        self.difficulty = difficulty
        self.target = "0" * difficulty
        self.block_reward = block_reward

    def mine_block(self, previous_block: Block, transactions: List[dict], miner_address: str = "DEFAULT_MINER") -> Block:
        """
        Mine a new block using Proof of Work.
        Creates a coinbase transaction to reward the miner.

        Args:
            previous_block: The last block in the chain
            transactions: List of transactions to include
            miner_address: Address to send block reward to

        Returns:
            A mined block with valid proof of work (includes coinbase transaction)
        """
        # Create coinbase transaction (mining reward)
        coinbase = Transaction(
            sender="COINBASE",
            recipient=miner_address,
            amount=self.block_reward,
            timestamp=get_timestamp(),
            is_coinbase=True
        )

        # Coinbase must be first transaction in block
        all_transactions = [coinbase.to_dict()] + transactions

        new_block = Block(
            index=previous_block.index + 1,
            timestamp=get_timestamp(),
            transactions=all_transactions,
            previous_hash=previous_block.hash,
            nonce=0
        )

        # Keep hashing until we find a valid proof of work
        while not new_block.hash.startswith(self.target):
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()

        return new_block

    def adjust_difficulty(self, blockchain, target_time: int = 10):
        """
        Adjust mining difficulty based on recent block times.

        Args:
            blockchain: The current blockchain
            target_time: Target time between blocks in seconds
        """
        if len(blockchain.chain) < 10:
            return

        recent_blocks = blockchain.chain[-10:]
        time_taken = calculate_time_span(recent_blocks)

        if time_taken < target_time * 9:
            self.difficulty += 1
            self.target = "0" * self.difficulty
        elif time_taken > target_time * 11:
            self.difficulty = max(1, self.difficulty - 1)
            self.target = "0" * self.difficulty


def calculate_time_span(blocks: List[Block]) -> int:
    """Calculate time span between first and last block."""
    # Simplified for now
    return len(blocks) * 10
