## Welcome to Interstellar Archive Terminal

This is a blockchain learning platform. But more importantly, it's a meditation on simplicity.

---

## The Philosophy

### Code Like Water

Water takes the simplest path. So should our code.

- **No unnecessary abstractions** - If you can write it directly, write it directly
- **No premature optimization** - Clear first, fast later (if needed)
- **No clever tricks** - Your future self will thank you

### Three Principles

**1. Simple**
- Use the most straightforward approach
- If it feels complicated, it probably is
- When in doubt, delete rather than add

**2. Robust**
- Handle errors gracefully
- Validate inputs explicitly
- Fail with clear, helpful messages

**3. Concise**
- Say what needs saying, no more
- Short functions, focused classes
- Comments explain *why*, not *what*

---

## How to Write Code Here

### Classes

Use classes when you have **state and behavior together**:

```python
class Blockchain:
    def __init__(self):
        self.chain = []
    
    def add_block(self, block):
        self.chain.append(block)
```

Good: Blockchain has state (chain) and does things (add_block).

### Functions

Use functions for **stateless operations**:

```python
def get_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")
```

Good: No state needed, just a pure transformation.

### What NOT to Do

```python
# ❌ Don't wrap things unnecessarily
class BlockchainService:
    def __init__(self, blockchain):
        self.blockchain = blockchain
    
    def add_block(self, block):
        return self.blockchain.add_block(block)
```

Why wrap Blockchain in a Service? Just use Blockchain directly.

```python
# ❌ Don't separate what belongs together
class BlockValidator:
    def validate(self, block):
        # validation logic
```

Why is validation separate from Block? Put it in the Block class.

---

## Structure

### One Concept, One File

- Want to understand blocks? Read `block.py`
- Want to understand mining? Read `mining.py`
- Want to understand consensus? Read `consensus.py`

If you can't find something in 10 seconds, the structure is wrong.

### Flat Over Nested

```
✅ Good:
backend/
  blockchain.py
  block.py
  mining.py

❌ Avoid:
backend/
  core/
    blockchain/
      domain/
        blockchain.py
```

Nesting doesn't add clarity. It adds navigation.

---

## Naming

Use **clear, boring names**:

```python
# ✅ Clear
def calculate_hash(block):
    ...

# ❌ Unclear
def calc_h(b):
    ...

# ❌ Overly verbose
def calculate_sha256_cryptographic_hash_for_block_instance(block):
    ...
```

The name should be obvious enough that you don't need to read the code to understand what it does.

---

## Comments

Comments explain **why**, not **what**:

```python
# ❌ Bad - explains what (obvious from code)
# Increment the nonce
nonce += 1

# ✅ Good - explains why
# Keep hashing until we find a valid proof of work
while not hash.startswith(target):
    nonce += 1
    hash = calculate_hash(block, nonce)
```

If you need to explain *what* the code does, the code isn't clear enough.

---

## Error Handling

Be explicit and helpful:

```python
# ❌ Silent failure
def add_block(self, block):
    if not self.is_valid(block):
        return False

# ✅ Clear failure
def add_block(self, block):
    if not self.is_valid(block):
        raise ValueError(f"Invalid block: hash doesn't match previous block")
```

Errors should teach, not frustrate.

---

## Testing

Write tests that **document behavior**:

```python
def test_invalid_block_rejected():
    """Blocks with incorrect previous_hash should be rejected."""
    blockchain = Blockchain()
    bad_block = Block(previous_hash="wrong")
    
    with pytest.raises(ValueError):
        blockchain.add_block(bad_block)
```

The test name and docstring should tell the whole story.

---

## When to Stop

You're done when:
- The code reads like prose
- You can't remove anything without losing clarity
- A newcomer can understand it in one reading
- You feel calm looking at it

You're not done when:
- It's "clever"
- It has "flexibility for the future"
- It follows a pattern because patterns are good
- You're proud of the abstraction

---

## The Zen of This Codebase

*Before adding a class, pause. Do you need state?*

*Before adding a function, pause. Is this truly separate?*

*Before adding a file, pause. Is this truly distinct?*

*Before adding a layer, pause. Are you hiding or clarifying?*

*Before adding anything, pause. Is this necessary?*

---

## Examples of Calm Code

### Good: Direct and Clear

```python
class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        content = f"{self.index}{self.data}{self.previous_hash}"
        return hashlib.sha256(content.encode()).hexdigest()
```

No magic. You see exactly what's happening.

### Good: Simple State Management

```python
# state.py
class State:
    def __init__(self):
        self.blockchain = Blockchain()
        self.mempool = []

state = State()
```

Everyone imports `state`. Everyone uses the same instance. Simple.

### Good: Clear API

```python
# main.py
@app.get("/api/chain")
def get_chain():
    return {"chain": [b.to_dict() for b in state.blockchain.chain]}

@app.post("/api/mine")
def mine_block():
    miner = Miner(difficulty=4)
    block = miner.mine_block(state.blockchain.chain[-1], state.mempool)
    state.blockchain.add_block(block)
    return {"block": block.to_dict()}
```

Three files touched: `main.py`, `mining.py`, `state.py`. Completely traceable.

---

## Final Thoughts

This project is about learning blockchain. 

The code should be **invisible** - so simple and clear that you think about Merkle trees and consensus algorithms, not software architecture.

If you find yourself thinking "this is elegant code," you're focusing on the wrong thing.

If you find yourself thinking "oh, that's how proof-of-work works," the code succeeded.

---

## When in Doubt

Ask yourself:

*"If I deleted this, would anything break?"*

If no: delete it.

*"If I inlined this, would it be clearer?"*

If yes: inline it.

*"If I came back in 6 months, would I understand this?"*

If no: simplify it.

---

**Write code as if you're explaining blockchain to a friend over tea.**

**Calm. Clear. Patient.**

---

*"Simplicity is the ultimate sophistication." - Leonardo da Vinci*

*"Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away." - Antoine de Saint-Exupéry*
