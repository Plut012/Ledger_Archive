"""Economic constants for the blockchain."""

# Block reward for mining
BLOCK_REWARD = 50.0  # Credits per block

# Optional: Halving schedule (like Bitcoin, but much faster for demo)
HALVING_INTERVAL = 210  # Blocks between halvings


def get_block_reward(block_height: int) -> float:
    """
    Calculate block reward based on block height.
    Implements halving schedule for educational purposes.

    Args:
        block_height: Current height of the blockchain

    Returns:
        Block reward amount in credits
    """
    halvings = block_height // HALVING_INTERVAL
    reward = BLOCK_REWARD / (2 ** halvings)

    # Ensure reward never goes below minimum
    return max(reward, 0.0001)
