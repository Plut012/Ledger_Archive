#!/usr/bin/env python3
"""Live test of character system with real LLM calls."""

import asyncio
import json
from llm.client import LLMClient
from db.mongo import mongo_client
from db.sessions import SessionManager
from characters.archivist import ArchivistController
from characters.witness import WitnessController


async def test_character_conversation():
    """Test live character conversations."""
    print("=" * 60)
    print("CHAIN OF TRUTH - Live Character Test")
    print("=" * 60)
    print()

    # Setup
    await mongo_client.connect()
    session_manager = SessionManager(mongo_client)
    await session_manager.initialize()

    llm_client = LLMClient()
    print(f"✓ Using {llm_client.provider} with model {llm_client.model}")
    print()

    # Create session
    session_id = await session_manager.create_session()
    session = await session_manager.get_session(session_id)
    game_state = session["game_state"]

    # Test ARCHIVIST
    print("=" * 60)
    print("Testing ARCHIVIST")
    print("=" * 60)
    print()

    archivist = ArchivistController(llm_client, session_manager)

    print("Q: What is a blockchain?")
    print("A: ", end="", flush=True)

    async for chunk in archivist.respond(
        session_id=session_id,
        user_message="What is a blockchain?",
        game_state=game_state
    ):
        if chunk.get("chunk"):
            print(chunk["chunk"], end="", flush=True)
        if chunk.get("done"):
            print("\n")
            if chunk.get("stateUpdates"):
                print(f"State updates: {chunk['stateUpdates']}")

    print()

    # Test restricted topic
    print("Q: Tell me about the Witness")
    print("A: ", end="", flush=True)

    async for chunk in archivist.respond(
        session_id=session_id,
        user_message="Tell me about the Witness",
        game_state=game_state
    ):
        if chunk.get("chunk"):
            print(chunk["chunk"], end="", flush=True)
        if chunk.get("done"):
            print("\n")
            if chunk.get("stateUpdates"):
                print(f"State updates: {chunk['stateUpdates']}")
                if "archivistSuspicion" in chunk["stateUpdates"]:
                    print(f"✓ Suspicion increased to {chunk['stateUpdates']['archivistSuspicion']}")

    print()

    # Test WITNESS
    print("=" * 60)
    print("Testing WITNESS (low trust = cryptic)")
    print("=" * 60)
    print()

    witness = WitnessController(llm_client, session_manager)

    print("Q: Who are you?")
    print("A: ", end="", flush=True)

    async for chunk in witness.respond(
        session_id=session_id,
        user_message="Who are you?",
        game_state=game_state
    ):
        if chunk.get("chunk"):
            print(chunk["chunk"], end="", flush=True)
        if chunk.get("done"):
            print("\n")
            if chunk.get("stateUpdates"):
                print(f"State updates: {chunk['stateUpdates']}")

    print()

    # Cleanup
    await session_manager.sessions.delete_one({"session_id": session_id})
    await mongo_client.disconnect()

    print("=" * 60)
    print("✓ Live character test complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_character_conversation())
