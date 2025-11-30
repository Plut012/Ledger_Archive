"""Quick test of the blockchain API endpoints."""

from procedural.generator import BlockGenerator
from procedural.testimony import TestimonyParser


def test_block_generation():
    """Test that we can generate blocks."""
    gen = BlockGenerator()

    # Generate a standard block
    block = gen.generate_block(1000)
    print(f"✓ Generated block #1000: {block.hash[:16]}...")

    # Generate a graveyard block
    block = gen.generate_block(55000)
    print(f"✓ Generated graveyard block #55000")

    # Check for archive transactions
    for tx in block.transactions:
        if tx.type == "archive":
            print(f"  Found archive transaction: {tx.sender} → {tx.recipient}")
            break

    # Generate a story block
    block = gen.generate_block(127445)
    print(f"✓ Generated story block #127445 (Witness first contact)")
    print(f"  Memo: {block.transactions[0].memo}")


def test_testimony_reconstruction():
    """Test consciousness reconstruction."""
    # Reconstruct from story block
    result = TestimonyParser.reconstruct_consciousness(74221, 0)

    if "error" not in result:
        print(f"✓ Reconstructed consciousness from block #74221")
        print(f"  Subject: {result['subject']}")
        print(f"  Status: {result['status']}")
        print(f"  Final Memory: {result['finalMemory']}")
    else:
        print(f"✗ Reconstruction failed: {result['error']}")


if __name__ == "__main__":
    print("Testing Procedural Blockchain Generation...")
    print()
    test_block_generation()
    print()
    test_testimony_reconstruction()
    print()
    print("All tests passed! ✓")
