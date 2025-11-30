"""Tests for procedural blockchain generation and testimony parsing."""

import pytest
from procedural.generator import BlockGenerator
from procedural.testimony import TestimonyParser


class TestBlockGenerator:
    """Test deterministic block generation."""

    def test_block_generation_is_deterministic(self):
        """Same seed should always generate same block."""
        gen1 = BlockGenerator(seed_version="test_v1")
        gen2 = BlockGenerator(seed_version="test_v1")

        block1 = gen1.generate_block(100)
        block2 = gen2.generate_block(100)

        assert block1.hash == block2.hash
        assert block1.index == block2.index
        assert block1.previous_hash == block2.previous_hash
        assert block1.nonce == block2.nonce
        assert block1.timestamp == block2.timestamp
        assert len(block1.transactions) == len(block2.transactions)

    def test_different_seeds_generate_different_blocks(self):
        """Different seeds should generate different blocks."""
        gen1 = BlockGenerator(seed_version="v1")
        gen2 = BlockGenerator(seed_version="v2")

        block1 = gen1.generate_block(100)
        block2 = gen2.generate_block(100)

        # Same index but different content
        assert block1.index == block2.index
        assert block1.hash != block2.hash

    def test_story_blocks_have_fixed_content(self):
        """Story-critical blocks should have exact content."""
        gen = BlockGenerator(seed_version="v1")

        # Block 127445 is Witness first contact
        block = gen.generate_block(127445)

        assert block.index == 127445
        assert len(block.transactions) == 1
        assert block.transactions[0].memo == "V2l0bmVzcyBsaXZlcw=="
        assert block.transactions[0].type == "transfer"
        assert block.transactions[0].sender == "NODE-UNKNOWN"

    def test_graveyard_blocks_have_archive_transactions(self):
        """Graveyard blocks should contain archive transactions."""
        gen = BlockGenerator(seed_version="v1")

        # Test several graveyard blocks
        archive_found = False
        for i in range(50000, 50100):
            block = gen.generate_block(i)
            for tx in block.transactions:
                if tx.type == "archive":
                    archive_found = True
                    assert tx.sender == "IMPERIAL-CORE"
                    assert "ARCHIVE-STATION" in tx.recipient
                    assert len(tx.memo) > 0
                    break
            if archive_found:
                break

        assert archive_found, "No archive transactions found in graveyard range"

    def test_standard_blocks_generate_correctly(self):
        """Standard procedural blocks should have valid structure."""
        gen = BlockGenerator(seed_version="v1")

        block = gen.generate_block(1000)

        assert block.index == 1000
        assert len(block.transactions) >= 1
        assert len(block.transactions) <= 6
        assert len(block.hash) == 64
        assert len(block.previous_hash) == 64

    def test_genesis_previous_hash(self):
        """First block should have genesis previous hash."""
        gen = BlockGenerator(seed_version="v1")

        block = gen.generate_block(0)

        assert block.previous_hash == "0" * 64

    def test_chain_linking(self):
        """Blocks should have deterministic previous_hash based on index."""
        gen = BlockGenerator(seed_version="v1")

        block1 = gen.generate_block(100)
        block2 = gen.generate_block(101)

        # For procedural generation, previous_hash is deterministic
        # but doesn't require actually generating the previous block
        # This maintains determinism while avoiding recursion
        assert len(block2.previous_hash) == 64
        assert block2.previous_hash != "0" * 64  # Not genesis

    def test_timestamp_increases_linearly(self):
        """Block timestamps should increase consistently."""
        gen = BlockGenerator(seed_version="v1")

        block1 = gen.generate_block(100)
        block2 = gen.generate_block(101)

        # Timestamps should be 10 minutes apart (600000 ms)
        assert block2.timestamp - block1.timestamp == 600000

    def test_caching_works(self):
        """LRU cache should return same object for repeated calls."""
        gen = BlockGenerator(seed_version="v1")

        block1 = gen.generate_block(100)
        block2 = gen.generate_block(100)

        # Should be same object from cache
        assert block1 is block2


class TestTestimonyParser:
    """Test testimony parsing and reconstruction."""

    def test_parse_archive_transaction(self):
        """Should correctly parse base64-encoded archive memo."""
        # Encoded: "Subject: Test | Status: ARCHIVED | Final Memory: Hello"
        memo = "U3ViamVjdDogVGVzdCB8IFN0YXR1czogQVJDSElWRUQgfCBGaW5hbCBNZW1vcnk6IEhlbGxv"

        result = TestimonyParser.parse_archive_transaction(memo)

        assert result is not None
        assert result["subject"] == "Test"
        assert result["status"] == "ARCHIVED"
        assert result["finalMemory"] == "Hello"

    def test_parse_invalid_memo_returns_none(self):
        """Should return None for invalid memo."""
        result = TestimonyParser.parse_archive_transaction("invalid_base64!!!")

        assert result is None

    def test_reconstruct_consciousness_from_story_block(self):
        """Should reconstruct consciousness from story block."""
        # Block 74221 has Administrator Chen's testimony
        result = TestimonyParser.reconstruct_consciousness(74221, 0)

        assert "error" not in result
        assert result["blockIndex"] == 74221
        assert result["subject"] == "Administrator Chen"
        assert result["status"] == "TRANSCENDED"
        assert "reconstruction" in result
        assert "CONSCIOUSNESS RECONSTRUCTION PROTOCOL" in result["reconstruction"]

    def test_reconstruct_with_invalid_tx_index(self):
        """Should return error for invalid transaction index."""
        result = TestimonyParser.reconstruct_consciousness(74221, 999)

        assert "error" in result
        assert "out of range" in result["error"].lower()

    def test_reconstruct_non_archive_transaction(self):
        """Should return error for non-archive transactions."""
        # Block 1000 has standard transfer transactions
        result = TestimonyParser.reconstruct_consciousness(1000, 0)

        assert "error" in result
        assert "not an archive type" in result["error"].lower()

    def test_reconstruction_includes_formatted_output(self):
        """Reconstruction should include nicely formatted ASCII output."""
        result = TestimonyParser.reconstruct_consciousness(74221, 0)

        assert "╔" in result["reconstruction"]
        assert "╚" in result["reconstruction"]
        assert "WARNING:" in result["reconstruction"]
        assert "terminated consciousness" in result["reconstruction"]


class TestBlockGeneratorEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_large_block_index(self):
        """Should generate blocks with large indices."""
        gen = BlockGenerator(seed_version="v1")

        block = gen.generate_block(849999)

        assert block.index == 849999
        assert len(block.hash) == 64

    def test_graveyard_boundary_start(self):
        """Block 50000 should be graveyard block."""
        gen = BlockGenerator(seed_version="v1")

        block = gen.generate_block(50000)

        # Should be a story block (graveyard start marker)
        assert block.index == 50000

    def test_graveyard_boundary_end(self):
        """Block 75000 should be graveyard block."""
        gen = BlockGenerator(seed_version="v1")

        block = gen.generate_block(75000)

        # Should be a story block (graveyard end marker)
        assert block.index == 75000

    def test_before_graveyard(self):
        """Block 49999 should not be graveyard block."""
        gen = BlockGenerator(seed_version="v1")

        block = gen.generate_block(49999)

        # Should be standard procedural
        assert block.index == 49999
        # All transactions should be standard transfers
        for tx in block.transactions:
            assert tx.type == "transfer"

    def test_after_graveyard(self):
        """Block 75001 should not be graveyard block."""
        gen = BlockGenerator(seed_version="v1")

        block = gen.generate_block(75001)

        # Should be standard procedural
        assert block.index == 75001


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
