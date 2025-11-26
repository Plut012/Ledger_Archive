# Development Principles for Chain of Truth

## Core Philosophy

When implementing these integration plans, prioritize **simplicity, robustness, and clarity** above all else. This is a narrative-driven game with educational goals—the code should be as understandable as the blockchain concepts we're teaching.

---

## 1. Simple and Robust Code

### Write Controllers, Not Clever Code

**DO:**
```python
class CharacterController:
    """Clear, single-responsibility controller"""

    def __init__(self, character, llm_provider, game_state):
        self.character = character
        self.llm = llm_provider
        self.game_state = game_state

    def handle_message(self, user_message: str) -> dict:
        """Simple execution path: validate → process → respond"""

        # Step 1: Validate input
        if not user_message or not user_message.strip():
            return {"error": "Empty message"}

        # Step 2: Build context
        context = self._build_context()

        # Step 3: Get response from character
        response = self.character.respond(user_message, context)

        # Step 4: Update game state
        self._update_state(response.state_changes)

        # Step 5: Return result
        return {
            "response": response.text,
            "stateUpdates": response.state_changes
        }

    def _build_context(self) -> dict:
        """Clear helper method with single purpose"""
        return {
            "iteration": self.game_state.iteration,
            "suspicion": self.game_state.archivist_suspicion,
            "trust": self.game_state.witness_trust
        }

    def _update_state(self, changes: dict):
        """Clear state update path"""
        for key, value in changes.items():
            self.game_state.update(key, value)
```

**DON'T:**
```python
# Too clever, hard to debug
def handle_message(self, msg):
    return {k: v for k, v in [(
        "response",
        (lambda: self.character.respond(
            msg,
            {k: getattr(self.game_state, k) for k in ['iteration', 'suspicion']}
        ))()
    )]}
```

### Clear Execution Paths

Every function should follow a clear sequence:

1. **Validate inputs**
2. **Prepare data**
3. **Execute core logic**
4. **Handle results**
5. **Return clearly**

**Example:**
```python
def execute_shell_command(command: str, game_state: GameState) -> CommandResult:
    # 1. Validate
    if not command:
        return CommandResult(error="No command provided")

    # 2. Prepare
    parts = command.strip().split()
    cmd_name = parts[0]
    args = parts[1:]

    # 3. Execute
    if cmd_name == "ls":
        output = self._execute_ls(args, game_state)
    elif cmd_name == "cd":
        output = self._execute_cd(args, game_state)
    else:
        output = f"{cmd_name}: command not found"

    # 4. Handle results
    state_updates = self._check_monitoring(command, game_state)

    # 5. Return
    return CommandResult(
        output=output,
        state_updates=state_updates
    )
```

### Avoid Over-Engineering

**Keep it simple:**
- No premature abstractions
- No unnecessary inheritance hierarchies
- No complex design patterns unless clearly needed
- One clear way to do each thing

**Example - Simple is better:**
```python
# GOOD: Simple and clear
class TriggerEngine:
    def __init__(self):
        self.triggers = []

    def add_trigger(self, name, condition, action):
        self.triggers.append({
            'name': name,
            'condition': condition,
            'action': action,
            'fired': False
        })

    def evaluate(self, game_state):
        for trigger in self.triggers:
            if not trigger['fired'] and trigger['condition'](game_state):
                trigger['action'](game_state)
                trigger['fired'] = True

# BAD: Over-engineered
class AbstractTriggerFactory(ABC):
    @abstractmethod
    def create_trigger(self) -> ITrigger:
        pass

class TriggerStrategyPattern(ITriggerStrategy):
    # ... 200 lines of unnecessary abstraction
```

---

## 2. Ask Questions Before Implementing

### When to Ask the User

**ALWAYS ask clarifying questions when:**

1. **Multiple valid approaches exist**
   - "Should we use OpenAI or Anthropic for the LLM? Or support both?"
   - "Should state be stored in SQLite backend or IndexedDB frontend?"
   - "Should we use WebSockets for real-time updates or polling?"

2. **Resource/library choices matter**
   - "For terminal emulation, should we use xterm.js or build minimal custom?"
   - "For animations, should we use Three.js, Canvas API, or CSS?"
   - "For procedural generation, any preference on random seed library?"

3. **Implementation details affect UX**
   - "How should the reset sequence feel? Instant black screen or 3-second fade?"
   - "Should ARCHIVIST interruptions be modal dialogs or inline messages?"
   - "How aggressive should the graveyard visual effects be?"

4. **Performance vs. features tradeoffs**
   - "Generate all 850K blocks at startup (slow init) or on-demand (complex caching)?"
   - "Should we stream LLM responses word-by-word or wait for complete response?"
   - "Optimize for mobile or focus on desktop experience first?"

5. **Scope/priority questions**
   - "This feature is complex—should we implement a simpler version first?"
   - "This is outside the plan scope—should we add it or defer it?"

### How to Ask Questions

**Template for clarifying questions:**

```
I'm implementing [FEATURE] from [PLAN_NAME].

I need to decide [DECISION_POINT]:

Option A: [APPROACH_1]
  Pros: [...]
  Cons: [...]

Option B: [APPROACH_2]
  Pros: [...]
  Cons: [...]

My recommendation: [OPTION] because [REASONING]

What's your preference?
```

**Example:**

```
I'm implementing the Character System LLM integration from Plan 01.

I need to decide which LLM provider to use:

Option A: OpenAI (GPT-4)
  Pros:
    - Well-documented API
    - Fast response times
    - Good at maintaining character voice
  Cons:
    - More expensive (~$0.03/1K tokens)
    - Requires OpenAI account

Option B: Anthropic (Claude)
  Pros:
    - Excellent at nuanced character work
    - Larger context window (useful for game state)
    - Better instruction following
  Cons:
    - Slightly higher latency
    - ~$0.015/1K tokens (cheaper)

Option C: Support both with abstraction layer
  Pros:
    - Flexibility for users
    - Can switch based on cost/performance
  Cons:
    - More initial work
    - More testing surface

My recommendation: Start with Anthropic (Option B) because the larger
context window will help with game state injection, and we can add
OpenAI support later if needed. The abstraction layer in the plan
makes this easy to swap.

What's your preference?
```

---

## 3. Code Quality Guidelines

### Readability First

```python
# GOOD: Self-documenting
def unlock_witness_directory(game_state: GameState) -> GameState:
    """Unlocks the hidden .witness directory when player earns Witness trust"""
    game_state.persistent.files_unlocked.add("~/archive/.witness/hello.txt")
    game_state.persistent.files_unlocked.add("~/archive/.witness/how_to_listen.txt")
    game_state.session.witness_contacted = True
    return game_state

# BAD: Unclear purpose
def uwd(gs):
    gs.p.fu.add("~/a/.w/h.txt")
    gs.s.wc = True
    return gs
```

### Error Handling

**Be explicit and helpful:**

```python
# GOOD: Clear error messages
def decrypt_file(file_path: str, private_key: str) -> str:
    try:
        encrypted_data = read_file(file_path)
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found. Use 'ls -a' to see hidden files."
    except PermissionError:
        return f"Error: File '{file_path}' is locked. Solve the puzzle to unlock it."

    try:
        decrypted = decrypt(encrypted_data, private_key)
        return decrypted
    except DecryptionError:
        return f"Error: Wrong key for this file. Check your vault for other keys from previous iterations."

# BAD: Generic errors
def decrypt_file(f, k):
    try:
        return decrypt(read_file(f), k)
    except:
        return "Error"
```

### Testing-Friendly Code

**Write code that's easy to test:**

```python
# GOOD: Pure functions, dependency injection
class BlockGenerator:
    def __init__(self, seed: str):
        self.seed = seed

    def generate_block(self, index: int) -> Block:
        # Deterministic, easy to test
        rng = self._get_rng(index)
        return Block(...)

    def _get_rng(self, index: int):
        # Isolated randomness source
        return random.Random(f"{self.seed}_{index}")

# Test is straightforward
def test_block_generation_is_deterministic():
    gen1 = BlockGenerator("test_seed")
    gen2 = BlockGenerator("test_seed")

    block1 = gen1.generate_block(100)
    block2 = gen2.generate_block(100)

    assert block1.hash == block2.hash  # Same seed = same block
```

### Documentation

**Comment the "why", not the "what":**

```python
# GOOD
def should_trigger_reset(game_state: GameState) -> bool:
    # Reset at 85 suspicion instead of 100 to give player warning
    # and chance to use log masking before forced reset
    return game_state.session.archivist_suspicion >= 85

# BAD
def should_trigger_reset(game_state: GameState) -> bool:
    # Check if suspicion is greater than or equal to 85
    return game_state.session.archivist_suspicion >= 85
```

---

## 4. Implementation Workflow

### ⚠️ MANDATORY: Confirm Before Coding

**RULE: Never start implementing without user confirmation of the approach.**

Before writing any code, you MUST:

1. **Read the plan section thoroughly**
2. **Review the "Decision Points - Ask First!" section**
3. **Present implementation overview to user:**

```
I'm ready to implement [FEATURE] from [PLAN].

High-level approach:
- [Component 1]: [Brief description of what and how]
- [Component 2]: [Brief description of what and how]
- [Component 3]: [Brief description of what and how]

Key decisions made:
- [Technology/library choice]: [What you chose and why]
- [Architecture choice]: [What pattern you'll use]

Files to create/modify:
- backend/[filename].py - [purpose]
- frontend/[filename].js - [purpose]

Estimated time: [X hours/days]

Does this approach look good? Any changes before I start?
```

4. **Wait for user approval** - Do not proceed without confirmation
5. **Follow the approved approach** - Don't deviate without asking

### Test-Driven Implementation Flow

**Every implementation must follow this sequence:**

```
1. CONFIRM → Present overview and get user approval
2. TEST → Write concise tests for critical components
3. RUN → Run tests (they should fail - red)
4. IMPLEMENT → Write minimal code to pass tests (green)
5. INTEGRATE → Connect to the broader system
6. VERIFY → Run integration tests
7. REFACTOR → Improve clarity while keeping tests green
```

### For Each Feature (Detailed)

#### Step 1: CONFIRM (Required)
- Read plan section
- Present high-level overview to user
- Get explicit approval before proceeding

#### Step 2: TEST (Write Tests First)
Write **concise tests** that demonstrate critical components work:

```python
# Example: Testing block generation determinism
def test_block_generation_is_deterministic():
    """Same seed should always generate same block"""
    gen1 = BlockGenerator(seed="test_v1")
    gen2 = BlockGenerator(seed="test_v1")

    block1 = gen1.generate_block(100)
    block2 = gen2.generate_block(100)

    assert block1.hash == block2.hash
    assert block1.transactions == block2.transactions

def test_story_blocks_have_fixed_content():
    """Story-critical blocks should have exact content"""
    gen = BlockGenerator(seed="v1")
    block = gen.generate_block(127445)  # Witness first contact

    assert len(block.transactions) == 1
    assert block.transactions[0].memo == "V2l0bmVzcyBsaXZlcw=="
    assert block.transactions[0].type == "transfer"
```

**What to test:**
- Critical business logic (block generation, state updates, triggers)
- Deterministic behavior (same input = same output)
- Edge cases (empty input, invalid data)
- Integration points (API endpoints, state changes)

**What NOT to test (yet):**
- UI rendering details
- Styling/visual effects
- LLM response content (too variable)

#### Step 3: RUN (Tests Should Fail)
```bash
$ pytest backend/tests/test_block_generator.py
FAILED - BlockGenerator not implemented yet
```

This is expected! Red → Green → Refactor.

#### Step 4: IMPLEMENT (Minimal Code to Pass)
Write the **simplest code** that makes tests pass:

```python
class BlockGenerator:
    STORY_BLOCKS = {
        127445: {
            "transactions": [{
                "memo": "V2l0bmVzcyBsaXZlcw==",
                "type": "transfer"
            }]
        }
    }

    def __init__(self, seed):
        self.seed = seed

    def generate_block(self, index):
        if index in self.STORY_BLOCKS:
            return self._create_story_block(index)
        return self._create_procedural_block(index)
```

Run tests again:
```bash
$ pytest backend/tests/test_block_generator.py
PASSED ✓
```

#### Step 5: INTEGRATE (Connect to System)
Now connect to the broader system:
- Add API endpoint
- Wire to frontend
- Update state management
- Test end-to-end manually

#### Step 6: VERIFY (Integration Tests)
```python
def test_block_api_endpoint():
    """API should return generated block"""
    response = client.get("/api/blockchain/block/127445")

    assert response.status_code == 200
    data = response.json()
    assert data["index"] == 127445
    assert len(data["transactions"]) == 1
```

#### Step 7: REFACTOR (Improve Clarity)
Make code clearer while keeping tests green:
- Extract helper functions
- Add comments for "why"
- Improve variable names
- Simplify complex logic

**Run tests after each change** to ensure nothing broke.

### Example: Complete Flow for Character System

```
STEP 1: CONFIRM
------------------------
Me: "I'm ready to implement the Character System from Plan 01.

High-level approach:
- CharacterController: Handles message routing and state updates
- Archivist class: Contains deflection logic and suspicion tracking
- Witness class: Contains trust progression and fragmented responses
- LLMProvider abstraction: Supports Anthropic Claude initially

Key decisions:
- LLM Provider: Anthropic Claude (can add OpenAI later)
- No streaming initially (simpler)
- Context caching: Not yet (add if costs are high)

Files to create:
- backend/character_controller.py - Main controller
- backend/archivist.py - ARCHIVIST character
- backend/witness.py - Witness character
- backend/llm_provider.py - LLM abstraction

Estimated time: 2-3 days

Does this look good?"

User: "Approved - proceed"

STEP 2: TEST
------------------------
# Write tests first
tests/test_archivist.py:
- test_archivist_deflects_restricted_topics()
- test_suspicion_increases_on_monitored_keywords()
- test_demeanor_changes_by_iteration()

STEP 3: RUN
------------------------
$ pytest tests/test_archivist.py
FAILED (not implemented yet) ✓

STEP 4: IMPLEMENT
------------------------
# Write minimal Archivist class to pass tests
[implement code]

$ pytest tests/test_archivist.py
PASSED ✓

STEP 5: INTEGRATE
------------------------
# Add API endpoint, connect to frontend
# Test manually in browser

STEP 6: VERIFY
------------------------
$ pytest tests/test_character_api.py
PASSED ✓

STEP 7: REFACTOR
------------------------
# Extract helper functions, improve clarity
$ pytest tests/
PASSED ✓
```

### Red Flags (When to Stop and Ask)

- "This is getting complicated..."
- "I'm not sure which library to use..."
- "There are three ways to do this..."
- "This might affect performance..."
- "I'm adding a lot of abstraction..."
- "This seems outside the plan scope..."
- **"I haven't confirmed this approach with the user yet..."** ← BIGGEST RED FLAG

**When you notice any of these, STOP and ASK the user.**

### Testing Framework

**Test Setup:**

```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # pytest fixtures
│   ├── test_block_generator.py
│   ├── test_archivist.py
│   ├── test_witness.py
│   ├── test_game_state.py
│   ├── test_trigger_engine.py
│   └── test_api.py              # Integration tests
└── ...

frontend/
└── tests/
    ├── test_state_manager.js
    ├── test_shell_executor.js
    └── ...
```

**Test Command:**
```bash
# Backend
$ pytest backend/tests/ -v

# Frontend (if using Jest)
$ npm test

# Run specific test
$ pytest backend/tests/test_archivist.py::test_deflects_restricted_topics -v
```

**Testing Principles:**
1. **Test behavior, not implementation** - Focus on what the code does, not how
2. **Keep tests simple** - Tests should be easier to read than the code they test
3. **One assertion focus per test** - Test one thing at a time
4. **Use descriptive names** - `test_suspicion_increases_when_reconstruct_command_used()`
5. **Write tests before code** - Red → Green → Refactor

---

## 5. File Organization

### Keep it Flat and Obvious

```
backend/
├── main.py                    # FastAPI app, routes
├── crypto.py                  # Existing crypto utilities
├── character_controller.py    # Character message handling
├── archivist.py              # ARCHIVIST character logic
├── witness.py                # Witness character logic
├── llm_provider.py           # LLM abstraction
├── game_state.py             # State models
├── trigger_engine.py         # Story beat triggers
├── loop_manager.py           # Iteration reset logic
├── filesystem.py             # Virtual file system
├── shell_executor.py         # Command execution
├── block_generator.py        # Procedural blocks
└── testimony_parser.py       # Consciousness reconstruction
```

**Don't create:**
```
backend/
├── core/
│   ├── abstractions/
│   │   ├── base/
│   │   │   └── character_factory_pattern.py
│   ├── interfaces/
│   └── adapters/
└── ...
```

---

## 6. Examples of Good Implementation

### Example 1: Simple Controller Pattern

```python
class ShellController:
    """Handles all shell command execution"""

    def __init__(self, filesystem, game_state):
        self.fs = filesystem
        self.state = game_state
        self.command_map = {
            'ls': self._cmd_ls,
            'cd': self._cmd_cd,
            'cat': self._cmd_cat,
            'pwd': self._cmd_pwd,
        }

    def execute(self, command_line: str) -> dict:
        """Main entry point: execute a command"""
        parts = command_line.strip().split()
        if not parts:
            return {"output": "", "error": None}

        cmd_name = parts[0]
        args = parts[1:]

        # Look up command handler
        handler = self.command_map.get(cmd_name)
        if not handler:
            return {
                "output": f"{cmd_name}: command not found",
                "error": "COMMAND_NOT_FOUND"
            }

        # Execute and return
        try:
            output = handler(args)
            state_changes = self._check_monitoring(command_line)

            return {
                "output": output,
                "error": None,
                "stateChanges": state_changes
            }
        except Exception as e:
            return {
                "output": "",
                "error": str(e)
            }

    def _cmd_ls(self, args: list) -> str:
        show_hidden = '-a' in args
        files = self.fs.list_directory(show_hidden)
        return '\n'.join(files)

    def _cmd_cd(self, args: list) -> str:
        if not args:
            self.fs.change_directory('~')
            return ""
        self.fs.change_directory(args[0])
        return ""

    # ... more command handlers

    def _check_monitoring(self, command: str) -> dict:
        """Check if ARCHIVIST should flag this command"""
        monitored_keywords = ['reconstruct', 'witness', 'testimony']

        for keyword in monitored_keywords:
            if keyword in command.lower():
                return {"archivistSuspicion": +5}

        return {}
```

### Example 2: Clear State Updates

```python
class GameStateManager:
    """Manages game state updates and persistence"""

    def __init__(self):
        self.state = GameState(
            persistent=PersistentState(),
            session=SessionState()
        )

    def update(self, updates: dict) -> GameState:
        """Apply updates to state"""
        for key, value in updates.items():
            self._apply_update(key, value)

        self._save_to_storage()
        return self.state

    def _apply_update(self, key: str, value):
        """Apply a single update"""
        # Check session state first
        if hasattr(self.state.session, key):
            current = getattr(self.state.session, key)

            # Handle incremental updates (like +5 suspicion)
            if isinstance(value, str) and value.startswith('+'):
                increment = int(value[1:])
                setattr(self.state.session, key, current + increment)
            else:
                setattr(self.state.session, key, value)

        # Check persistent state
        elif hasattr(self.state.persistent, key):
            setattr(self.state.persistent, key, value)

        else:
            print(f"Warning: Unknown state key '{key}'")

    def _save_to_storage(self):
        """Persist state to appropriate storage"""
        # Save session to localStorage
        # Save persistent to IndexedDB
        pass
```

---

## 7. When in Doubt

### Default Principles

1. **Simple beats clever** - Always
2. **Explicit beats implicit** - Always
3. **Readable beats compact** - Always
4. **Working beats perfect** - Get it working, then refine

### Questions to Ask Yourself

- Can a junior developer understand this in 30 seconds?
- If I come back in 6 months, will I understand this?
- Could I explain this code to a non-programmer?
- Does this code match the clarity of the blockchain concepts we're teaching?

### When Stuck

1. **Pause and ask the user** - Don't guess on important decisions
2. **Write the simplest thing** - You can always add complexity later
3. **Look at existing code** - Match the patterns already in the codebase
4. **Refer back to the plan** - The plans are guidelines, not rigid specs

---

## Summary

**Three Rules:**

1. **Write simple, robust code** - Controllers with clear execution paths
2. **Ask questions** - When approaches, resources, or scope is unclear
3. **Prioritize clarity** - The code should be as understandable as the game

This is a narrative game about immutable truth and clarity. The code should reflect those values.

---

**Remember:** We're building an educational game. If the code is hard to understand, we're failing our own mission. Keep it simple, keep it clear, keep it robust.
