#!/usr/bin/env python3
"""Test script for character system - run this to verify everything works."""

import asyncio
import sys
from llm.client import LLMClient
from db.mongo import mongo_client
from db.sessions import SessionManager
from characters.archivist import ArchivistController
from characters.witness import WitnessController


async def test_setup():
    """Test basic setup and connectivity."""
    print("=" * 60)
    print("CHAIN OF TRUTH - Character System Test")
    print("=" * 60)
    print()

    # Test 1: MongoDB connection
    print("1. Testing MongoDB connection...")
    try:
        await mongo_client.connect()
        print("   ✓ MongoDB connected successfully")
    except Exception as e:
        print(f"   ✗ MongoDB connection failed: {e}")
        print("   Make sure MongoDB is running: ./start_mongodb.sh")
        return False

    # Test 2: Session manager
    print("2. Testing session manager...")
    try:
        session_manager = SessionManager(mongo_client)
        await session_manager.initialize()
        print("   ✓ Session manager initialized")
    except Exception as e:
        print(f"   ✗ Session manager failed: {e}")
        return False

    # Test 3: Create a test session
    print("3. Creating test session...")
    try:
        session_id = await session_manager.create_session()
        print(f"   ✓ Session created: {session_id}")
    except Exception as e:
        print(f"   ✗ Session creation failed: {e}")
        return False

    # Test 4: Retrieve session
    print("4. Retrieving session...")
    try:
        session = await session_manager.get_session(session_id)
        print(f"   ✓ Session retrieved")
        print(f"   - Iteration: {session['game_state']['iteration']}")
        print(f"   - Suspicion: {session['game_state']['archivistSuspicion']}")
        print(f"   - Trust: {session['game_state']['witnessTrust']}")
    except Exception as e:
        print(f"   ✗ Session retrieval failed: {e}")
        return False

    # Test 5: Update game state
    print("5. Testing game state updates...")
    try:
        await session_manager.update_game_state(session_id, {
            "archivistSuspicion": 25,
            "witnessTrust": 15
        })
        updated_session = await session_manager.get_session(session_id)
        assert updated_session['game_state']['archivistSuspicion'] == 25
        assert updated_session['game_state']['witnessTrust'] == 15
        print("   ✓ Game state updated successfully")
    except Exception as e:
        print(f"   ✗ Game state update failed: {e}")
        return False

    # Test 6: Add conversation messages
    print("6. Testing conversation storage...")
    try:
        await session_manager.add_message(session_id, "archivist", "user", "Hello ARCHIVIST")
        await session_manager.add_message(session_id, "archivist", "assistant", "Greetings, Captain.")

        conversation = await session_manager.get_conversation(session_id, "archivist")
        assert len(conversation) == 2
        print(f"   ✓ Conversation stored ({len(conversation)} messages)")
    except Exception as e:
        print(f"   ✗ Conversation storage failed: {e}")
        return False

    # Test 7: Character persona testing
    print("7. Testing character personas...")
    try:
        from characters.archivist import ArchivistPersona
        from characters.witness import WitnessPersona

        archivist_persona = ArchivistPersona()
        print("   ✓ ARCHIVIST persona initialized")
        print(f"   - Name: {archivist_persona.name}")
        print(f"   - Temperature: {archivist_persona.temperature}")
        print(f"   - Restricted topics: {len(archivist_persona.RESTRICTED_TOPICS)}")

        witness_persona = WitnessPersona()
        print("   ✓ WITNESS persona initialized")
        print(f"   - Name: {witness_persona.name}")
        print(f"   - Temperature: {witness_persona.temperature}")
        print(f"   - Trust thresholds: {len(witness_persona.TRUST_THRESHOLDS)}")
    except Exception as e:
        print(f"   ✗ Persona testing failed: {e}")
        return False

    # Cleanup
    print("\n8. Cleaning up test data...")
    try:
        await session_manager.sessions.delete_one({"session_id": session_id})
        print("   ✓ Test session deleted")
    except Exception as e:
        print(f"   ⚠ Cleanup warning: {e}")

    await mongo_client.disconnect()

    print()
    print("=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Set up your .env file with OPENAI_API_KEY")
    print("2. Start the server: python main.py")
    print("3. Test the API endpoints (see CHARACTER_SYSTEM_README.md)")
    print()

    return True


if __name__ == "__main__":
    result = asyncio.run(test_setup())
    sys.exit(0 if result else 1)
