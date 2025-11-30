"""Test script for narrative state system."""

import asyncio
import sys
from narrative.state import GameState, PersistentState, SessionState
from narrative.triggers import TriggerEngine
from narrative.loop import LoopManager


def test_basic_state():
    """Test basic state creation and manipulation."""
    print("=" * 50)
    print("TEST: Basic State Creation")
    print("=" * 50)

    state = GameState(
        persistent=PersistentState(),
        session=SessionState()
    )

    print(f"✓ Initial iteration: {state.persistent.iteration}")
    print(f"✓ Initial act: {state.session.current_act}")
    print(f"✓ Initial suspicion: {state.session.archivist_suspicion}")
    print(f"✓ Initial trust: {state.session.witness_trust}")
    print()


def test_state_serialization():
    """Test state to_dict and from_dict."""
    print("=" * 50)
    print("TEST: State Serialization")
    print("=" * 50)

    # Create state with some data
    state = GameState(
        persistent=PersistentState(iteration=5),
        session=SessionState(current_act=2, witness_trust=30)
    )

    # Add some data
    state.persistent.puzzles_solved.add("tutorial_complete")
    state.session.files_discovered.add(".boot_prev.log")

    # Serialize
    state_dict = state.to_dict()
    print(f"✓ Serialized state: {state_dict}")

    # Deserialize
    restored_state = GameState.from_dict(state_dict)
    print(f"✓ Restored iteration: {restored_state.persistent.iteration}")
    print(f"✓ Restored act: {restored_state.session.current_act}")
    print(f"✓ Restored puzzles: {restored_state.persistent.puzzles_solved}")
    print()


def test_triggers():
    """Test trigger system."""
    print("=" * 50)
    print("TEST: Trigger System")
    print("=" * 50)

    engine = TriggerEngine()
    state = GameState(
        persistent=PersistentState(),
        session=SessionState()
    )

    print(f"Initial act: {state.session.current_act}")
    print(f"Witness contacted: {state.session.witness_contacted}")

    # Add conditions to trigger Act 2
    state.persistent.puzzles_solved.add("tutorial_complete")
    state.session.files_discovered.add(".boot_prev.log")

    # Evaluate triggers
    state = engine.evaluate_all(state)

    print(f"✓ After triggers - Act: {state.session.current_act}")

    # Test witness emergence trigger
    state.session.files_discovered.add("memo_1")
    state.session.files_discovered.add("memo_2")
    state.session.files_discovered.add("memo_3")

    state = engine.evaluate_all(state)

    print(f"✓ Witness contacted: {state.session.witness_contacted}")
    print(f"✓ Files unlocked: {state.persistent.files_unlocked}")

    # Test graveyard access
    state.session.witness_trust = 45

    state = engine.evaluate_all(state)

    print(f"✓ Graveyard discovered: {state.session.graveyard_discovered}")
    print()


def test_loop_reset():
    """Test loop/iteration reset."""
    print("=" * 50)
    print("TEST: Loop Reset System")
    print("=" * 50)

    state = GameState(
        persistent=PersistentState(),
        session=SessionState()
    )

    # Add some progress
    state.session.current_act = 3
    state.session.archivist_suspicion = 50
    state.session.witness_trust = 40
    state.persistent.puzzles_solved.add("puzzle_1")

    print(f"Before reset - Iteration: {state.persistent.iteration}")
    print(f"Before reset - Act: {state.session.current_act}")
    print(f"Before reset - Suspicion: {state.session.archivist_suspicion}")
    print(f"Before reset - Puzzles: {state.persistent.puzzles_solved}")

    # Reset to next iteration
    state = LoopManager.reset_to_next_iteration(state, "HIGH_SUSPICION")

    print(f"✓ After reset - Iteration: {state.persistent.iteration}")
    print(f"✓ After reset - Act: {state.session.current_act}")
    print(f"✓ After reset - Suspicion: {state.session.archivist_suspicion}")
    print(f"✓ After reset - Puzzles (persistent): {state.persistent.puzzles_solved}")
    print(f"✓ Messages to future: {len(state.persistent.messages_to_future)} messages")
    print()


def test_llm_context_export():
    """Test LLM context export."""
    print("=" * 50)
    print("TEST: LLM Context Export")
    print("=" * 50)

    state = GameState(
        persistent=PersistentState(iteration=3),
        session=SessionState(
            current_act=2,
            archivist_suspicion=20,
            witness_trust=35
        )
    )

    state.persistent.puzzles_solved.add("tutorial_complete")
    state.session.recent_commands = ["help", "status", "ls"]

    context = state.export_for_llm()

    print("LLM Context:")
    import json
    print(json.dumps(context, indent=2))
    print()


def test_reset_message():
    """Test reset messages."""
    print("=" * 50)
    print("TEST: Reset Messages")
    print("=" * 50)

    messages = [
        ("PROTOCOL_DEVIATION", 5),
        ("HIGH_SUSPICION", 10),
        ("MANUAL_RESET", 15)
    ]

    for reason, iteration in messages:
        print(f"\n--- {reason} (Iteration {iteration}) ---")
        print(LoopManager.get_reset_message(iteration, reason))
    print()


def run_all_tests():
    """Run all tests."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 12 + "NARRATIVE STATE SYSTEM TESTS" + " " * 18 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")

    test_basic_state()
    test_state_serialization()
    test_triggers()
    test_loop_reset()
    test_llm_context_export()
    test_reset_message()

    print("=" * 50)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 50)
    print()


if __name__ == "__main__":
    run_all_tests()
