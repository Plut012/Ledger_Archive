# Phase 2 Context: Crypto Vault Module

## Quick Orientation

**Your Task:** Build the Crypto Vault UI module - an interactive wallet interface

**Expected Duration:** 2-3 work sessions

**Phase Status:** 🔄 READY TO START

---

## What You Inherit from Phase 1

### ✅ Working Backend Crypto

**Available in backend/crypto.py:**
```python
class Wallet:
    generate_keypair()     # Creates public/private keys
    sign(message)          # Signs a message
    verify(msg, sig, pk)   # Verifies signature
```

**API Endpoints:**
- `POST /api/wallet/generate` → `{public_key, private_key, address}`
- `POST /api/transaction` → Validates signatures, adds to mempool
- `GET /api/chain` → Full blockchain
- `GET /api/state` → Current state (height, pending tx, etc.)

**Tests:**
- All crypto tests passing
- Transaction signing working
- Signature validation working

### ✅ Working Frontend

**Already functional:**
- Terminal UI framework
- Chain Viewer module (fully working)
- WebSocket connection to backend
- Navigation system
- Console I/O

**Placeholder waiting for you:**
- `frontend/js/modules/crypto-vault.js` (stub)

---

## Your Goal: Build Crypto Vault UI

### What You're Building

An interactive terminal module where users can:

```
┌──────────────────────────────────────────────┐
│ CRYPTOGRAPHIC VAULT                          │
├──────────────────────────────────────────────┤
│ [KEY MANAGEMENT]                             │
│                                              │
│ Public Key:  04a1b2c3d4e5f6...              │
│ Address:     0x742d35Cc663...               │
│                                              │
│ [Generate New Keypair] [Export Keys]        │
│                                              │
├──────────────────────────────────────────────┤
│ [TRANSACTION BUILDER]                        │
│                                              │
│ From:     0x742d... (your address)          │
│ To:       [input field]                     │
│ Amount:   [input field] ARC                 │
│                                              │
│ [Sign & Broadcast]                          │
│                                              │
├──────────────────────────────────────────────┤
│ [TRANSACTION HISTORY]                        │
│ #1  0x891f...  →  1.5 ARC  ◉ CONFIRMED     │
│ #2  0x4f2a...  →  0.3 ARC  ◐ PENDING       │
└──────────────────────────────────────────────┘
```

---

## Implementation Plan

### Step 1: Wallet Display & Generation

**File:** `frontend/js/modules/crypto-vault.js`

**Tasks:**
- [ ] Create module structure (init, render, cleanup)
- [ ] Add "Generate Keypair" button
- [ ] Call API: `POST /api/wallet/generate`
- [ ] Display public key, address
- [ ] Store private key in memory (warn user it's temporary)

**UI Elements:**
- Button: Generate New Keypair
- Display: Public key (truncated)
- Display: Full address
- Button: Export Keys (copy to clipboard)

---

### Step 2: Transaction Builder

**Tasks:**
- [ ] Create transaction form (to, amount)
- [ ] Auto-fill "from" with current wallet address
- [ ] Validate inputs (address format, amount > 0)
- [ ] Sign transaction with private key (call wallet.sign())
- [ ] POST signed transaction to API
- [ ] Show success/error feedback

**UI Elements:**
- Input: Recipient address
- Input: Amount
- Button: Sign & Broadcast
- Status: Success/error messages

---

### Step 3: Transaction History

**Tasks:**
- [ ] Fetch transactions from mempool
- [ ] Fetch transactions from mined blocks
- [ ] Filter by current wallet address
- [ ] Display with status (pending/confirmed)
- [ ] Auto-update when new block mined

**UI Elements:**
- List: Transaction hash, recipient, amount, status
- Status indicators: ◉ CONFIRMED, ◐ PENDING

---

### Step 4: Backend Support (if needed)

**New endpoint to add (optional):**

```python
# backend/main.py

@app.get("/api/transactions/{address}")
def get_transactions(address: str):
    """Get all transactions for an address."""
    # Return pending + confirmed transactions
    return {
        "pending": [...],
        "confirmed": [...]
    }
```

**Only add if needed for transaction history feature.**

---

## Files You'll Modify

```
frontend/js/modules/crypto-vault.js   ← Main work here
backend/main.py                       ← Optional: add transaction query endpoint
frontend/css/modules.css              ← Optional: vault-specific styles
```

**Estimated LOC:** 150-200 lines

---

## Success Criteria

### Phase 2 is complete when:

**Functionality:**
- [ ] User can click "Generate Keypair"
- [ ] Keys and address display correctly
- [ ] User can fill transaction form
- [ ] Transaction is signed automatically
- [ ] Signed transaction broadcasts to mempool
- [ ] Transaction appears in "pending" status
- [ ] After mining, status changes to "confirmed"

**Code Quality:**
- [ ] Code follows project philosophy (simple, clear)
- [ ] No unnecessary abstractions
- [ ] Functions are small and focused
- [ ] Comments explain "why" not "what"

**User Experience:**
- [ ] UI is intuitive (no tutorial needed)
- [ ] Feedback is immediate and clear
- [ ] Errors are helpful
- [ ] Wallet warning displayed (temporary, in-memory only)

---

## API Reference (from Phase 1)

### Generate Wallet

```bash
POST /api/wallet/generate

Response:
{
    "public_key": "04a1b2c3...",
    "private_key": "e8f7d6c5...",  # Keep secure!
    "address": "0x742d35Cc..."
}
```

### Submit Transaction

```bash
POST /api/transaction

Body:
{
    "sender": "0x742d...",
    "recipient": "0x891f...",
    "amount": 1.5,
    "timestamp": "2024-01-01 12:00:00",
    "signature": "a1b2c3d4..."
}

Response:
{
    "status": "added",
    "tx_hash": "4f2a8b..."
}
```

### Get Blockchain State

```bash
GET /api/state

Response:
{
    "height": 42,
    "pending_transactions": 3,
    "is_valid": true,
    "latest_block": {...}
}
```

---

## User Flow Example

```
1. User navigates to Crypto Vault module
   → Sees empty wallet section

2. User clicks "Generate Keypair"
   → API call to backend
   → Keys generated and returned
   → Public key and address displayed
   → Console logs: "Wallet generated: 0x742d..."

3. User fills transaction form:
   To: 0x891f...
   Amount: 1.5

4. User clicks "Sign & Broadcast"
   → Transaction signed with private key
   → POST to /api/transaction
   → Success message displayed
   → Console logs: "Transaction broadcast: tx_4f2a..."
   → Transaction appears in "Pending" list

5. User switches to Chain Viewer
   → Clicks "Mine Block"
   → Block mined with transaction

6. User returns to Crypto Vault
   → Transaction now shows ◉ CONFIRMED
```

---

## Code Template to Get Started

```javascript
// frontend/js/modules/crypto-vault.js

const CryptoVault = {
    currentWallet: null,  // {public_key, private_key, address}
    transactions: [],

    init(container) {
        this.render(container);
        this.setupEventListeners();
    },

    render(container) {
        container.innerHTML = `
            <div class="module-header">CRYPTOGRAPHIC VAULT</div>

            <div class="module-section">
                <div class="section-title">[KEY MANAGEMENT]</div>
                <div id="wallet-display">
                    <!-- Wallet info renders here -->
                </div>
                <button id="btn-generate-wallet">Generate New Keypair</button>
            </div>

            <div class="module-section">
                <div class="section-title">[TRANSACTION BUILDER]</div>
                <div id="tx-form">
                    <!-- Transaction form here -->
                </div>
            </div>

            <div class="module-section">
                <div class="section-title">[TRANSACTION HISTORY]</div>
                <div id="tx-history">
                    <!-- Transaction list here -->
                </div>
            </div>
        `;
    },

    setupEventListeners() {
        // TODO: Add event listeners
    },

    async generateWallet() {
        // TODO: Call API, store result, update UI
    },

    async signAndBroadcast() {
        // TODO: Create transaction, sign, send to API
    },

    cleanup() {
        // Clear sensitive data
        this.currentWallet = null;
    }
};
```

---

## Important Notes

### Security Warnings

**This is educational software:**
- Wallets are NOT encrypted
- Private keys stored in browser memory only
- Keys lost on page refresh
- Not suitable for real value

**User warnings to display:**
- "⚠️ Wallet exists in memory only - export to save"
- "⚠️ Never share your private key"
- "⚠️ This is educational software only"

### Transaction Signing

**Use the crypto from Phase 1:**
- Don't implement signing again
- Call the backend's sign method via API
- Or replicate the same algorithm in JS (keep consistent)

**Recommendation:** Call backend for signing (less duplication)

---

## Testing Your Work

### Manual Testing Checklist

- [ ] Click "Generate Keypair" → Keys appear
- [ ] Click again → Different keys generated
- [ ] Fill transaction form → No errors
- [ ] Submit with invalid address → Error shown
- [ ] Submit with negative amount → Error shown
- [ ] Submit valid transaction → Appears in pending
- [ ] Mine a block → Transaction moves to confirmed
- [ ] Refresh page → Wallet cleared (as expected)

### Integration Testing

```bash
# Backend must be running
uv run python backend/main.py

# Frontend must be served
cd frontend && python -m http.server 8080

# Open browser to: http://localhost:8080
# Navigate to Crypto Vault
# Follow user flow above
```

---

## Common Pitfalls to Avoid

❌ **Don't** implement your own crypto (use Phase 1's work)
❌ **Don't** persist wallets to localStorage (security issue for learning tool)
❌ **Don't** add complex key derivation (keep simple)
❌ **Don't** over-engineer the UI (terminal aesthetic)

✅ **Do** reuse existing terminal UI patterns
✅ **Do** show clear user feedback
✅ **Do** warn about temporary wallet storage
✅ **Do** keep code simple and readable

---

## Phase 2 Completion Checklist

*Fill this out when done - see docs/phase2_handoff.md*

---

## Need Help?

**Read these first:**
- `docs/phase2_plan.md` - Full detailed plan
- `docs/phase1_handoff.md` - What Phase 1 delivered
- `docs/ui_plan.md` - UI design specification
- `docs/claude.md` - Code philosophy

**Check these files:**
- `frontend/js/modules/chain-viewer.js` - Example module structure
- `backend/crypto.py` - Crypto implementation from Phase 1
- `backend/main.py` - API endpoints available

---

**Ready to build!** Start with `frontend/js/modules/crypto-vault.js`

*Good luck, Archive Captain.* 🚀
