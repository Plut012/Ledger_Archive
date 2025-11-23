"""Tests for coinbase transactions and mining rewards."""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import pytest
from transaction import Transaction
from block import Block, get_timestamp
from blockchain import Blockchain
from mining import Miner
from constants import BLOCK_REWARD


class TestCoinbaseTransactions:
    """Test suite for coinbase transaction functionality."""

    def test_coinbase_transaction_is_valid(self):
        """Test that a properly formed coinbase transaction is valid."""
        coinbase = Transaction(
            sender="COINBASE",
            recipient="MINER_ADDRESS",
            amount=BLOCK_REWARD,
            timestamp=get_timestamp(),
            is_coinbase=True
        )

        assert coinbase.is_valid()

    def test_coinbase_doesnt_need_signature(self):
        """Test that coinbase transactions don't require signatures."""
        coinbase = Transaction(
            sender="COINBASE",
            recipient="MINER_ADDRESS",
            amount=BLOCK_REWARD,
            timestamp=get_timestamp(),
            signature="",  # No signature
            is_coinbase=True
        )

        assert coinbase.is_valid()

    def test_coinbase_requires_positive_amount(self):
        """Test that coinbase transactions must have positive amount."""
        coinbase = Transaction(
            sender="COINBASE",
            recipient="MINER_ADDRESS",
            amount=0,  # Invalid
            timestamp=get_timestamp(),
            is_coinbase=True
        )

        assert not coinbase.is_valid()

    def test_coinbase_requires_recipient(self):
        """Test that coinbase transactions must have a recipient."""
        coinbase = Transaction(
            sender="COINBASE",
            recipient="",  # Invalid
            amount=BLOCK_REWARD,
            timestamp=get_timestamp(),
            is_coinbase=True
        )

        assert not coinbase.is_valid()

    def test_coinbase_must_be_from_coinbase(self):
        """Test that coinbase transactions must have COINBASE as sender."""
        fake_coinbase = Transaction(
            sender="FAKE_SENDER",  # Invalid
            recipient="MINER_ADDRESS",
            amount=BLOCK_REWARD,
            timestamp=get_timestamp(),
            is_coinbase=True
        )

        assert not fake_coinbase.is_valid()

    def test_miner_creates_coinbase_automatically(self):
        """Test that mining creates coinbase transaction."""
        blockchain = Blockchain()
        miner = Miner(difficulty=1, block_reward=50.0)

        block = miner.mine_block(
            blockchain.get_latest_block(),
            [],
            miner_address="TEST_MINER"
        )

        # Block should have at least one transaction (coinbase)
        assert len(block.transactions) == 1

        # First transaction should be coinbase
        coinbase_dict = block.transactions[0]
        assert coinbase_dict["sender"] == "COINBASE"
        assert coinbase_dict["recipient"] == "TEST_MINER"
        assert coinbase_dict["amount"] == 50.0
        assert coinbase_dict["is_coinbase"] is True

    def test_coinbase_is_first_transaction(self):
        """Test that coinbase is always first transaction in block."""
        blockchain = Blockchain()
        miner = Miner(difficulty=1)

        # Create some regular transactions
        tx1 = Transaction("ALICE", "BOB", 10.0, get_timestamp(), "sig1")
        tx2 = Transaction("BOB", "CHARLIE", 5.0, get_timestamp(), "sig2")

        block = miner.mine_block(
            blockchain.get_latest_block(),
            [tx1.to_dict(), tx2.to_dict()],
            miner_address="MINER"
        )

        # Should have 3 transactions total (1 coinbase + 2 regular)
        assert len(block.transactions) == 3

        # First one should be coinbase
        assert block.transactions[0]["is_coinbase"] is True
        assert block.transactions[0]["sender"] == "COINBASE"

        # Others should be regular transactions
        assert not block.transactions[1].get("is_coinbase", False)
        assert not block.transactions[2].get("is_coinbase", False)

    def test_different_miner_addresses(self):
        """Test that coinbase goes to specified miner address."""
        blockchain = Blockchain()
        miner = Miner(difficulty=1)

        addresses = ["MINER_A", "MINER_B", "MINER_C"]

        for address in addresses:
            block = miner.mine_block(
                blockchain.get_latest_block(),
                [],
                miner_address=address
            )

            coinbase = block.transactions[0]
            assert coinbase["recipient"] == address

    def test_block_reward_amount(self):
        """Test that block reward amount is correct."""
        blockchain = Blockchain()

        # Test with default reward
        miner1 = Miner(difficulty=1)
        block1 = miner1.mine_block(
            blockchain.get_latest_block(),
            [],
            miner_address="MINER_1"
        )
        assert block1.transactions[0]["amount"] == BLOCK_REWARD

        # Test with custom reward
        custom_reward = 100.0
        miner2 = Miner(difficulty=1, block_reward=custom_reward)
        block2 = miner2.mine_block(
            block1,
            [],
            miner_address="MINER_2"
        )
        assert block2.transactions[0]["amount"] == custom_reward

    def test_coinbase_serialization(self):
        """Test that coinbase transactions serialize correctly."""
        coinbase = Transaction(
            sender="COINBASE",
            recipient="MINER",
            amount=50.0,
            timestamp="2024-01-01",
            is_coinbase=True
        )

        # Convert to dict
        coinbase_dict = coinbase.to_dict()

        assert coinbase_dict["is_coinbase"] is True
        assert coinbase_dict["sender"] == "COINBASE"

        # Convert back from dict
        restored = Transaction.from_dict(coinbase_dict)

        assert restored.is_coinbase is True
        assert restored.sender == "COINBASE"
        assert restored.amount == 50.0
