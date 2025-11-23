# Phase 5: Balance Tracking & Economic Incentives

## Overview

**Goal:** Complete the economic foundation of the blockchain by implementing balance tracking, transaction validation with funds, and mining incentives.

**Why:** Right now transactions are accepted even if the sender has no funds, and miners receive no reward for their work. This phase makes the blockchain economically complete and teaches key concepts about cryptocurrency economics.

---

## What This Phase Adds

### 1. **Account Balance Tracking**
- Track balance for each address
- Simple account-based model (like Ethereum)
- Calculate balances from transaction history
- Expose balances via API

### 2. **Transaction Validation with Balances**
- Reject transactions if sender has insufficient funds
- Prevent double-spending
- Clear error messages for invalid transactions

### 3. **Block Rewards & Coinbase Transactions**
- Special "coinbase" transaction for mining rewards
- Miners receive newly minted coins
- Block reward amount (e.g., 50 coins per block)
- Optional: halving schedule for educational purposes

### 4. **UI Enhancements**
- Display account balance in Crypto Vault
- Show block rewards in Chain Viewer
- Display coinbase transactions differently
- Balance warnings when creating transactions

---

## Implementation Plan

### Backend Changes

#### 1. **New File: `backend/ledger.py`**
```python
class Ledger:
    """
    Tracks account balances from blockchain state.
    Simple account-based model (not UTXO).
    """

    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.balances = {}

    def calculate_balances(self):
        """Recalculate all balances from scratch by replaying chain."""
        pass

    def get_balance(self, address):
        """Get current balance for an address."""
        pass

    def has_sufficient_funds(self, address, amount):
        """Check if address can spend amount."""
        pass
```

#### 2. **Modify: `backend/transaction.py`**
- Add `is_coinbase` flag
- Special validation for coinbase transactions
- Update `is_valid()` to check balances (optional parameter)

```python
class Transaction:
    def __init__(self, sender, recipient, amount, timestamp=None, is_coinbase=False):
        self.is_coinbase = is_coinbase
        # ...

    def is_valid(self, ledger=None):
        """
        Validate transaction.
        If ledger provided, also check sender has sufficient funds.
        """
        # Coinbase transactions don't need signatures
        if self.is_coinbase:
            return self.sender == "COINBASE" and self.amount > 0

        # Regular transaction validation
        # Check signature, check balance if ledger provided
        pass
```

#### 3. **Modify: `backend/blockchain.py`**
- Add ledger instance
- Update `add_block()` to validate transactions have sufficient funds
- Recalculate balances after adding block

#### 4. **Modify: `backend/mining.py`**
- Create coinbase transaction automatically
- Add it as first transaction in block
- Configurable block reward

```python
class Miner:
    def __init__(self, difficulty=4, block_reward=50):
        self.block_reward = block_reward
        # ...

    def mine_block(self, previous_block, transactions, miner_address):
        """
        Mine a new block with coinbase transaction.
        miner_address: where to send the block reward
        """
        # Create coinbase transaction
        coinbase = Transaction(
            sender="COINBASE",
            recipient=miner_address,
            amount=self.block_reward,
            is_coinbase=True
        )

        # Add coinbase as first transaction
        all_transactions = [coinbase] + transactions
        # ... continue mining
```

#### 5. **New API Endpoints in `backend/main.py`**
```python
@app.get("/api/balance/{address}")
def get_balance(address: str):
    """Get balance for an address."""
    balance = state.ledger.get_balance(address)
    return {"address": address, "balance": balance}

@app.get("/api/balances")
def get_all_balances():
    """Get all non-zero balances."""
    return {"balances": state.ledger.balances}

# Update POST /api/mine to accept miner_address
@app.post("/api/mine")
def mine_new_block(miner_address: str = "DEFAULT_MINER"):
    """Mine with coinbase reward going to miner_address."""
    # ...
```

#### 6. **Modify: `backend/state.py`**
```python
from ledger import Ledger

class State:
    def __init__(self):
        self.blockchain = Blockchain()
        self.ledger = Ledger(self.blockchain)
        # ...
```

---

### Frontend Changes

#### 1. **Modify: `frontend/js/modules/crypto-vault.js`**
- Add balance display at top of module
- Fetch and display current wallet balance
- Show warning if trying to send more than balance
- Auto-refresh balance after transactions

```javascript
async loadBalance() {
    if (!this.currentWallet) return;

    const response = await fetch(`/api/balance/${this.currentWallet.address}`);
    const data = await response.json();

    // Display balance prominently
    document.getElementById('wallet-balance').textContent =
        `${data.balance} CREDITS`;
}
```

#### 2. **Modify: `frontend/js/modules/chain-viewer.js`**
- Show coinbase transactions differently (special styling)
- Display block reward amount
- Accept miner address when mining

```javascript
async mineBlock() {
    // Get miner address from input or use default
    const minerAddress = document.getElementById('miner-address').value
                         || 'DEFAULT_MINER';

    const response = await fetch('/api/mine', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ miner_address: minerAddress })
    });
    // ...
}
```

#### 3. **Optional: New module `frontend/js/modules/ledger-explorer.js`**
- View all addresses and balances
- Rich list (top balances)
- Address search
- Transaction history for address

---

### Testing

#### New File: `tests/test_ledger.py`
```python
def test_genesis_state():
    """Ledger should start empty."""

def test_coinbase_transaction():
    """Mining a block should create coinbase transaction."""

def test_balance_tracking():
    """Balances should update after transactions."""

def test_insufficient_funds():
    """Transaction should fail if sender lacks funds."""

def test_double_spend_prevention():
    """Cannot spend more than you have."""
```

---

## Economic Constants

```python
# In backend/constants.py (new file)

# Block reward
BLOCK_REWARD = 50  # Initial reward

# Optional: Halving schedule (like Bitcoin)
HALVING_INTERVAL = 210  # Blocks between halvings (much smaller for demo)

def get_block_reward(block_height):
    """Calculate block reward based on height."""
    halvings = block_height // HALVING_INTERVAL
    return BLOCK_REWARD // (2 ** halvings)
```

---

## UI/UX Improvements

### Crypto Vault Enhancements
```
┌─────────────────────────────────────────┐
│ CRYPTO VAULT                            │
├─────────────────────────────────────────┤
│ 💰 Balance: 150 CREDITS                 │
│                                         │
│ [Your Wallet]                           │
│ Address: 0x7f8a...                      │
│ Public Key: ...                         │
│                                         │
│ [Create Transaction]                    │
│ Recipient: [____________]               │
│ Amount: [____] (Max: 150)               │
│ [Send] ⚠️ Fee: 0.1                      │
└─────────────────────────────────────────┘
```

### Chain Viewer Enhancements
```
Block #5
├─ Coinbase Transaction ⛏️
│  COINBASE → 0x4a2c... (50 CREDITS)
├─ Transaction
│  0x7f8a... → 0x9b3d... (10 CREDITS)
└─ Transaction
   0x4a2c... → 0x7f8a... (5 CREDITS)
```

---

## Implementation Steps

### Step 1: Backend Foundation (30 min)
- [ ] Create `backend/ledger.py`
- [ ] Add ledger to state
- [ ] Implement balance calculation
- [ ] Add balance API endpoints

### Step 2: Coinbase Transactions (20 min)
- [ ] Modify `Transaction` class for coinbase
- [ ] Update `Miner` to create coinbase transactions
- [ ] Test mining with rewards

### Step 3: Transaction Validation (20 min)
- [ ] Update `Transaction.is_valid()` with balance check
- [ ] Prevent insufficient funds transactions
- [ ] Add error messages

### Step 4: Frontend - Crypto Vault (30 min)
- [ ] Add balance display
- [ ] Fetch balance from API
- [ ] Show warnings for insufficient funds
- [ ] Auto-refresh after transactions

### Step 5: Frontend - Chain Viewer (20 min)
- [ ] Display coinbase transactions differently
- [ ] Show block rewards
- [ ] Add miner address input

### Step 6: Testing (30 min)
- [ ] Write ledger tests
- [ ] Test coinbase transactions
- [ ] Test balance validation
- [ ] Test edge cases (empty balances, double spend)

### Step 7: Documentation (15 min)
- [ ] Update START_HERE.md
- [ ] Create phase5_handoff.md
- [ ] Add economic concepts to LEARNING_GUIDE.md

---

## Key Educational Concepts

This phase teaches:

1. **Account Model** - How balances are tracked (vs UTXO)
2. **Monetary Policy** - How new currency is created
3. **Mining Incentives** - Why miners secure the network
4. **Scarcity** - Limited supply through block rewards
5. **Economic Security** - Can't spend what you don't have
6. **Coinbase Transactions** - Special first transaction in block

---

## Optional Future Enhancements

After Phase 5, could add:
- Transaction fees (paid to miners)
- Gas prices for dynamic fees
- Mempool fee market
- Halving schedule visualization
- Supply curve chart
- Inflation rate calculator

---

## Success Criteria

Phase 5 is complete when:

✅ Balances are tracked for all addresses
✅ Transactions validate sender has funds
✅ Mining creates coinbase transactions
✅ Miners receive block rewards
✅ Crypto Vault displays current balance
✅ Chain Viewer shows coinbase transactions
✅ Tests pass for all new functionality
✅ Tutorial updated with economic concepts

---

## Estimated Time

- **Backend:** ~1.5 hours
- **Frontend:** ~1 hour
- **Testing:** ~30 min
- **Documentation:** ~30 min
- **Total:** ~3.5 hours

---

## Notes

- Keep it simple: account-based model (not UTXO)
- Don't over-engineer: single reward amount is fine
- Focus on education: make concepts visible in UI
- Maintain code philosophy: flat, clear, direct

---

**Next:** See `docs/phase5_handoff.md` after completion.
