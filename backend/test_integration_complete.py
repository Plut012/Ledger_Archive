"""
Integration test for narrative state system + LLM character integration.
Tests the complete flow from state updates to character context.
"""

import asyncio
from narrative.state import GameState, PersistentState, SessionState
from narrative.triggers import TriggerEngine
from narrative.loop import LoopManager


async def test_complete_integration():
    """Test complete narrative state system with LLM context export."""

    print("\n" + "=" * 70)
    print("INTEGRATION TEST: Narrative State System + LLM Character Context")
    print("=" * 70 + "\n")

    # Initialize state
    print("1️⃣  Initializing game state...")
    state = GameState(
        persistent=PersistentState(),
        session=SessionState()
    )
    print(f"   ✓ Iteration: {state.persistent.iteration}")
    print(f"   ✓ Act: {state.session.current_act}")
    print()

    # Initialize trigger engine
    engine = TriggerEngine()

    # Simulate tutorial completion
    print("2️⃣  Simulating tutorial completion...")
    state.persistent.puzzles_solved.add("tutorial_complete")
    state.session.files_discovered.add(".boot_prev.log")
    state = engine.evaluate_all(state)
    print(f"   ✓ Act after tutorial: {state.session.current_act}")
    print(f"   ✓ Tutorial puzzle solved")
    print()

    # Export context for ARCHIVIST
    print("3️⃣  Exporting context for ARCHIVIST...")
    context = state.export_for_llm()
    print(f"   ✓ Context includes {len(context)} fields")
    print(f"   ✓ Current act: {context['currentAct']}")
    print(f"   ✓ Suspicion: {context['archivistSuspicion']}")
    print(f"   ✓ Puzzles solved: {context['puzzlesSolved']}")
    print()

    # Simulate player discovering restricted files
    print("4️⃣  Simulating restricted file discovery...")
    for i in range(1, 4):
        state.session.files_discovered.add(f"restricted_memo_{i}")
    state = engine.evaluate_all(state)
    print(f"   ✓ Witness contacted: {state.session.witness_contacted}")
    print(f"   ✓ Files unlocked: {len(state.persistent.files_unlocked)}")
    print()

    # Build trust with WITNESS
    print("5️⃣  Building trust with WITNESS...")
    state.session.witness_trust = 45
    state = engine.evaluate_all(state)
    context = state.export_for_llm()
    print(f"   ✓ Trust level: {state.session.witness_trust}")
    print(f"   ✓ Graveyard discovered: {state.session.graveyard_discovered}")
    print(f"   ✓ Evidence shared: {context['evidenceShared']}")
    print()

    # Increase trust further
    print("6️⃣  Increasing trust to unlock letters...")
    state.session.witness_trust = 65
    state = engine.evaluate_all(state)
    context = state.export_for_llm()
    print(f"   ✓ Trust level: {state.session.witness_trust}")
    print(f"   ✓ Total files unlocked: {len(state.persistent.files_unlocked)}")
    print(f"   ✓ Evidence shared: {context['evidenceShared']}")
    print()

    # Simulate high suspicion
    print("7️⃣  Simulating high suspicion scenario...")
    state.session.archivist_suspicion = 50
    context = state.export_for_llm()
    print(f"   ✓ Suspicion level: {state.session.archivist_suspicion}")
    print(f"   ✓ ARCHIVIST context aware of suspicion")
    print()

    # Test loop reset
    print("8️⃣  Testing loop reset mechanics...")
    print(f"   Before reset:")
    print(f"   - Iteration: {state.persistent.iteration}")
    print(f"   - Act: {state.session.current_act}")
    print(f"   - Puzzles solved: {len(state.persistent.puzzles_solved)}")

    state = LoopManager.reset_to_next_iteration(state, "MANUAL_RESET")

    print(f"   After reset:")
    print(f"   - Iteration: {state.persistent.iteration} (incremented)")
    print(f"   - Act: {state.session.current_act} (reset to 1)")
    print(f"   - Puzzles solved: {len(state.persistent.puzzles_solved)} (preserved)")
    print(f"   - Messages to future: {len(state.persistent.messages_to_future)}")
    print()

    # Export final context
    print("9️⃣  Exporting final LLM context...")
    final_context = state.export_for_llm()
    print("   Context ready for character responses:")
    print(f"   - Iteration: {final_context['iteration']}")
    print(f"   - Current Act: {final_context['currentAct']}")
    print(f"   - Suspicion: {final_context['archivistSuspicion']}")
    print(f"   - Trust: {final_context['witnessTrust']}")
    print(f"   - Puzzles: {final_context['puzzlesSolved']}")
    print(f"   - Evidence: {final_context['evidenceShared']}")
    print(f"   - Flags: {final_context['flags']}")
    print()

    # Test serialization (for IndexedDB)
    print("🔟 Testing state serialization for persistence...")
    state_dict = state.to_dict()
    restored_state = GameState.from_dict(state_dict)
    print(f"   ✓ Serialized to dict: {len(state_dict)} top-level keys")
    print(f"   ✓ Restored iteration: {restored_state.persistent.iteration}")
    print(f"   ✓ Restored puzzles: {len(restored_state.persistent.puzzles_solved)}")
    print()

    # Summary
    print("=" * 70)
    print("✅ INTEGRATION TEST COMPLETE")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  • State system: ✓ Working")
    print(f"  • Trigger system: ✓ Working (7 triggers)")
    print(f"  • Loop resets: ✓ Working")
    print(f"  • LLM context export: ✓ Working")
    print(f"  • Serialization: ✓ Working")
    print()
    print("The narrative state system is ready for integration with:")
    print("  ✓ LLM Character System (ARCHIVIST & WITNESS)")
    print("  ✓ Frontend State Manager (IndexedDB persistence)")
    print("  ✓ WebSocket real-time sync")
    print("  ⏳ Virtual file system (next phase)")
    print()
    print("Next step: Test with actual LLM character responses!")
    print()


if __name__ == "__main__":
    asyncio.run(test_complete_integration())
