"""Tests for blockchain functionality."""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from blockchain import Blockchain
from block import Block


def test_genesis_block_creation():
    """Genesis block should be created automatically."""
    chain = Blockchain()
    assert len(chain.chain) == 1
    assert chain.chain[0].index == 0
    assert chain.chain[0].previous_hash == "0"


def test_add_valid_block():
    """Valid blocks should be added to chain."""
    chain = Blockchain()
    previous = chain.get_latest_block()

    new_block = Block(
        index=1,
        timestamp="2024-01-01 00:00:00",
        transactions=[],
        previous_hash=previous.hash
    )

    assert chain.add_block(new_block) == True
    assert len(chain.chain) == 2


def test_reject_invalid_block():
    """Blocks with wrong previous_hash should be rejected."""
    chain = Blockchain()

    bad_block = Block(
        index=1,
        timestamp="2024-01-01 00:00:00",
        transactions=[],
        previous_hash="wrong_hash"
    )

    assert chain.add_block(bad_block) == False
    assert len(chain.chain) == 1  # Still just genesis


def test_chain_validation():
    """Valid chains should pass validation."""
    chain = Blockchain()
    previous = chain.get_latest_block()

    # Add a valid block
    new_block = Block(
        index=1,
        timestamp="2024-01-01 00:00:00",
        transactions=[],
        previous_hash=previous.hash
    )
    chain.add_block(new_block)

    assert chain.is_valid_chain() == True


if __name__ == "__main__":
    test_genesis_block_creation()
    test_add_valid_block()
    test_reject_invalid_block()
    test_chain_validation()
    print("All tests passed!")
