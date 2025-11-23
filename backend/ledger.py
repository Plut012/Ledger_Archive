"""Ledger for tracking account balances."""

from typing import Dict
from transaction import Transaction


class Ledger:
    """
    Tracks account balances by replaying the blockchain.
    Uses a simple account-based model (like Ethereum, not Bitcoin's UTXO).
    """

    def __init__(self, blockchain):
        """
        Initialize ledger with a blockchain.

        Args:
            blockchain: Blockchain instance to track balances for
        """
        self.blockchain = blockchain
        self.balances: Dict[str, float] = {}

    def calculate_balances(self) -> Dict[str, float]:
        """
        Recalculate all balances from scratch by replaying the entire chain.
        This is called after adding a new block to ensure balances are current.

        Returns:
            Dictionary mapping addresses to balances
        """
        balances = {}

        # Iterate through all blocks in the chain
        for block in self.blockchain.chain:
            # Iterate through all transactions in the block
            for tx_dict in block.transactions:
                tx = Transaction.from_dict(tx_dict)

                # Coinbase transactions only add to recipient
                if tx.is_coinbase:
                    balances[tx.recipient] = balances.get(tx.recipient, 0.0) + tx.amount

                # Regular transactions: subtract from sender, add to recipient
                else:
                    # Subtract from sender
                    balances[tx.sender] = balances.get(tx.sender, 0.0) - tx.amount

                    # Add to recipient
                    balances[tx.recipient] = balances.get(tx.recipient, 0.0) + tx.amount

        self.balances = balances
        return balances

    def get_balance(self, address: str) -> float:
        """
        Get the current balance for an address.

        Args:
            address: Address to get balance for

        Returns:
            Balance in credits (0.0 if address has never transacted)
        """
        # Ensure balances are up to date
        if not self.balances:
            self.calculate_balances()

        return self.balances.get(address, 0.0)

    def has_sufficient_funds(self, address: str, amount: float) -> bool:
        """
        Check if an address has sufficient funds for a transaction.

        Args:
            address: Address to check
            amount: Amount to check

        Returns:
            True if address has >= amount, False otherwise
        """
        return self.get_balance(address) >= amount

    def get_all_balances(self) -> Dict[str, float]:
        """
        Get all non-zero balances.

        Returns:
            Dictionary of address -> balance for all addresses with non-zero balance
        """
        if not self.balances:
            self.calculate_balances()

        # Return only non-zero balances for cleaner UI
        return {addr: balance for addr, balance in self.balances.items() if balance > 0}

    def get_total_supply(self) -> float:
        """
        Calculate total supply of coins in circulation.
        Should equal: number_of_blocks_mined * block_reward

        Returns:
            Total supply of credits
        """
        if not self.balances:
            self.calculate_balances()

        return sum(self.balances.values())
