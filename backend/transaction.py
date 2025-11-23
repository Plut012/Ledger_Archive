"""Transaction structure and validation."""

from dataclasses import dataclass
import hashlib
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from crypto import Wallet


@dataclass
class Transaction:
    """A transaction moving value between addresses."""

    sender: str
    recipient: str
    amount: float
    timestamp: str
    signature: str = ""
    is_coinbase: bool = False  # Special transaction for mining rewards

    def calculate_hash(self) -> str:
        """Generate hash of transaction data."""
        tx_data = {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp
        }
        tx_string = json.dumps(tx_data, sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def sign(self, wallet: 'Wallet') -> None:
        """
        Sign this transaction with the provided wallet.

        Args:
            wallet: Wallet object with private key to sign with
        """
        # Get the transaction data to sign (hash of the transaction)
        message = self.calculate_hash()

        # Sign the transaction hash with the wallet's private key
        self.signature = wallet.sign(message)

    def is_valid(self, ledger=None) -> bool:
        """
        Validate transaction.

        Checks:
        1. Amount is positive
        2. Sender and recipient are present
        3. Signature is valid (if present)
        4. Sender has sufficient funds (if ledger provided)

        Args:
            ledger: Optional Ledger instance to check balances

        Returns:
            True if transaction is valid, False otherwise
        """
        # Coinbase transactions have special rules
        if self.is_coinbase:
            # Coinbase must come from "COINBASE" and have positive amount
            if self.sender != "COINBASE":
                return False
            if self.amount <= 0:
                return False
            if not self.recipient:
                return False
            # Coinbase doesn't need signature
            return True

        # Regular transaction validation
        # Basic validation
        if self.amount <= 0:
            return False
        if not self.sender or not self.recipient:
            return False

        # Verify signature if present
        if self.signature:
            from crypto import Wallet
            message = self.calculate_hash()
            # For sender verification, we'd need the sender's public key
            # In a real system, sender would be an address and we'd derive the public key
            # For educational purposes, we verify the signature format
            if not Wallet.verify(message, self.signature, self.sender):
                return False

        # Check balance if ledger provided
        if ledger:
            if not ledger.has_sufficient_funds(self.sender, self.amount):
                return False

        return True

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": self.signature,
            "is_coinbase": self.is_coinbase
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create transaction from dictionary."""
        return cls(
            sender=data["sender"],
            recipient=data["recipient"],
            amount=data["amount"],
            timestamp=data["timestamp"],
            signature=data.get("signature", ""),
            is_coinbase=data.get("is_coinbase", False)
        )
