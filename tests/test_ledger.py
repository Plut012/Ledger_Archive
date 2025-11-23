"""Tests for ledger and balance tracking."""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import pytest
from blockchain import Blockchain
from ledger import Ledger
from transaction import Transaction
from block import Block, get_timestamp
from mining import Miner
from constants import BLOCK_REWARD


class TestLedger:
    """Test suite for Ledger functionality."""

    def test_empty_blockchain_has_zero_balances(self):
        """Test that genesis blockchain has no balances."""
        blockchain = Blockchain()
        ledger = Ledger(blockchain)

        balances = ledger.calculate_balances()

        assert balances == {}
        assert ledger.get_total_supply() == 0

    def test_coinbase_transaction_increases_balance(self):
        """Test that mining a block with coinbase increases miner balance."""
        blockchain = Blockchain()
        ledger = Ledger(blockchain)
        miner = Miner(difficulty=1)

        # Mine a block with coinbase
        block = miner.mine_block(
            blockchain.get_latest_block(),
            [],
            miner_address="MINER_1"
        )
        blockchain.add_block(block)
        ledger.calculate_balances()

        # Check miner received reward
        assert ledger.get_balance("MINER_1") == BLOCK_REWARD
        assert ledger.get_total_supply() == BLOCK_REWARD

    def test_multiple_blocks_accumulate_supply(self):
        """Test that mining multiple blocks increases total supply."""
        blockchain = Blockchain()
        ledger = Ledger(blockchain)
        miner = Miner(difficulty=1)

        # Mine 3 blocks
        for i in range(3):
            block = miner.mine_block(
                blockchain.get_latest_block(),
                [],
                miner_address=f"MINER_{i}"
            )
            blockchain.add_block(block)

        ledger.calculate_balances()

        # Total supply should be 3 * block_reward
        assert ledger.get_total_supply() == 3 * BLOCK_REWARD

        # Each miner should have one block reward
        assert ledger.get_balance("MINER_0") == BLOCK_REWARD
        assert ledger.get_balance("MINER_1") == BLOCK_REWARD
        assert ledger.get_balance("MINER_2") == BLOCK_REWARD

    def test_regular_transaction_moves_funds(self):
        """Test that regular transactions transfer balances correctly."""
        blockchain = Blockchain()
        ledger = Ledger(blockchain)
        miner = Miner(difficulty=1)

        # Mine a block to create some coins
        block1 = miner.mine_block(
            blockchain.get_latest_block(),
            [],
            miner_address="ALICE"
        )
        blockchain.add_block(block1)

        # Create transaction from Alice to Bob
        tx = Transaction(
            sender="ALICE",
            recipient="BOB",
            amount=25.0,
            timestamp=get_timestamp(),
            signature="test_sig"
        )

        # Mine block with transaction
        block2 = miner.mine_block(
            blockchain.get_latest_block(),
            [tx.to_dict()],
            miner_address="ALICE"
        )
        blockchain.add_block(block2)
        ledger.calculate_balances()

        # Alice should have: 50 (first block) + 50 (second block) - 25 (sent) = 75
        assert ledger.get_balance("ALICE") == 75.0

        # Bob should have: 25 (received)
        assert ledger.get_balance("BOB") == 25.0

        # Total supply: 2 blocks = 100
        assert ledger.get_total_supply() == 100.0

    def test_insufficient_funds_detected(self):
        """Test that ledger correctly identifies insufficient funds."""
        blockchain = Blockchain()
        ledger = Ledger(blockchain)

        # Check balance of address that never received coins
        assert not ledger.has_sufficient_funds("BROKE_USER", 1.0)
        assert ledger.get_balance("BROKE_USER") == 0.0

    def test_exact_balance_allowed(self):
        """Test that spending exact balance is allowed."""
        blockchain = Blockchain()
        ledger = Ledger(blockchain)
        miner = Miner(difficulty=1)

        # Mine a block
        block = miner.mine_block(
            blockchain.get_latest_block(),
            [],
            miner_address="ALICE"
        )
        blockchain.add_block(block)
        ledger.calculate_balances()

        # Alice should be able to spend exact balance
        assert ledger.has_sufficient_funds("ALICE", BLOCK_REWARD)
        assert not ledger.has_sufficient_funds("ALICE", BLOCK_REWARD + 0.01)

    def test_get_all_balances_filters_zero(self):
        """Test that get_all_balances only returns non-zero balances."""
        blockchain = Blockchain()
        ledger = Ledger(blockchain)
        miner = Miner(difficulty=1)

        # Mine a block
        block = miner.mine_block(
            blockchain.get_latest_block(),
            [],
            miner_address="ALICE"
        )
        blockchain.add_block(block)
        ledger.calculate_balances()

        all_balances = ledger.get_all_balances()

        # Should only have Alice's balance
        assert len(all_balances) == 1
        assert "ALICE" in all_balances
        assert all_balances["ALICE"] == BLOCK_REWARD

    def test_complex_transaction_chain(self):
        """Test a complex series of transactions."""
        blockchain = Blockchain()
        ledger = Ledger(blockchain)
        miner = Miner(difficulty=1)

        # Mine initial block for Alice
        block1 = miner.mine_block(
            blockchain.get_latest_block(),
            [],
            miner_address="ALICE"
        )
        blockchain.add_block(block1)

        # Alice sends 10 to Bob
        tx1 = Transaction("ALICE", "BOB", 10.0, get_timestamp(), "sig1")

        # Alice sends 20 to Charlie
        tx2 = Transaction("ALICE", "CHARLIE", 20.0, get_timestamp(), "sig2")

        # Mine block with both transactions (Bob is miner)
        block2 = miner.mine_block(
            blockchain.get_latest_block(),
            [tx1.to_dict(), tx2.to_dict()],
            miner_address="BOB"
        )
        blockchain.add_block(block2)

        # Bob sends 30 to Charlie
        tx3 = Transaction("BOB", "CHARLIE", 30.0, get_timestamp(), "sig3")

        # Mine block (Charlie is miner)
        block3 = miner.mine_block(
            blockchain.get_latest_block(),
            [tx3.to_dict()],
            miner_address="CHARLIE"
        )
        blockchain.add_block(block3)

        ledger.calculate_balances()

        # Alice: 50 - 10 - 20 = 20
        assert ledger.get_balance("ALICE") == 20.0

        # Bob: 10 (from Alice) + 50 (mining) - 30 (to Charlie) = 30
        assert ledger.get_balance("BOB") == 30.0

        # Charlie: 20 (from Alice) + 30 (from Bob) + 50 (mining) = 100
        assert ledger.get_balance("CHARLIE") == 100.0

        # Total: 3 blocks * 50 = 150
        assert ledger.get_total_supply() == 150.0

    def test_balance_calculation_idempotent(self):
        """Test that recalculating balances gives same result."""
        blockchain = Blockchain()
        ledger = Ledger(blockchain)
        miner = Miner(difficulty=1)

        # Mine some blocks
        for i in range(3):
            block = miner.mine_block(
                blockchain.get_latest_block(),
                [],
                miner_address=f"MINER_{i}"
            )
            blockchain.add_block(block)

        # Calculate balances twice
        balances1 = ledger.calculate_balances()
        balances2 = ledger.calculate_balances()

        assert balances1 == balances2
