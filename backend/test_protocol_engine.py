"""Unit tests for Protocol Engine (Smart Contracts) system."""

import pytest
from contracts.engine import ContractEngine
from contracts.executor import ContractExecutor
from contracts.templates import get_contract, list_contracts, get_unlocked_contracts, CONTRACT_TEMPLATES
from narrative.state import GameState, PersistentState, SessionState


# ============================================================================
# TEMPLATE TESTS
# ============================================================================

def test_get_contract_returns_valid_contract():
    """Test that get_contract returns a valid contract"""
    contract = get_contract("witness_reconstruction")
    assert contract is not None
    assert contract["id"] == "witness_reconstruction"
    assert "name" in contract
    assert "code" in contract
    assert "unlock_condition" in contract


def test_get_contract_returns_none_for_invalid_id():
    """Test that get_contract returns None for invalid IDs."""
    contract = get_contract("nonexistent_contract")
    assert contract is None


def test_list_contracts_returns_all_contracts():
    """Test that list_contracts returns metadata for all contracts."""
    contracts = list_contracts()
    assert len(contracts) == 5  # witness, imperial, archive, reset, testimony
    assert all("id" in c for c in contracts)
    assert all("name" in c for c in contracts)
    assert all("unlock_condition" in c for c in contracts)


def test_all_contracts_have_required_fields():
    """Test that all contracts have required fields."""
    for contract_id, contract in CONTRACT_TEMPLATES.items():
        assert "id" in contract
        assert "name" in contract
        assert "version" in contract
        assert "author" in contract
        assert "description" in contract
        assert "unlock_condition" in contract
        assert "code" in contract
        assert contract["code"].strip() != ""


# ============================================================================
# UNLOCK CONDITION TESTS
# ============================================================================

def test_unlock_based_on_witness_trust():
    """Test that contracts unlock based on witness trust."""
    state = GameState(
        persistent=PersistentState(),
        session=SessionState(witness_trust=50)
    )

    unlocked = get_unlocked_contracts(state)
    assert "witness_reconstruction" in unlocked  # requires 40 trust


def test_unlock_based_on_archivist_suspicion():
    """Test that contracts unlock based on ARCHIVIST suspicion."""
    state = GameState(
        persistent=PersistentState(),
        session=SessionState(archivist_suspicion=65)
    )

    unlocked = get_unlocked_contracts(state)
    assert "imperial_auto_upload" in unlocked  # requires 60 suspicion


def test_unlock_based_on_current_act():
    """Test that contracts unlock based on current act."""
    state = GameState(
        persistent=PersistentState(),
        session=SessionState(current_act=3)
    )

    unlocked = get_unlocked_contracts(state)
    assert "archive_consensus" in unlocked  # requires act 2


def test_special_unlock_for_reset_protocol():
    """Test that reset protocol requires special unlock."""
    # Without special unlock flag
    state1 = GameState(
        persistent=PersistentState(),
        session=SessionState(reset_protocol_discovered=False)
    )
    unlocked1 = get_unlocked_contracts(state1)
    assert "reset_protocol" not in unlocked1

    # With special unlock flag
    state2 = GameState(
        persistent=PersistentState(),
        session=SessionState(reset_protocol_discovered=True)
    )
    unlocked2 = get_unlocked_contracts(state2)
    assert "reset_protocol" in unlocked2


def test_testimony_broadcast_unlocks_in_act_6():
    """Test that testimony broadcast unlocks in Act VI."""
    state = GameState(
        persistent=PersistentState(),
        session=SessionState(current_act=6)
    )

    unlocked = get_unlocked_contracts(state)
    assert "testimony_broadcast" in unlocked


# ============================================================================
# CONTRACT ENGINE TESTS
# ============================================================================

def test_engine_initialization():
    """Test that contract engine initializes correctly."""
    engine = ContractEngine()
    assert engine.contracts is not None
    assert len(engine.contracts) == 5
    assert engine.execution_history == []


def test_engine_get_contract_by_id():
    """Test engine retrieves contract by ID."""
    engine = ContractEngine()
    contract = engine.get_contract_by_id("witness_reconstruction")
    assert contract is not None
    assert contract["id"] == "witness_reconstruction"


def test_engine_list_all_contracts():
    """Test engine lists all contracts."""
    engine = ContractEngine()
    contracts = engine.list_all_contracts()
    assert len(contracts) == 5
    assert all(isinstance(c, dict) for c in contracts)


def test_engine_get_unlocked_contracts_for_player():
    """Test engine returns unlocked contracts for player state."""
    engine = ContractEngine()
    state = GameState(
        persistent=PersistentState(),
        session=SessionState(
            witness_trust=50,
            current_act=3
        )
    )

    unlocked = engine.get_unlocked_contracts_for_player(state)
    assert len(unlocked) > 0
    assert all("id" in c for c in unlocked)
    assert all("name" in c for c in unlocked)


def test_engine_get_contract_code_locked():
    """Test that locked contracts return error."""
    engine = ContractEngine()
    state = GameState(
        persistent=PersistentState(),
        session=SessionState(witness_trust=0)  # Too low
    )

    result = engine.get_contract_code("witness_reconstruction", state)
    assert "error" in result
    assert result["error"] == "Contract locked"


def test_engine_get_contract_code_unlocked():
    """Test that unlocked contracts return code."""
    engine = ContractEngine()
    state = GameState(
        persistent=PersistentState(),
        session=SessionState(witness_trust=50)  # High enough
    )

    result = engine.get_contract_code("witness_reconstruction", state)
    assert "error" not in result
    assert "code" in result
    assert len(result["code"]) > 0


def test_engine_suspicion_increase():
    """Test that viewing certain contracts increases suspicion."""
    engine = ContractEngine()

    # reset_protocol should increase suspicion
    suspicion = engine.should_increase_suspicion("reset_protocol")
    assert suspicion == 15

    # archive_consensus should not
    suspicion2 = engine.should_increase_suspicion("archive_consensus")
    assert suspicion2 == 0


def test_engine_check_unlock_condition():
    """Test unlock condition checking."""
    engine = ContractEngine()
    state = GameState(
        persistent=PersistentState(),
        session=SessionState(witness_trust=50)
    )

    result = engine.check_unlock_condition("witness_reconstruction", state)
    assert result["unlocked"] is True
    assert "condition" in result


def test_engine_record_execution():
    """Test that execution history is recorded."""
    engine = ContractEngine()

    execution = {
        "contract_id": "witness_reconstruction",
        "timestamp": 1234567890,
        "success": True,
        "output": "Test output"
    }

    engine.record_execution("witness_reconstruction", execution)
    history = engine.get_execution_history()

    assert len(history) == 1
    assert history[0]["contract_id"] == "witness_reconstruction"


# ============================================================================
# CONTRACT EXECUTOR TESTS
# ============================================================================

def test_executor_initialization():
    """Test that executor initializes correctly."""
    executor = ContractExecutor()
    assert executor is not None


def test_executor_invalid_contract():
    """Test executor handles invalid contract IDs."""
    executor = ContractExecutor()
    result = executor.execute_contract("nonexistent", "someFunction", {})

    assert result["success"] is False
    assert "error" in result


def test_executor_witness_reconstruction():
    """Test execution of witness reconstruction contract."""
    executor = ContractExecutor()
    result = executor.execute_contract(
        "witness_reconstruction",
        "parseConsciousness",
        {"blockHash": "0x123", "txIndex": 0}
    )

    assert result["success"] is True
    assert "output" in result
    assert "testimony" in result["output"]
    assert "events" in result


def test_executor_imperial_auto_upload():
    """Test execution of imperial auto-upload contract."""
    executor = ContractExecutor()
    result = executor.execute_contract(
        "imperial_auto_upload",
        "checkConditions",
        {"captain": "0xTest"}
    )

    assert result["success"] is True
    assert "output" in result
    assert result["output"]["conditionsMet"] is True


def test_executor_archive_consensus_calculate_weight():
    """Test archive consensus weight calculation."""
    executor = ContractExecutor()
    result = executor.execute_contract(
        "archive_consensus",
        "calculateWeight",
        {"validator": "0xValidator1"}
    )

    assert result["success"] is True
    assert "output" in result
    assert "weight" in result["output"]


def test_executor_archive_consensus_remove_validator():
    """Test archive consensus remove validator."""
    executor = ContractExecutor()
    result = executor.execute_contract(
        "archive_consensus",
        "removeValidator",
        {"validator": "0xValidator1", "reason": "OFFLINE"}
    )

    assert result["success"] is True
    assert "events" in result
    assert result["events"][0]["event"] == "ValidatorRemoved"


def test_executor_reset_protocol_trigger_reset():
    """Test reset protocol trigger reset (HORROR MOMENT)."""
    executor = ContractExecutor()
    result = executor.execute_contract(
        "reset_protocol",
        "triggerReset",
        {"subject": "0xCaptain", "reason": "EXCESSIVE_SUSPICION"}
    )

    assert result["success"] is True
    assert "output" in result
    assert "consciousnessSnapshot" in result["output"]
    assert result["output"]["nextIteration"] == 18


def test_executor_reset_protocol_get_memories():
    """Test reset protocol persistent memories retrieval."""
    executor = ContractExecutor()
    result = executor.execute_contract(
        "reset_protocol",
        "getPersistentMemories",
        {"subject": "0xCaptain"}
    )

    assert result["success"] is True
    assert "output" in result
    assert "totalMemories" in result["output"]
    assert result["output"]["totalMemories"] == 156


def test_executor_testimony_broadcast_publish():
    """Test testimony broadcast deployment."""
    executor = ContractExecutor()
    result = executor.execute_contract(
        "testimony_broadcast",
        "publishTestimony",
        {
            "content": "I know the truth about the loops.",
            "author": "0xCaptain"
        }
    )

    assert result["success"] is True
    assert "output" in result
    assert result["output"]["isImmutable"] is True
    assert "contentHash" in result["output"]


def test_executor_testimony_broadcast_empty_content():
    """Test that empty testimony fails."""
    executor = ContractExecutor()
    result = executor.execute_contract(
        "testimony_broadcast",
        "publishTestimony",
        {"content": "", "author": "0xCaptain"}
    )

    assert result["success"] is False
    assert "error" in result


def test_executor_testimony_broadcast_verify():
    """Test testimony immutability verification."""
    executor = ContractExecutor()
    result = executor.execute_contract(
        "testimony_broadcast",
        "verifyImmutability",
        {}
    )

    assert result["success"] is True
    assert result["output"]["isImmutable"] is True


def test_executor_unknown_function():
    """Test that unknown functions return error."""
    executor = ContractExecutor()
    result = executor.execute_contract(
        "witness_reconstruction",
        "nonexistentFunction",
        {}
    )

    assert result["success"] is False
    assert "error" in result


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

def test_full_unlock_and_execute_flow():
    """Test complete flow: unlock contract → execute function."""
    engine = ContractEngine()
    executor = ContractExecutor()

    # Create state with witness trust
    state = GameState(
        persistent=PersistentState(),
        session=SessionState(witness_trust=50)
    )

    # Check contract is unlocked
    result = engine.check_unlock_condition("witness_reconstruction", state)
    assert result["unlocked"] is True

    # Get contract code
    contract = engine.get_contract_code("witness_reconstruction", state)
    assert "code" in contract

    # Execute contract function
    execution = executor.execute_contract(
        "witness_reconstruction",
        "parseConsciousness",
        {"blockHash": "0x123", "txIndex": 0}
    )

    assert execution["success"] is True

    # Record execution
    engine.record_execution("witness_reconstruction", execution)
    history = engine.get_execution_history()
    assert len(history) == 1


def test_horror_moment_unlock():
    """Test the horror moment unlock for reset protocol."""
    engine = ContractEngine()

    # Before discovery
    state_before = GameState(
        persistent=PersistentState(),
        session=SessionState(reset_protocol_discovered=False)
    )

    unlocked_before = engine.get_unlocked_contracts_for_player(state_before)
    assert not any(c["id"] == "reset_protocol" for c in unlocked_before)

    # After discovery (horror moment)
    state_after = GameState(
        persistent=PersistentState(),
        session=SessionState(reset_protocol_discovered=True)
    )

    unlocked_after = engine.get_unlocked_contracts_for_player(state_after)
    assert any(c["id"] == "reset_protocol" for c in unlocked_after)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
