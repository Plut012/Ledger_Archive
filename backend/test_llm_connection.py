#!/usr/bin/env python3
"""Quick test of LLM connection with actual API call."""

import asyncio
from llm.client import LLMClient


async def test_llm():
    """Test basic LLM functionality."""
    print("Testing LLM connection...")
    print("=" * 60)

    try:
        # Initialize client (will use ANTHROPIC_API_KEY from .env)
        client = LLMClient()
        print(f"✓ LLM client initialized")
        print(f"  Provider: {client.provider}")
        print(f"  Model: {client.model}")
        print()

        # Test non-streaming
        print("Testing non-streaming completion...")
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello from Claude!' in exactly 3 words."}
        ]

        response = await client.chat_completion(messages, max_tokens=50)
        print(f"✓ Response: {response}")
        print()

        # Test streaming
        print("Testing streaming completion...")
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Count to 5, one number per word."}
        ]

        print("Stream output: ", end="", flush=True)
        async for chunk in client.stream_chat_completion(messages, max_tokens=50):
            print(chunk, end="", flush=True)
        print()
        print("✓ Streaming complete")
        print()

        print("=" * 60)
        print("✓ All LLM tests passed!")
        print("Your API key is working correctly.")

    except Exception as e:
        print(f"✗ Error: {e}")
        print()
        print("Check your .env file:")
        print("  - ANTHROPIC_API_KEY should be set")
        print("  - LLM_PROVIDER should be 'anthropic'")
        return False

    return True


if __name__ == "__main__":
    asyncio.run(test_llm())
