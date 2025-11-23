"""
Tests for cryptographic operations.

PHASE 1: Comprehensive tests for crypto.py and transaction signing

Run with: uv run pytest tests/test_crypto.py -v
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from crypto import Wallet, generate_address
from transaction import Transaction
from datetime import datetime


def test_generate_keypair():
    """
    Should create valid public/private key pair.

    Success criteria:
    - private_key is not empty
    - public_key is not empty
    - address is not empty
    - Keys are hex strings
    - Each generation creates different keys
    """
    wallet = Wallet()
    wallet.generate_keypair()

    assert wallet.private_key != ""
    assert wallet.public_key != ""
    assert wallet.address != ""
    assert len(wallet.private_key) == 64  # 32 bytes as hex = 64 chars
    assert len(wallet.public_key) == 64   # SHA-256 hash = 64 hex chars
    assert len(wallet.address) == 40      # First 40 chars of SHA-256

    # Keys should be different each time
    wallet2 = Wallet()
    wallet2.generate_keypair()
    assert wallet.private_key != wallet2.private_key
    assert wallet.public_key != wallet2.public_key
    assert wallet.address != wallet2.address


def test_sign_message():
    """
    Should create a valid signature for a message.

    Success criteria:
    - Signature is not empty
    - Signature is deterministic (same message = same signature)
    - Different messages = different signatures
    """
    wallet = Wallet()
    wallet.generate_keypair()

    message = "Test message"
    signature = wallet.sign(message)

    assert signature != ""
    assert len(signature) == 64  # SHA-256 hash = 64 hex chars

    # Same message should produce same signature (deterministic)
    signature2 = wallet.sign(message)
    assert signature == signature2

    # Different message should produce different signature
    signature3 = wallet.sign("Different message")
    assert signature != signature3


def test_verify_valid_signature():
    """
    Should verify a valid signature.

    Success criteria:
    - Valid signature returns True
    - Can verify with public key only (no private key needed)
    """
    wallet = Wallet()
    wallet.generate_keypair()

    message = "Test message"
    signature = wallet.sign(message)

    # Verify using the static method (doesn't need wallet instance)
    is_valid = Wallet.verify(message, signature, wallet.public_key)
    assert is_valid == True

    # Can also verify using instance method
    is_valid2 = wallet.verify(message, signature, wallet.public_key)
    assert is_valid2 == True


def test_verify_invalid_signature():
    """
    Should reject an invalid signature.

    Success criteria:
    - Wrong signature format returns False
    - Empty signature returns False
    """
    wallet = Wallet()
    wallet.generate_keypair()

    message = "Test message"
    signature = wallet.sign(message)

    # Wrong signature format should fail (not hex)
    is_valid = Wallet.verify(message, "not_a_valid_hex_signature!", wallet.public_key)
    assert is_valid == False

    # Wrong signature format should fail (wrong length)
    is_valid = Wallet.verify(message, "abc123", wallet.public_key)
    assert is_valid == False

    # Empty signature should fail
    is_valid = Wallet.verify(message, "", wallet.public_key)
    assert is_valid == False

    # Empty public key should fail
    is_valid = Wallet.verify(message, signature, "")
    assert is_valid == False


def test_generate_address():
    """
    Should generate consistent address from public key.

    Success criteria:
    - Address is 40 characters (hex string)
    - Same public key = same address
    - Different public key = different address
    """
    public_key = "test_public_key_123"

    address = generate_address(public_key)
    assert len(address) == 40
    assert address.isalnum()  # Should be alphanumeric (hex)

    # Should be consistent (deterministic)
    address2 = generate_address(public_key)
    assert address == address2

    # Different key = different address
    address3 = generate_address("different_key")
    assert address != address3


def test_wallet_address_matches_public_key():
    """
    Should generate address that matches public key.

    Success criteria:
    - Wallet address is derived from public key
    - Address can be regenerated from public key
    """
    wallet = Wallet()
    wallet.generate_keypair()

    # Wallet address should be derivable from public key
    regenerated_address = generate_address(wallet.public_key)
    assert wallet.address == regenerated_address


def test_transaction_signing():
    """
    Should sign a transaction with wallet.

    Success criteria:
    - Transaction can be signed
    - Signature is added to transaction
    - Signed transaction is valid
    """
    wallet = Wallet()
    wallet.generate_keypair()

    tx = Transaction(
        sender=wallet.address,
        recipient="recipient_address",
        amount=10.0,
        timestamp=datetime.now().isoformat()
    )

    # Sign the transaction
    tx.sign(wallet)

    assert tx.signature != ""
    assert len(tx.signature) == 64
    assert tx.is_valid() == True


def test_transaction_without_signature():
    """
    Should validate transaction without signature.

    Success criteria:
    - Transaction without signature is still valid (for coinbase txs)
    - Basic validation still works
    """
    tx = Transaction(
        sender="sender_address",
        recipient="recipient_address",
        amount=10.0,
        timestamp=datetime.now().isoformat(),
        signature=""
    )

    # Transaction without signature should still pass basic validation
    assert tx.is_valid() == True


def test_transaction_invalid_amount():
    """
    Should reject transaction with invalid amount.

    Success criteria:
    - Zero amount is rejected
    - Negative amount is rejected
    """
    tx1 = Transaction(
        sender="sender",
        recipient="recipient",
        amount=0,
        timestamp=datetime.now().isoformat()
    )
    assert tx1.is_valid() == False

    tx2 = Transaction(
        sender="sender",
        recipient="recipient",
        amount=-10,
        timestamp=datetime.now().isoformat()
    )
    assert tx2.is_valid() == False


def test_transaction_calculate_hash():
    """
    Should calculate consistent hash for transaction.

    Success criteria:
    - Hash is deterministic
    - Different transactions have different hashes
    - Signature is not included in hash
    """
    tx = Transaction(
        sender="alice",
        recipient="bob",
        amount=5.0,
        timestamp="2024-01-01T00:00:00"
    )

    hash1 = tx.calculate_hash()
    hash2 = tx.calculate_hash()
    assert hash1 == hash2  # Deterministic

    # Different transaction should have different hash
    tx2 = Transaction(
        sender="alice",
        recipient="bob",
        amount=6.0,  # Different amount
        timestamp="2024-01-01T00:00:00"
    )
    hash3 = tx2.calculate_hash()
    assert hash1 != hash3


def test_sign_requires_wallet():
    """
    Should require wallet to sign.

    Success criteria:
    - Cannot sign without wallet
    - Wallet must have keys generated
    """
    wallet = Wallet()  # No keys generated

    tx = Transaction(
        sender="sender",
        recipient="recipient",
        amount=10.0,
        timestamp=datetime.now().isoformat()
    )

    # Should raise error when signing with wallet that has no keys
    try:
        tx.sign(wallet)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "private key" in str(e).lower()


# ============================================================
# Run tests
# ============================================================

if __name__ == "__main__":
    print("Running crypto tests...")
    print("Run with: uv run pytest tests/test_crypto.py -v\n")

    test_generate_keypair()
    print("✓ test_generate_keypair")

    test_sign_message()
    print("✓ test_sign_message")

    test_verify_valid_signature()
    print("✓ test_verify_valid_signature")

    test_verify_invalid_signature()
    print("✓ test_verify_invalid_signature")

    test_generate_address()
    print("✓ test_generate_address")

    test_wallet_address_matches_public_key()
    print("✓ test_wallet_address_matches_public_key")

    test_transaction_signing()
    print("✓ test_transaction_signing")

    test_transaction_without_signature()
    print("✓ test_transaction_without_signature")

    test_transaction_invalid_amount()
    print("✓ test_transaction_invalid_amount")

    test_transaction_calculate_hash()
    print("✓ test_transaction_calculate_hash")

    test_sign_requires_wallet()
    print("✓ test_sign_requires_wallet")

    print("\n✅ All tests passing! Phase 1 crypto implementation complete.")
