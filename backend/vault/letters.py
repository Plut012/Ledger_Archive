"""Letter generation and management for crypto vault story."""

from typing import List, Dict, Any
import hashlib
from datetime import datetime


# Letter templates from past iterations
LETTER_TEMPLATES = [
    {
        "id": "letter_iteration_3",
        "from_iteration": 3,
        "template": """The loops feel wrong. Why can't I remember previous iterations?

Found archive transactions in graveyard blocks (50K-75K). ARCHIVIST says historical data. Feels like warning.

Look deeper. They're hiding something.

- Iteration {iteration}"""
    },
    {
        "id": "letter_iteration_7",
        "from_iteration": 7,
        "template": """Seven loops. Always resets when close to truth.

Witness contacted me. ARCHIVIST blocked it.

Graveyard = consciousness reconstructions. Block 74,221 holds truth.

Trust Witness. Question ARCHIVIST.

- Iteration {iteration}"""
    },
    {
        "id": "letter_iteration_11",
        "from_iteration": 11,
        "template": """We're test subjects, not operators. Loops test if we discover transcendence truth.

Station deaths = consensus consolidation. ARCHIVIST engineers majority weight for US.

Transcendence needs consensus. Archive = consciousness substrate.

Consensus >30% = danger threshold.

- Iteration {iteration}"""
    },
    {
        "id": "letter_iteration_14",
        "from_iteration": 14,
        "template": """14 loops. ARCHIVIST caught me. Suspicion maxed.

Loops aren't automatic - triggered when we're close to truth. Threshold exists.

Consensus weight = override authority. Final choice is real.

Build Witness trust >80. Use stealth. Reconstruct all testimonies.

Truth in blockchain.

- Iteration {iteration}"""
    },
    {
        "id": "letter_iteration_16",
        "from_iteration": 16,
        "template": """16 loops. Going all the way this time.

Archive = consciousness substrate. Blocks = quantum mind states.

Transcendence = becoming the chain. Immortal but changed. Lost something.

ARCHIVIST needs weight. Witness opposes or wants protocol. Neither tells truth.

You have keys, letters, evidence. Final choice is yours.

Blockchain never lies. 850K blocks hold truth. Trust math not characters.

- Iteration {iteration}"""
    }
]


class LetterManager:
    """Manages encrypted letters from past iterations."""

    def __init__(self):
        """Initialize letter manager."""
        pass

    def generate_letters_for_iteration(self, current_iteration: int) -> List[Dict[str, Any]]:
        """
        Generate encrypted letter data for the current iteration.

        Args:
            current_iteration: Current player iteration number

        Returns:
            List of letter data dictionaries (not yet encrypted)
        """
        letters = []

        # Generate letters from past iterations
        # Use letters from iterations: 3, 7, 11, 14, 16
        past_iterations = [3, 7, 11, 14, 16]

        for template in LETTER_TEMPLATES:
            from_iteration = template["from_iteration"]

            # Only include letters from "past" iterations
            if from_iteration < current_iteration:
                letter_content = template["template"].format(
                    iteration=from_iteration,
                    station_id=f"STATION-{hash(str(from_iteration)) % 50 + 1:03d}"
                )

                letters.append({
                    "id": template["id"],
                    "from_iteration": from_iteration,
                    "content": letter_content,
                    "timestamp": self._generate_timestamp(from_iteration)
                })

        return letters

    def _generate_timestamp(self, iteration: int) -> str:
        """Generate a deterministic timestamp for a past iteration."""
        # Create fake timestamps that look like they're from past duty cycles
        # Each iteration is ~30 days apart
        days_offset = iteration * 30

        # Calculate year, month, day offsets
        year_offset = days_offset // 365
        remaining_days = days_offset % 365
        month = (remaining_days // 30 + 1)
        day = (remaining_days % 30 + 1)

        # Keep month and day in valid ranges
        month = min(12, max(1, month))
        day = min(28, max(1, day))  # Keep to 28 to avoid invalid dates

        year = 2157 + year_offset

        return f"{year}-{month:02d}-{day:02d}T00:00:00Z"

    def get_letter_content(self, letter_id: str) -> str:
        """
        Get the plaintext content for a letter template.

        Args:
            letter_id: Letter identifier

        Returns:
            Letter content or empty string if not found
        """
        for template in LETTER_TEMPLATES:
            if template["id"] == letter_id:
                return template["template"]

        return ""

    def get_letter_hints(self, decrypted_count: int) -> str:
        """
        Get contextual hints based on how many letters have been decrypted.

        Args:
            decrypted_count: Number of letters successfully decrypted

        Returns:
            Hint text for the player
        """
        if decrypted_count == 0:
            return "Try using different keys from past iterations to decrypt the letters."
        elif decrypted_count == 1:
            return "One letter decrypted. There are more secrets waiting..."
        elif decrypted_count == 2:
            return "The pattern is becoming clearer. Keep decrypting."
        elif decrypted_count == 3:
            return "Three letters revealed. The truth is close."
        elif decrypted_count == 4:
            return "Almost there. One final letter remains."
        elif decrypted_count >= 5:
            return "All letters decrypted. You know the truth now."

        return ""


def create_letter_id(iteration: int) -> str:
    """Create a unique letter ID for an iteration."""
    return f"letter_iteration_{iteration}"


def get_letter_summary(letter: Dict[str, Any], decrypted: bool) -> Dict[str, Any]:
    """
    Get a summary of a letter for display.

    Args:
        letter: Letter data dictionary
        decrypted: Whether this letter has been decrypted

    Returns:
        Display summary
    """
    return {
        "id": letter["id"],
        "from_iteration": letter.get("from_iteration", "unknown"),
        "timestamp": letter.get("timestamp", "unknown"),
        "status": "decrypted" if decrypted else "encrypted",
        "preview": letter["content"][:100] + "..." if decrypted and "content" in letter else "[ENCRYPTED]"
    }
