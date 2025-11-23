"""Tests for transaction validation with balance checking."""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import pytest
from blockchain import Blockchain
from ledger import Ledger
from transaction import Transaction
from mining import Miner
from block import get_timestamp
from constants import BLOCK_REWARD


class TestBalanceValidation:
    """Test suite for balance validation in transactions."""

    def test_transaction_fails_without_funds(self):
        """Test that transaction fails when sender has no funds."""
        blockchain = Blockchain()
        ledger = Ledger(blockchain)

        tx = Transaction(
            sender="BROKE_USER",
            recipient="ALICE",
            amount=10.0,
            timestamp=get_timestamp(),
            signature="test_sig"
        )

        # Should fail validation when ledger is provided
        assert not tx.is_valid(ledger=ledger)

    def test_transaction_succeeds_with_sufficient_funds(self):
        """Test that transaction succeeds when sender has enough funds."""
        blockchain = Blockchain()
        ledger = Ledger(blockchain)
        miner = Miner(difficulty=1)

        # Give Alice some funds
        block = miner.mine_block(
            blockchain.get_latest_block(),
            [],
            miner_address="ALICE"
        )
        blockchain.add_block(block)
        ledger.calculate_balances()

        # Alice tries to send 10 (has 50)
        tx = Transaction(
            sender="ALICE",
            recipient="BOB",
            amount=10.0,
            timestamp=get_timestamp(),
            signature=""  # No signature for test (would need real wallet to sign)
        )

        # Should succeed with ledger
        assert tx.is_valid(ledger=ledger)

    def test_transaction_fails_with_insufficient_funds(self):
        """Test that transaction fails when sender doesn't have enough."""
        blockchain = Blockchain()
        ledger = Ledger(blockchain)
        miner = Miner(difficulty=1)

        # Give Alice 50
        block = miner.mine_block(
            blockchain.get_latest_block(),
            [],
            miner_address="ALICE"
        )
        blockchain.add_block(block)
        ledger.calculate_balances()

        # Alice tries to send 100 (only has 50)
        tx = Transaction(
            sender="ALICE",
            recipient="BOB",
            amount=100.0,
            timestamp=get_timestamp(),
            signature=""
        )

        # Should fail with ledger
        assert not tx.is_valid(ledger=ledger)

    def test_transaction_succeeds_with_exact_balance(self):
        """Test that transaction succeeds when amount equals balance."""
        blockchain = Blockchain()
        ledger = Ledger(blockchain)
        miner = Miner(difficulty=1)

        # Give Alice 50
        block = miner.mine_block(
            blockchain.get_latest_block(),
            [],
            miner_address="ALICE"
        )
        blockchain.add_block(block)
        ledger.calculate_balances()

        # Alice sends exactly 50
        tx = Transaction(
            sender="ALICE",
            recipient="BOB",
            amount=BLOCK_REWARD,
            timestamp=get_timestamp(),
            signature=""
        )

        # Should succeed
        assert tx.is_valid(ledger=ledger)

    def test_validation_without_ledger_skips_balance_check(self):
        """Test that validation without ledger doesn't check balances."""
        # Transaction from user with no funds
        tx = Transaction(
            sender="BROKE_USER",
            recipient="ALICE",
            amount=10.0,
            timestamp=get_timestamp(),
            signature=""
        )

        # Should pass basic validation (no ledger provided)
        assert tx.is_valid()  # No ledger = no balance check

    def test_coinbase_ignores_balance_check(self):
        """Test that coinbase transactions bypass balance checking."""
        blockchain = Blockchain()
        ledger = Ledger(blockchain)

        coinbase = Transaction(
            sender="COINBASE",
            recipient="MINER",
            amount=50.0,
            timestamp=get_timestamp(),
            is_coinbase=True
        )

        # Should be valid even though COINBASE has no balance
        assert coinbase.is_valid(ledger=ledger)

    def test_multiple_transactions_deplete_balance(self):
        """Test that multiple transactions correctly deplete balance."""
        blockchain = Blockchain()
        ledger = Ledger(blockchain)
        miner = Miner(difficulty=1)

        # Give Alice 50
        block1 = miner.mine_block(
            blockchain.get_latest_block(),
            [],
            miner_address="ALICE"
        )
        blockchain.add_block(block1)
        ledger.calculate_balances()

        # First transaction: Alice sends 20 to Bob
        tx1 = Transaction("ALICE", "BOB", 20.0, get_timestamp(), "")
        assert tx1.is_valid(ledger=ledger)

        # Mine it
        block2 = miner.mine_block(
            blockchain.get_latest_block(),
            [tx1.to_dict()],
            miner_address="CHARLIE"
        )
        blockchain.add_block(block2)
        ledger.calculate_balances()

        # Second transaction: Alice tries to send 40 (only has 30 left)
        tx2 = Transaction("ALICE", "BOB", 40.0, get_timestamp(), "")
        assert not tx2.is_valid(ledger=ledger)

        # Third transaction: Alice sends 30 (exact balance)
        tx3 = Transaction("ALICE", "BOB", 30.0, get_timestamp(), "")
        assert tx3.is_valid(ledger=ledger)

    def test_balance_check_with_pending_transactions(self):
        """Test that balance check uses confirmed balances only."""
        blockchain = Blockchain()
        ledger = Ledger(blockchain)
        miner = Miner(difficulty=1)

        # Give Alice 50
        block = miner.mine_block(
            blockchain.get_latest_block(),
            [],
            miner_address="ALICE"
        )
        blockchain.add_block(block)
        ledger.calculate_balances()

        # Alice can spend up to 50
        tx1 = Transaction("ALICE", "BOB", 30.0, get_timestamp(), "")
        assert tx1.is_valid(ledger=ledger)

        # Even though tx1 isn't mined yet, Alice can still create another tx
        # (in mempool) because ledger only tracks confirmed transactions
        tx2 = Transaction("ALICE", "CHARLIE", 30.0, get_timestamp(), "")
        assert tx2.is_valid(ledger=ledger)

        # Note: In a real system, mempool would track pending TXs
        # But our ledger only tracks confirmed (mined) transactions
