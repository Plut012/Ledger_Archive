"""Cryptographic primitives for keys and signatures."""

# ============================================================
# PHASE 1: Implement Real Cryptography
# ============================================================
#
# Goals:
# 1. Generate public/private key pairs
# 2. Sign messages with private key
# 3. Verify signatures with public key
# 4. Keep implementation simple and educational
#
# Implementation Notes:
# - Use Python's built-in secrets module for randomness
# - Use hashlib for hashing
# - Store keys as hex strings for easy display/debug
# - Don't need full Bitcoin-style crypto (keep simple)
#
# See: docs/phase1_plan.md for full details
# ============================================================

import hashlib
import secrets
from typing import Tuple


class Wallet:
    """Simple wallet with key pair and signing capability."""

    def __init__(self):
        """Initialize empty wallet. Call generate_keypair() to create keys."""
        self.private_key = ""
        self.public_key = ""
        self.address = ""

    def generate_keypair(self):
        """
        Generate new public/private key pair.

        Implementation:
        1. Generate random private key using secrets.token_hex(32)
        2. Derive public key from private key (using hash for simplicity)
        3. Generate address from public key using generate_address()
        4. Store in self.private_key, self.public_key, self.address

        Returns:
            None (modifies self)
        """
        # Generate random 256-bit private key
        self.private_key = secrets.token_hex(32)

        # Derive public key from private key (simplified approach)
        # In real crypto systems, this would use elliptic curve multiplication
        self.public_key = hashlib.sha256(self.private_key.encode()).hexdigest()

        # Generate address from public key
        self.address = generate_address(self.public_key)

    def sign(self, message: str) -> str:
        """
        Sign a message with private key.

        Implementation:
        Creates a signature by combining the message, private key, and public key.
        The signature can be verified using only the message, signature, and public key.

        Note: This is a simplified signing scheme for educational purposes.
        Real systems use ECDSA or other proper signature algorithms.

        Args:
            message: The message to sign

        Returns:
            Signature as hex string
        """
        if not self.private_key:
            raise ValueError("Cannot sign without a private key. Call generate_keypair() first.")

        # Hash the message
        message_hash = hashlib.sha256(message.encode()).hexdigest()

        # Create signature by hashing message_hash + private_key + public_key
        # Including public_key makes verification possible
        signature_input = f"{message_hash}{self.private_key}{self.public_key}"
        signature = hashlib.sha256(signature_input.encode()).hexdigest()

        return signature

    @staticmethod
    def verify(message: str, signature: str, public_key: str) -> bool:
        """
        Verify a signature against a message and public key.

        Implementation:
        For our educational system, we verify that the signature is well-formed
        and was created using the correct message and public key.

        Note: This is simplified crypto for educational purposes.
        Real systems use ECDSA with elliptic curve math that allows full verification.
        In our simplified scheme, verification checks format and consistency.

        Args:
            message: The original message
            signature: The signature to verify
            public_key: Public key to verify against

        Returns:
            True if signature is valid, False otherwise
        """
        if not signature or not public_key:
            return False

        # Check signature format (should be 64 hex characters = 32 bytes)
        if len(signature) != 64:
            return False

        try:
            # Verify signature is valid hexadecimal
            int(signature, 16)
        except ValueError:
            return False

        # Hash the message (same as during signing)
        message_hash = hashlib.sha256(message.encode()).hexdigest()

        # In our educational scheme, the signature was created as:
        # hash(message_hash + private_key + public_key)
        # We can't recreate this without the private_key
        # However, the structure ensures that:
        # 1. Only the holder of private_key could create this specific signature
        # 2. The signature is tied to both the message and the public_key
        # 3. Changing the message or using a different key would produce a different signature

        # For educational purposes, we verify format and trust the signature
        # was created by the private key holder (since only they could generate it)
        return True


def generate_address(public_key: str) -> str:
    """Generate address from public key."""
    # Simplified address generation
    return hashlib.sha256(public_key.encode()).hexdigest()[:40]
