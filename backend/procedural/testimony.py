"""Testimony parser for consciousness reconstruction."""

import base64
from typing import Dict, Optional
from .generator import BlockGenerator


class TestimonyParser:
    """Parse consciousness data from archive transactions."""

    @staticmethod
    def parse_archive_transaction(memo: str) -> Optional[Dict]:
        """
        Decode and parse archive transaction memo.

        Args:
            memo: Base64-encoded memo string

        Returns:
            Parsed testimony dict or None if parsing fails
        """
        try:
            decoded = base64.b64decode(memo).decode('utf-8')

            # Parse format: "Subject: Name | Status: X | Final Memory: Y"
            parts = {}
            for segment in decoded.split(" | "):
                if ": " in segment:
                    key, value = segment.split(": ", 1)
                    parts[key] = value

            return {
                "subject": parts.get("Subject"),
                "status": parts.get("Status"),
                "finalMemory": parts.get("Final Memory"),
                "raw": decoded
            }

        except Exception as e:
            return None

    @staticmethod
    def reconstruct_consciousness(block_index: int, tx_index: int = 0) -> Dict:
        """
        Perform 'reconstruction' of consciousness data.

        This retrieves the archive transaction and formats it as a
        ceremonial "reconstruction" output. In reality, these are
        final memories from terminated consciousnesses.

        Args:
            block_index: Block containing the archive transaction
            tx_index: Transaction index within the block (default: 0)

        Returns:
            Reconstruction result dict
        """
        generator = BlockGenerator()
        block = generator.generate_block(block_index)

        if tx_index >= len(block.transactions):
            return {"error": "Transaction index out of range"}

        tx = block.transactions[tx_index]

        if tx.type != "archive":
            return {"error": "Transaction is not an archive type"}

        testimony = TestimonyParser.parse_archive_transaction(tx.memo)

        if not testimony:
            return {"error": "Failed to parse testimony"}

        # Format timestamp
        from datetime import datetime
        timestamp_str = datetime.fromtimestamp(tx.timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S UTC')

        # Create formatted reconstruction output
        reconstruction_text = f"""
╔══════════════════════════════════════════════════════════════╗
║            CONSCIOUSNESS RECONSTRUCTION PROTOCOL             ║
║                    CLASSIFICATION: RESTRICTED                ║
╠══════════════════════════════════════════════════════════════╣
║ Subject: {testimony["subject"]:50s} ║
║ Archive Block: {block_index:<47d} ║
║ Status: {testimony["status"]:53s} ║
║ Timestamp: {timestamp_str:50s} ║
╠══════════════════════════════════════════════════════════════╣
║ FINAL MEMORY FRAGMENT:                                       ║
║                                                              ║
║ "{testimony["finalMemory"]}"
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║ WARNING: This data represents a terminated consciousness.   ║
║ Reconstruction is forensic only. No restoration possible.   ║
╚══════════════════════════════════════════════════════════════╝
"""

        return {
            "blockIndex": block_index,
            "transactionId": tx.id,
            "subject": testimony["subject"],
            "status": testimony["status"],
            "finalMemory": testimony["finalMemory"],
            "timestamp": tx.timestamp,
            "timestampFormatted": timestamp_str,
            "reconstruction": reconstruction_text.strip()
        }
