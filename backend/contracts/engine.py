"""Contract engine for managing and retrieving smart contracts."""

from typing import Dict, List, Optional
from .templates import CONTRACT_TEMPLATES, get_contract, list_contracts, get_unlocked_contracts


class ContractEngine:
    """
    Manages smart contract storage, retrieval, and access control.

    Simple controller pattern - stores contracts and checks unlock conditions.
    """

    def __init__(self):
        """Initialize contract engine."""
        self.contracts = CONTRACT_TEMPLATES
        self.execution_history = []

    def get_contract_by_id(self, contract_id: str) -> Optional[Dict]:
        """
        Retrieve contract by ID.

        Args:
            contract_id: Contract identifier

        Returns:
            Contract dict or None if not found
        """
        return get_contract(contract_id)

    def list_all_contracts(self) -> List[Dict]:
        """
        List all available contracts (metadata only, no code).

        Returns:
            List of contract metadata dicts
        """
        return list_contracts()

    def get_unlocked_contracts_for_player(self, game_state) -> List[Dict]:
        """
        Get contracts unlocked for player based on game state.

        Args:
            game_state: Current game state object

        Returns:
            List of unlocked contract metadata dicts
        """
        unlocked_ids = get_unlocked_contracts(game_state)

        return [
            {
                "id": contract_id,
                "name": self.contracts[contract_id]["name"],
                "version": self.contracts[contract_id]["version"],
                "author": self.contracts[contract_id]["author"],
                "description": self.contracts[contract_id]["description"],
                "discovered_act": self.contracts[contract_id].get("discovered_act", 1)
            }
            for contract_id in unlocked_ids
        ]

    def get_contract_code(self, contract_id: str, game_state) -> Optional[Dict]:
        """
        Get full contract code if unlocked.

        Args:
            contract_id: Contract identifier
            game_state: Current game state

        Returns:
            Contract dict with code, or error dict
        """
        # Check if contract exists
        contract = self.get_contract_by_id(contract_id)
        if not contract:
            return {"error": "Contract not found"}

        # Check if unlocked
        unlocked_ids = get_unlocked_contracts(game_state)
        if contract_id not in unlocked_ids:
            return {
                "error": "Contract locked",
                "unlock_condition": contract["unlock_condition"]
            }

        # Return full contract
        return {
            "id": contract["id"],
            "name": contract["name"],
            "version": contract["version"],
            "author": contract["author"],
            "description": contract["description"],
            "code": contract["code"],
            "execution_notes": contract.get("execution_notes", "")
        }

    def check_unlock_condition(self, contract_id: str, game_state) -> Dict:
        """
        Check if contract unlock condition is met.

        Args:
            contract_id: Contract identifier
            game_state: Current game state

        Returns:
            Dict with unlocked status and reason
        """
        contract = self.get_contract_by_id(contract_id)
        if not contract:
            return {"unlocked": False, "reason": "Contract not found"}

        unlocked_ids = get_unlocked_contracts(game_state)

        if contract_id in unlocked_ids:
            return {
                "unlocked": True,
                "reason": "Condition met",
                "condition": contract["unlock_condition"]
            }
        else:
            return {
                "unlocked": False,
                "reason": "Condition not met",
                "condition": contract["unlock_condition"]
            }

    def record_execution(self, contract_id: str, execution_result: Dict):
        """
        Record contract execution to history.

        Args:
            contract_id: Contract that was executed
            execution_result: Result of execution
        """
        self.execution_history.append({
            "contract_id": contract_id,
            "timestamp": execution_result.get("timestamp"),
            "success": execution_result.get("success", False),
            "output": execution_result.get("output", "")
        })

    def get_execution_history(self, limit: int = 20) -> List[Dict]:
        """
        Get recent execution history.

        Args:
            limit: Maximum number of records to return

        Returns:
            List of execution records
        """
        return self.execution_history[-limit:]

    def should_increase_suspicion(self, contract_id: str) -> int:
        """
        Check if viewing this contract should increase ARCHIVIST suspicion.

        Args:
            contract_id: Contract being viewed

        Returns:
            Suspicion points to add (0 if none)
        """
        contract = self.get_contract_by_id(contract_id)
        if not contract:
            return 0

        return contract.get("suspicion_on_view", 0)
