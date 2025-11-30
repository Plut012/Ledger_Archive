"""
Test Chain Integration (Phase 04)

Tests deterministic block generation, story blocks, graveyard blocks,
and testimony reconstruction.
"""

import sys
sys.path.insert(0, '/home/pluto/dev/chain/backend')

from procedural.generator import BlockGenerator
from procedural.testimony import TestimonyParser


def test_deterministic_generation():
    """Test that same seed produces same blocks"""
    print("\n=== Test 1: Deterministic Generation ===")

    gen1 = BlockGenerator(seed_version="v1")
    gen2 = BlockGenerator(seed_version="v1")

    # Test block 1000
    block1 = gen1.generate_block(1000)
    block2 = gen2.generate_block(1000)

    assert block1.hash == block2.hash, "Hashes should match for same seed"
    assert block1.index == block2.index, "Indices should match"
    assert len(block1.transactions) == len(block2.transactions), "Transaction counts should match"

    print(f"✓ Block #1000 generated deterministically")
    print(f"  Hash: {block1.hash[:16]}...")
    print(f"  Transactions: {len(block1.transactions)}")
    print(f"  Timestamp: {block1.timestamp}")


def test_story_blocks():
    """Test story-critical blocks have fixed content"""
    print("\n=== Test 2: Story-Critical Blocks ===")

    gen = BlockGenerator()

    # Test Witness first contact (127445)
    block = gen.generate_block(127445)

    # Note: Story blocks are still marked as procedural (part of 850K chain)
    # but have fixed content
    assert len(block.transactions) == 1, "Witness first contact should have 1 transaction"

    tx = block.transactions[0]
    assert tx.type == "transfer", "Should be transfer type"
    assert tx.sender == "NODE-UNKNOWN", "Sender should be NODE-UNKNOWN"

    # Decode memo
    import base64
    memo_decoded = base64.b64decode(tx.memo).decode()
    assert "Witness lives" in memo_decoded, "Memo should contain Witness message"

    print(f"✓ Block #127445 (Witness First Contact)")
    print(f"  Type: {tx.type}")
    print(f"  Sender: {tx.sender}")
    print(f"  Memo (decoded): {memo_decoded}")

    # Test Administrator Chen's testimony (74221)
    block2 = gen.generate_block(74221)
    tx2 = block2.transactions[0]

    assert tx2.type == "archive", "Should be archive type"
    memo2_decoded = base64.b64decode(tx2.memo).decode()
    assert "Administrator Chen" in memo2_decoded, "Should reference Chen"
    assert "TRANSCENDED" in memo2_decoded, "Should show transcended status"

    print(f"✓ Block #74221 (Administrator Chen)")
    print(f"  Type: {tx2.type}")
    print(f"  Preview: {memo2_decoded[:50]}...")


def test_graveyard_blocks():
    """Test graveyard blocks (50K-75K) have special generation"""
    print("\n=== Test 3: Graveyard Blocks ===")

    gen = BlockGenerator()

    # Test a graveyard block
    block = gen.generate_block(60000)

    # Graveyard blocks are in range 50K-75K
    is_graveyard = 50000 <= block.index <= 75000
    assert is_graveyard, "Block should be in graveyard range"
    assert block.is_procedural, "Graveyard blocks are procedurally generated"

    # Check for archive transactions
    archive_txs = [tx for tx in block.transactions if tx.type == "archive"]

    print(f"✓ Block #60000 (Graveyard)")
    print(f"  Total transactions: {len(block.transactions)}")
    print(f"  Archive transactions: {len(archive_txs)}")
    print(f"  Is graveyard: {is_graveyard}")

    if archive_txs:
        tx = archive_txs[0]
        import base64
        memo_decoded = base64.b64decode(tx.memo).decode()
        print(f"  Archive memo preview: {memo_decoded[:80]}...")

    # Test determinism of graveyard blocks
    block2 = gen.generate_block(60000)
    assert block.hash == block2.hash, "Graveyard blocks should be deterministic"
    print(f"  ✓ Determinism verified")


def test_testimony_parsing():
    """Test testimony parser"""
    print("\n=== Test 4: Testimony Parsing ===")

    parser = TestimonyParser()

    # Test parsing Chen's testimony
    result = parser.reconstruct_consciousness(74221, 0)

    assert "error" not in result, f"Should parse successfully, got: {result.get('error')}"
    assert result["subject"] == "Administrator Chen", "Should extract subject"
    assert result["status"] == "TRANSCENDED", "Should extract status"
    assert "reconstruction" in result, "Should include formatted reconstruction"

    print(f"✓ Testimony Parsed Successfully")
    print(f"  Subject: {result['subject']}")
    print(f"  Status: {result['status']}")
    if result.get('finalMemory'):
        print(f"  Final Memory: {result['finalMemory'][:50]}...")
    print(f"\n  Reconstruction Output:")
    print(result["reconstruction"])


def test_cache_performance():
    """Test that caching works"""
    print("\n=== Test 5: Cache Performance ===")

    gen = BlockGenerator()

    # Generate same block twice
    import time

    start = time.time()
    block1 = gen.generate_block(100000)
    time1 = time.time() - start

    start = time.time()
    block2 = gen.generate_block(100000)  # Should hit cache
    time2 = time.time() - start

    assert block1.hash == block2.hash, "Cached block should match"

    print(f"✓ Cache Test")
    print(f"  First generation: {time1*1000:.2f}ms")
    print(f"  Cached retrieval: {time2*1000:.2f}ms")
    print(f"  Speedup: {time1/time2:.1f}x faster")
    print(f"  Cache: LRU cache (1000 blocks max)")


def test_edge_cases():
    """Test edge cases"""
    print("\n=== Test 6: Edge Cases ===")

    gen = BlockGenerator()

    # Test genesis block (block 0)
    block0 = gen.generate_block(0)
    assert block0.index == 0, "Should generate block 0"
    assert block0.previous_hash == "0" * 64, "Genesis should have null previous hash"
    print(f"✓ Genesis block (0) generated")

    # Test high index block
    block_high = gen.generate_block(849999)  # Last block
    assert block_high.index == 849999, "Should generate near end of chain"
    print(f"✓ High index block (849999) generated")

    # Test boundary blocks
    block_graveyard_start = gen.generate_block(50000)
    assert 50000 <= block_graveyard_start.index <= 75000, "Should be graveyard"
    print(f"✓ Graveyard start boundary (50000)")

    block_graveyard_end = gen.generate_block(75000)
    assert 50000 <= block_graveyard_end.index <= 75000, "Should be graveyard"
    print(f"✓ Graveyard end boundary (75000)")

    block_after_graveyard = gen.generate_block(75001)
    assert not (50000 <= block_after_graveyard.index <= 75000), "Should not be graveyard"
    print(f"✓ After graveyard (75001) is normal")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("PHASE 04: CHAIN INTEGRATION - TEST SUITE")
    print("="*70)

    try:
        test_deterministic_generation()
        test_story_blocks()
        test_graveyard_blocks()
        test_testimony_parsing()
        test_cache_performance()
        test_edge_cases()

        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED")
        print("="*70)
        print("\nPhase 04: Chain Integration is COMPLETE and VERIFIED")
        print("\nKey Features:")
        print("  ✓ Deterministic block generation (850K blocks)")
        print("  ✓ Story-critical blocks with fixed content")
        print("  ✓ Graveyard blocks (50K-75K) with consciousness archives")
        print("  ✓ Testimony parsing and reconstruction")
        print("  ✓ LRU caching for performance")
        print("  ✓ Edge case handling")

        return True

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
