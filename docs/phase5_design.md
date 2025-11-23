# Phase 5: Balance Tracking System Design

## Architecture Overview

### Design Decisions

1. **Account-based model** (not UTXO)
   - Simpler to understand for educational purposes
   - Each address has a single balance
   - Like Ethereum, not Bitcoin

2. **Ledger recalculation approach**
   - Balances calculated by replaying entire chain
   - No separate database needed
   - Always in sync with blockchain state

3. **Coinbase transactions**
   - Special transaction type: `is_coinbase=True`
   - Sender is always "COINBASE"
   - No signature required
   - Creates new coins (block reward)

---

## Data Structures

### Modified: Transaction
```python
@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float
    timestamp: str
    signature: str = ""
    is_coinbase: bool = False  # NEW

    def is_valid(self, ledger=None) -> bool:
        # Coinbase transactions have different rules
        if self.is_coinbase:
            return (
                self.sender == "COINBASE" and
                self.amount > 0 and
                self.recipient  # Must have recipient
            )

        # Regular transactions
        # ... existing validation ...

        # Optional: check balance if ledger provided
        if ledger:
            if not ledger.has_sufficient_funds(self.sender, self.amount):
                return False

        return True
```

### New: Ledger
```python
class Ledger:
    """
    Tracks account balances by replaying the blockchain.
    Simple account-based model.
    """

    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.balances = {}  # address -> balance

    def calculate_balances(self) -> dict:
        """
        Recalculate all balances from scratch.
        This is called after adding a block.
        """
        balances = {}

        # Iterate through all blocks
        for block in self.blockchain.chain:
            # Iterate through all transactions in block
            for tx_dict in block.transactions:
                tx = Transaction.from_dict(tx_dict)

                # Coinbase: only add to recipient
                if tx.is_coinbase:
                    balances[tx.recipient] = balances.get(tx.recipient, 0) + tx.amount

                # Regular transaction: subtract from sender, add to recipient
                else:
                    balances[tx.sender] = balances.get(tx.sender, 0) - tx.amount
                    balances[tx.recipient] = balances.get(tx.recipient, 0) + tx.amount

        self.balances = balances
        return balances

    def get_balance(self, address: str) -> float:
        """Get balance for an address."""
        if address not in self.balances:
            self.calculate_balances()
        return self.balances.get(address, 0.0)

    def has_sufficient_funds(self, address: str, amount: float) -> bool:
        """Check if address can spend amount."""
        return self.get_balance(address) >= amount
```

---

## Block Rewards

### Constants
```python
# backend/constants.py (NEW FILE)

BLOCK_REWARD = 50.0  # Coins per block
HALVING_INTERVAL = 210  # Optional: blocks between halvings

def get_block_reward(block_height: int) -> float:
    """Calculate block reward with optional halving."""
    halvings = block_height // HALVING_INTERVAL
    reward = BLOCK_REWARD / (2 ** halvings)
    return max(reward, 0.0001)  # Minimum reward
```

### Modified: Miner
```python
class Miner:
    def __init__(self, difficulty=4, block_reward=BLOCK_REWARD):
        self.difficulty = difficulty
        self.block_reward = block_reward

    def mine_block(self, previous_block, transactions, miner_address):
        """
        Mine a new block with coinbase transaction.

        Args:
            previous_block: Previous block in chain
            transactions: List of transaction dicts from mempool
            miner_address: Address to send block reward to

        Returns:
            Mined Block with coinbase as first transaction
        """
        # Create coinbase transaction
        coinbase = Transaction(
            sender="COINBASE",
            recipient=miner_address,
            amount=self.block_reward,
            timestamp=get_timestamp(),
            is_coinbase=True
        )

        # Add coinbase as first transaction
        all_transactions = [coinbase.to_dict()] + transactions

        # Mine block with all transactions
        # ... existing mining logic ...
```

---

## API Changes

### New Endpoints

```python
# GET /api/balance/{address}
{
    "address": "0x7f8a...",
    "balance": 150.5
}

# GET /api/balances
{
    "balances": {
        "0x7f8a...": 150.5,
        "0x4a2c...": 75.0,
        "DEFAULT_MINER": 250.0
    },
    "total_supply": 475.5
}
```

### Modified Endpoints

```python
# POST /api/mine
# Now accepts miner_address in body
{
    "miner_address": "0x7f8a..."  # Optional, defaults to "DEFAULT_MINER"
}

# Response includes coinbase info
{
    "status": "success",
    "block": { ... },
    "coinbase": {
        "recipient": "0x7f8a...",
        "reward": 50.0
    }
}

# POST /api/transaction
# Now validates balance before accepting
{
    "sender": "0x7f8a...",
    "recipient": "0x9b3d...",
    "amount": 10.0,
    ...
}

# Response includes balance info
{
    "status": "added",
    "tx_hash": "abc123...",
    "sender_balance_after": 140.5
}

# OR if insufficient funds:
{
    "status": "invalid",
    "error": "Insufficient funds",
    "available": 5.0,
    "required": 10.0
}
```

---

## UI Changes

### Crypto Vault

**Before:**
```
┌─────────────────────────────┐
│ CRYPTO VAULT                │
│ [Generate Keypair]          │
│ [Create Transaction]        │
└─────────────────────────────┘
```

**After:**
```
┌─────────────────────────────┐
│ CRYPTO VAULT                │
├─────────────────────────────┤
│ 💰 BALANCE: 150 CREDITS     │
├─────────────────────────────┤
│ [Generate Keypair]          │
│ [Create Transaction]        │
│   Amount: [___] (Max: 150)  │
│   ⚠️ Insufficient funds      │
└─────────────────────────────┘
```

### Chain Viewer

**Before:**
```
Block #5
├─ TX: 0x7f8a... → 0x9b3d... (10)
└─ TX: 0x4a2c... → 0x7f8a... (5)
```

**After:**
```
Block #5
├─ ⛏️ COINBASE → 0x7f8a... (50 CREDITS)
├─ TX: 0x7f8a... → 0x9b3d... (10 CREDITS)
└─ TX: 0x4a2c... → 0x7f8a... (5 CREDITS)
```

---

## State Management

### Modified: State
```python
from ledger import Ledger

class State:
    def __init__(self):
        self.blockchain = Blockchain()
        self.ledger = Ledger(self.blockchain)  # NEW
        self.mempool = []
        self.network = Network()

    def add_block(self, block):
        """Add block and update ledger."""
        if self.blockchain.add_block(block):
            # Recalculate balances after adding block
            self.ledger.calculate_balances()
            return True
        return False
```

---

## Transaction Flow

### Creating a Transaction (with balance check)

```
1. User enters recipient and amount
   ↓
2. Frontend checks local balance
   - If insufficient: show warning
   - If sufficient: continue
   ↓
3. Sign transaction
   ↓
4. POST /api/transaction
   ↓
5. Backend validates:
   - Signature valid?
   - Balance sufficient?
   ↓
6. If valid: add to mempool
   If invalid: return error with balance info
   ↓
7. Frontend shows result
```

### Mining a Block (with rewards)

```
1. User clicks "Mine Block"
   ↓
2. Provide miner_address (or use default)
   ↓
3. POST /api/mine with miner_address
   ↓
4. Backend:
   - Create coinbase transaction (COINBASE → miner_address)
   - Add pending transactions from mempool
   - Mine block (find valid nonce)
   - Add block to chain
   - Recalculate ledger balances
   ↓
5. Return block with coinbase info
   ↓
6. Frontend shows:
   - "Block mined!"
   - "You earned 50 CREDITS"
   - Updated balance
```

---

## Edge Cases

### 1. Empty Balance
- Address with 0 balance cannot send transactions
- Show clear error message
- Don't add to mempool

### 2. Exact Balance
- If balance = amount, transaction should succeed
- Balance becomes 0 after

### 3. Genesis State
- Genesis block has no transactions
- All balances start at 0
- First coins come from mining

### 4. Double Spend
- User tries to send more than they have
- Backend rejects during validation
- Mempool never contains invalid transactions

### 5. Coinbase Validation
- Only miners can create coinbase transactions
- API endpoint controls this (user can't submit coinbase)
- Coinbase must always be first transaction in block

---

## Testing Strategy

### Unit Tests

```python
# test_ledger.py
def test_empty_blockchain_has_zero_balances()
def test_coinbase_transaction_increases_balance()
def test_regular_transaction_moves_funds()
def test_insufficient_funds_rejected()
def test_balance_calculation_is_accurate()
def test_multiple_transactions_compound()

# test_transaction.py
def test_coinbase_transaction_is_valid()
def test_coinbase_needs_no_signature()
def test_regular_transaction_needs_balance()
def test_zero_balance_prevents_transaction()

# test_mining.py
def test_mined_block_has_coinbase()
def test_coinbase_is_first_transaction()
def test_miner_receives_reward()
def test_block_reward_amount_correct()
```

### Integration Tests

```python
# test_integration.py
def test_full_transaction_flow():
    """
    1. Mine block (miner gets 50 coins)
    2. Miner sends 10 coins to Alice
    3. Mine another block (miner gets 100 total)
    4. Alice sends 5 coins to Bob
    5. Verify all balances are correct
    """
```

---

## Implementation Order

1. **Create constants.py** - Define BLOCK_REWARD
2. **Modify transaction.py** - Add is_coinbase field
3. **Create ledger.py** - Implement balance tracking
4. **Modify state.py** - Add ledger instance
5. **Modify mining.py** - Add coinbase transactions
6. **Modify blockchain.py** - Integrate ledger updates
7. **Modify main.py** - Add balance endpoints, update mine endpoint
8. **Test backend** - Run all tests
9. **Modify crypto-vault.js** - Add balance display and validation
10. **Modify chain-viewer.js** - Show coinbase transactions, accept miner address
11. **Test frontend** - Manual testing
12. **Update tutorial** - Add economic concepts to Learning Guide

---

## Success Metrics

✅ All balances sum to (blocks_mined * BLOCK_REWARD)
✅ Cannot create transaction with insufficient funds
✅ Mining creates coinbase transaction
✅ Balances display correctly in UI
✅ Tests pass
✅ Code follows project philosophy (simple, flat, clear)

---

**Ready to implement!**
