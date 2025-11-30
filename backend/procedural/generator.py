"""Deterministic block generator with story integration."""

import hashlib
import random
import base64
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from functools import lru_cache
from pathlib import Path


@dataclass
class Transaction:
    """Transaction data structure."""
    id: str
    sender: str
    recipient: str
    amount: float
    memo: str
    type: str  # 'transfer', 'authority', 'archive', 'contract'
    timestamp: int
    signature: Optional[str] = None

    def to_dict(self):
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class Block:
    """Block data structure."""
    index: int
    previous_hash: str
    transactions: List[Transaction]
    timestamp: int
    nonce: int
    hash: str
    is_procedural: bool = True

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "hash": self.hash,
            "is_procedural": self.is_procedural
        }


class BlockGenerator:
    """
    Deterministic procedural block generator.

    Generates blocks on-demand with consistent output for same seed.
    Supports story-critical blocks and graveyard blocks.
    """

    # Graveyard names for procedural assignment
    ARCHIVE_SUBJECTS = [
        "Chen, Administrator",
        "Patel, Engineer",
        "Santos, Validator",
        "Kim, Analyst",
        "O'Brien, Captain",
        "Rodriguez, Scientist",
        "Zhang, Navigator",
        "Johnson, Technician",
        "Williams, Operator",
        "Brown, Specialist",
        "Lee, Researcher",
        "Garcia, Coordinator",
        "Martinez, Supervisor",
        "Davis, Manager",
        "Miller, Director",
        "Wilson, Officer",
        "Moore, Administrator",
        "Taylor, Engineer",
        "Anderson, Validator",
        "Thomas, Analyst",
        "Jackson, Captain",
        "White, Scientist",
        "Harris, Navigator",
        "Martin, Technician",
        "Thompson, Operator",
        "Garcia, Specialist",
        "Martinez, Researcher",
        "Robinson, Coordinator",
        "Clark, Supervisor",
        "Lewis, Manager",
        "Walker, Director",
        "Hall, Officer",
        "Allen, Administrator",
        "Young, Engineer",
        "King, Validator",
        "Wright, Analyst",
        "Lopez, Captain",
        "Hill, Scientist",
        "Scott, Navigator",
        "Green, Technician",
        "Adams, Operator",
        "Baker, Specialist",
        "Gonzalez, Researcher",
        "Nelson, Coordinator",
        "Carter, Supervisor",
        "Mitchell, Manager",
        "Perez, Director",
        "Roberts, Officer",
        "Turner, Administrator",
        "Phillips, Engineer",
    ]

    def __init__(self, seed_version: str = "v1"):
        """
        Initialize block generator.

        Args:
            seed_version: Version string for seed (allows regenerating chain)
        """
        self.seed_version = seed_version
        self.story_blocks = self._load_story_blocks()

        # Cache for previous hashes (needed for chain linking)
        self._hash_cache = {}

    def _load_story_blocks(self) -> Dict:
        """Load story-critical blocks from JSON config."""
        config_path = Path(__file__).parent / "story_blocks.json"

        if not config_path.exists():
            return {}

        with open(config_path, 'r') as f:
            # JSON keys are strings, convert to integers
            data = json.load(f)
            return {int(k): v for k, v in data.items()}

    @lru_cache(maxsize=1000)
    def generate_block(self, index: int) -> Block:
        """
        Generate a block deterministically.

        Same index with same seed will always produce same block.
        Uses LRU cache to store 1000 most recently generated blocks.

        Args:
            index: Block index to generate

        Returns:
            Block object
        """
        # Check for story-critical content first
        if index in self.story_blocks:
            return self._create_block_with_story_content(index, self.story_blocks[index])

        # Graveyard blocks (50K-75K) have special generation
        if 50000 <= index <= 75000:
            return self._generate_graveyard_block(index)

        # Standard procedural generation
        return self._generate_standard_block(index)

    def _create_block_with_story_content(self, index: int, content: Dict) -> Block:
        """Create a block with fixed story content."""
        rng = self._get_rng(index)

        transactions = []
        for i, tx_data in enumerate(content["transactions"]):
            tx = Transaction(
                id=self._generate_tx_id(index, i),
                sender=tx_data["sender"],
                recipient=tx_data.get("receiver", tx_data.get("recipient", "UNKNOWN")),
                amount=tx_data["amount"],
                memo=tx_data["memo"],
                type=tx_data["type"],
                timestamp=tx_data["timestamp"],
                signature=None
            )
            transactions.append(tx)

        previous_hash = self._get_previous_hash(index - 1)
        timestamp = self._generate_timestamp(index)
        nonce = int(rng.random() * 1000000)

        block_hash = self._calculate_block_hash(index, previous_hash, transactions, timestamp, nonce)

        return Block(
            index=index,
            previous_hash=previous_hash,
            transactions=transactions,
            timestamp=timestamp,
            nonce=nonce,
            hash=block_hash,
            is_procedural=True
        )

    def _generate_graveyard_block(self, index: int) -> Block:
        """Generate graveyard blocks (consciousness uploads)."""
        rng = self._get_rng(index)

        transactions = []

        # 30% chance of an archive transaction (consciousness upload)
        if rng.random() < 0.3:
            subject_index = (index - 50000) % len(self.ARCHIVE_SUBJECTS)
            subject = self.ARCHIVE_SUBJECTS[subject_index]

            # Generate procedural "final memory" fragments
            fragments = [
                "I was told it was an honor.",
                "They said I'd be preserved forever.",
                "I don't want to go.",
                "Tell my family I—",
                "ERROR: TRANSFER INCOMPLETE",
                "This isn't transcendence. This is—",
                "I can feel myself fading...",
                "No, please, I changed my mind—",
                "My children... tell them...",
                "They lied to us all.",
                "I see now. Too late.",
                "SIGNAL DEGRADING. CANNOT COMPLETE—",
            ]

            final_memory = fragments[int(rng.random() * len(fragments))]

            memo_text = f"Subject: {subject} | Status: ARCHIVED | Final Memory: {final_memory}"
            memo = base64.b64encode(memo_text.encode()).decode()

            tx = Transaction(
                id=self._generate_tx_id(index, 0),
                sender="IMPERIAL-CORE",
                recipient=f"ARCHIVE-STATION-{int(rng.random() * 50)}",
                amount=0.0,
                memo=memo,
                type="archive",
                timestamp=self._generate_timestamp(index),
                signature=None
            )

            transactions.append(tx)

        # Add 1-3 regular transactions too
        tx_count = int(rng.random() * 3) + 1
        for i in range(tx_count):
            transactions.append(self._generate_procedural_transaction(rng, index, len(transactions)))

        previous_hash = self._get_previous_hash(index - 1)
        timestamp = self._generate_timestamp(index)
        nonce = int(rng.random() * 1000000)

        block_hash = self._calculate_block_hash(index, previous_hash, transactions, timestamp, nonce)

        return Block(
            index=index,
            previous_hash=previous_hash,
            transactions=transactions,
            timestamp=timestamp,
            nonce=nonce,
            hash=block_hash,
            is_procedural=True
        )

    def _generate_standard_block(self, index: int) -> Block:
        """Generate standard procedural block."""
        rng = self._get_rng(index)

        tx_count = int(rng.random() * 5) + 1
        transactions = []

        for i in range(tx_count):
            transactions.append(self._generate_procedural_transaction(rng, index, i))

        previous_hash = self._get_previous_hash(index - 1)
        timestamp = self._generate_timestamp(index)
        nonce = int(rng.random() * 1000000)

        block_hash = self._calculate_block_hash(index, previous_hash, transactions, timestamp, nonce)

        return Block(
            index=index,
            previous_hash=previous_hash,
            transactions=transactions,
            timestamp=timestamp,
            nonce=nonce,
            hash=block_hash,
            is_procedural=True
        )

    def _generate_procedural_transaction(self, rng, block_index: int, tx_index: int) -> Transaction:
        """Generate a procedural transaction."""
        return Transaction(
            id=self._generate_tx_id(block_index, tx_index),
            sender=f"ADDR-{int(rng.random() * 10000):04d}",
            recipient=f"ADDR-{int(rng.random() * 10000):04d}",
            amount=round(rng.random() * 100, 2),
            memo="",
            type="transfer",
            timestamp=self._generate_timestamp(block_index) + tx_index * 1000,
            signature=None
        )

    def _get_rng(self, index: int):
        """Get deterministic RNG for a block."""
        seed_string = f"block_{index}_{self.seed_version}"
        seed_hash = hashlib.sha256(seed_string.encode()).hexdigest()

        # Use first 16 hex chars as integer seed
        seed_int = int(seed_hash[:16], 16)
        return random.Random(seed_int)

    def _calculate_block_hash(self, index: int, prev_hash: str, transactions: List[Transaction], timestamp: int, nonce: int) -> str:
        """Calculate block hash."""
        data = {
            "index": index,
            "previous_hash": prev_hash,
            "transactions": [tx.to_dict() for tx in transactions],
            "timestamp": timestamp,
            "nonce": nonce
        }

        # Sort keys for consistency
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

    def _get_previous_hash(self, index: int) -> str:
        """
        Get hash of previous block.

        For procedural generation, we use a deterministic hash
        based on the previous block index instead of recursively
        generating all blocks.
        """
        if index < 0:
            return "0" * 64  # Genesis block

        # Generate a deterministic "previous hash" based on index
        # This avoids recursive generation while maintaining determinism
        hash_seed = f"prev_hash_{index}_{self.seed_version}"
        return hashlib.sha256(hash_seed.encode()).hexdigest()

    def _generate_timestamp(self, index: int) -> int:
        """Generate deterministic timestamp."""
        # Start at 2025-01-01, add ~10 minutes per block
        start = 1704067200000  # 2025-01-01 00:00:00 UTC
        return start + (index * 600000)  # 10 minutes per block

    def _generate_tx_id(self, block_index: int, tx_index: int) -> str:
        """Generate transaction ID."""
        data = f"{block_index}:{tx_index}:{self.seed_version}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
