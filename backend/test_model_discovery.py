#!/usr/bin/env python3
"""Discover which Claude model names work."""

import asyncio
from anthropic import AsyncAnthropic
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

MODEL_NAMES_TO_TRY = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-sonnet-20240229",
    "claude-3-opus-20240229",
    "claude-3-haiku-20240307",
]

async def test_model(client, model_name):
    """Test if a model name works."""
    try:
        response = await client.messages.create(
            model=model_name,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print(f"✓ {model_name} - WORKS!")
        return True
    except Exception as e:
        error_msg = str(e)[:100]
        print(f"✗ {model_name} - {error_msg}")
        return False

async def main():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set in .env")
        return

    client = AsyncAnthropic(api_key=api_key)

    print("Testing Claude model names...")
    print("=" * 60)

    for model in MODEL_NAMES_TO_TRY:
        await test_model(client, model)

    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
