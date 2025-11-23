"""Block data structure and hashing logic."""

from dataclasses import dataclass, field
from typing import List
import hashlib
import json
import time


@dataclass
class Block:
    """A single block in the blockchain."""

    index: int
    timestamp: str
    transactions: List[dict]
    previous_hash: str
    nonce: int = 0
    hash: str = field(default="", init=False)

    def __post_init__(self):
        """Calculate hash after initialization."""
        if not self.hash:
            self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Generate SHA-256 hash of block contents."""
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create block from dictionary."""
        return cls(
            index=data["index"],
            timestamp=data["timestamp"],
            transactions=data["transactions"],
            previous_hash=data["previous_hash"],
            nonce=data["nonce"]
        )


def get_timestamp() -> str:
    """Get current timestamp in consistent format."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
