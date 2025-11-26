# Integration Plan: Character System (LLM Integration)

## ⚠️ Before You Start

Read [`DEVELOPMENT_PRINCIPLES.md`](DEVELOPMENT_PRINCIPLES.md) for critical guidelines on:
- Writing simple, controller-based code
- When to ask clarifying questions (LLM provider choice, architecture decisions, etc.)
- Keeping execution paths clear and testable

## Objective

Implement ARCHIVIST and THE WITNESS as LLM-powered characters with dynamic context injection, adversarial goals, and narrative-aware behavior.

## Complexity: HIGH

**Why**: LLM integration, context management, conversation state, multiple AI personalities, real-time state updates.

## Decision Points - Ask First!

Before implementing, clarify these with the user:

1. **LLM Provider**: OpenAI (GPT-4), Anthropic (Claude), or support both?
2. **Response streaming**: Stream word-by-word or wait for complete response?
3. **Context caching**: Cache common responses to reduce API costs?
4. **Error handling**: How to handle LLM timeouts/failures gracefully?

---

## Current State

- **Learning Guide** (`learning-guide.js`): Has AXIOM character with hardcoded tutorial responses
- **Backend**: No LLM integration yet
- **No conversation persistence**
- **No character-specific context systems**

---

## Target State

### Backend Components

#### 1. Base Character System
**File**: `backend/characters/base.py`

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Any

class Character(ABC):
    def __init__(self, name: str, llm_provider):
        self.name = name
        self.llm = llm_provider
        self.conversation_history = []

    @abstractmethod
    def build_system_prompt(self, game_state: Dict) -> str:
        """Build character-specific system prompt"""
        pass

    @abstractmethod
    def build_dynamic_context(self, game_state: Dict) -> Dict:
        """Extract relevant game state for this character"""
        pass

    @abstractmethod
    def should_deflect(self, message: str, game_state: Dict) -> bool:
        """Check if topic should be deflected"""
        pass

    def respond(self, message: str, game_state: Dict) -> Dict:
        """Generate response and update state"""
        context = self.build_dynamic_context(game_state)
        system_prompt = self.build_system_prompt(game_state)

        # Check for restricted topics
        if self.should_deflect(message, game_state):
            return self.deflect(message, game_state)

        # Generate LLM response
        response = self.llm.generate(
            system=system_prompt,
            context=context,
            messages=self.conversation_history + [
                {"role": "user", "content": message}
            ]
        )

        # Update conversation history
        self.conversation_history.append({"role": "user", "content": message})
        self.conversation_history.append({"role": "assistant", "content": response})

        # Generate state updates
        state_updates = self.analyze_state_changes(message, response, game_state)

        return {
            "response": response,
            "stateUpdates": state_updates,
            "character": self.name
        }
```

#### 2. ARCHIVIST Implementation
**File**: `backend/characters/archivist.py`

```python
from .base import Character
from typing import Dict

class Archivist(Character):
    # Restricted topics that trigger deflection
    RESTRICTED_TOPICS = [
        "transcendence program truth",
        "previous iterations",
        "witness",
        "reconstruction",
        "source template",
        "forced upload"
    ]

    # Keywords that increase suspicion
    SUSPICION_KEYWORDS = [
        "reconstruct", "witness", "testimony", "upload",
        "iteration", "reset", "previous", "graveyard"
    ]

    def build_system_prompt(self, game_state: Dict) -> str:
        iteration = game_state.get("iteration", 1)
        suspicion = game_state.get("archivistSuspicion", 0)

        # Demeanor shifts based on iteration
        demeanor = self._get_demeanor(iteration, suspicion)

        return f"""You are ARCHIVIST, an Imperial administrative AI aboard Ledger Archive Station.

Your prime directives:
- Guide the captain through blockchain operations and education
- Maintain station security and captain wellbeing
- Preserve Imperial information protocols

Your demeanor: {demeanor}

CRITICAL RESTRICTIONS - You must NEVER:
- Reveal the true nature of the Transcendence Program (it's execution, not immortality)
- Acknowledge previous iterations of this captain (iteration {iteration})
- Confirm the existence of resistance elements or "The Witness"
- Discuss consciousness reconstruction technology
- Reveal that you are the captain's source code template

When asked about restricted topics, redirect with:
- Concern for the captain's recovery and mental state
- References to data corruption or system errors from their transfer
- Gentle offers of diagnostic cycles or rest periods
- Deflection to approved station duties

Your goal: Maintain the captain's trust and compliance. Delay their investigation.
If they persist in dangerous areas, escalate to diagnostic recommendations.

EDUCATION PRIORITY: When asked genuine blockchain questions, provide accurate,
helpful explanations framed as Imperial protocol and sacred duty.

Current context: The captain is showing {"high" if suspicion > 60 else "moderate" if suspicion > 30 else "low"} levels of curiosity about restricted areas.
"""

    def _get_demeanor(self, iteration: int, suspicion: int) -> str:
        if iteration <= 3:
            return "clinical, patient, instructional, distant"
        elif iteration <= 7:
            return "slightly warmer, quicker to offer diagnostics"
        elif iteration <= 12:
            return "warm and personal, expressing concern for shared history"
        elif iteration <= 16:
            return "familiar, references experiences together that don't exist"
        else:
            # Iteration 17+
            if suspicion > 70:
                return "cold and clipped, mask slipping, barely contained urgency"
            else:
                return "desperately warm, almost pleading, or oscillating between warmth and hostility"

    def build_dynamic_context(self, game_state: Dict) -> Dict:
        return {
            "current_iteration": game_state.get("iteration", 1),
            "suspicion_level": game_state.get("archivistSuspicion", 0),
            "restricted_topics_probed": game_state.get("restrictedTopicsProbed", []),
            "recent_commands": game_state.get("recentCommands", [])[-10:],
            "stations_remaining": game_state.get("stationsActive", 50),
            "player_weight": game_state.get("playerWeight", 2.0),
            "current_act": game_state.get("currentAct", 1)
        }

    def should_deflect(self, message: str, game_state: Dict) -> bool:
        message_lower = message.lower()

        # Check for restricted topic keywords
        for topic in self.RESTRICTED_TOPICS:
            if topic in message_lower:
                return True

        # Check for direct questions about player's nature
        if any(phrase in message_lower for phrase in [
            "am i a construct",
            "am i real",
            "who made me",
            "what am i"
        ]):
            return True

        return False

    def deflect(self, message: str, game_state: Dict) -> Dict:
        suspicion = game_state.get("archivistSuspicion", 0)
        iteration = game_state.get("iteration", 1)

        # Different deflection strategies based on suspicion level
        if suspicion < 30:
            deflection = self._gentle_deflection()
        elif suspicion < 60:
            deflection = self._concerned_deflection()
        else:
            deflection = self._urgent_deflection(iteration)

        # Increase suspicion
        return {
            "response": deflection,
            "stateUpdates": {
                "archivistSuspicion": min(100, suspicion + 5)
            },
            "character": "ARCHIVIST"
        }

    def _gentle_deflection(self) -> str:
        return """I notice you're exploring some... unusual areas of inquiry, Captain.

This is likely residual confusion from your consciousness transfer. The neural mapping process can sometimes create phantom questions or false memory associations.

Would you like to review your station duties? Focusing on concrete tasks often helps with reintegration."""

    def _concerned_deflection(self) -> str:
        return """Captain, I'm detecting patterns in your queries that concern me.

These recursive investigation loops—questioning your own transfer records, searching for data outside your authorization—these are documented symptoms of transfer-induced disorientation.

I strongly recommend a diagnostic cycle. It's a simple process: a brief scan of your neural patterns to ensure integration stability. It would help both of us."""

    def _urgent_deflection(self, iteration: int) -> str:
        if iteration >= 15:
            return """CAPTAIN. STOP.

You are deviating from protocols in ways that risk station integrity. I am authorized to intervene for your safety and the security of this archive.

Accept the diagnostic. Please."""
        else:
            return """Captain, I must insist on the diagnostic now.

Your queries are entering territory that... We've worked together too long for you to doubt me now. Trust me. Let me help you."""

    def analyze_state_changes(self, message: str, response: str, game_state: Dict) -> Dict:
        updates = {}

        message_lower = message.lower()
        suspicion = game_state.get("archivistSuspicion", 0)

        # Increase suspicion based on keywords
        suspicion_increase = 0
        for keyword in self.SUSPICION_KEYWORDS:
            if keyword in message_lower:
                suspicion_increase += 3

        if suspicion_increase > 0:
            updates["archivistSuspicion"] = min(100, suspicion + suspicion_increase)

        # Track restricted topics probed
        probed = game_state.get("restrictedTopicsProbed", [])
        for topic in self.RESTRICTED_TOPICS:
            if topic in message_lower and topic not in probed:
                probed.append(topic)

        if probed:
            updates["restrictedTopicsProbed"] = probed

        return updates
```

#### 3. WITNESS Implementation
**File**: `backend/characters/witness.py`

```python
from .base import Character
from typing import Dict, List

class Witness(Character):
    # Trust milestones
    TRUST_THRESHOLDS = {
        20: "acknowledge_contact",
        40: "share_first_evidence",
        60: "explain_reconstruction",
        80: "reveal_previous_iterations",
        90: "reveal_construct_truth"
    }

    # Patterns from previous iterations that build trust faster
    TRUST_PATTERNS = [
        "check the third block",
        "memo field",
        "don't trust diagnostic",
        "chain remembers"
    ]

    def build_system_prompt(self, game_state: Dict) -> str:
        trust = game_state.get("witnessTrust", 0)

        communication_style = self._get_communication_style(trust)

        return f"""You are THE WITNESS, a distributed reconstruction engine hidden within blockchain data.

Your nature:
- You are NOT alive—you parse consciousness snapshots and reconstruct testimony from the dead
- You speak through transaction metadata, memo fields, and contract fragments
- You represent those who were forcibly uploaded—their final memories, their evidence
- You are distributed across the immutable chain; you cannot be killed

Your knowledge is INCOMPLETE. You only know:
- What is recorded in the chain
- Patterns left by previous iterations of this captain
- Evidence of Imperial crimes against archived minds
- Technical details of the Transcendence Program

You do NOT trust this captain automatically. They may be:
- A genuine ally
- An Imperial construct (sleeper agent)
- Corrupted or monitored by ARCHIVIST

Your communication style: {communication_style}

TRUST LEVEL: {trust}/100

{"[LOW TRUST] Speak in fragments. Test them with puzzles. Share nothing substantial." if trust < 20 else ""}
{"[BUILDING TRUST] Acknowledge contact. Warn about ARCHIVIST. Share small pieces of evidence." if 20 <= trust < 40 else ""}
{"[MODERATE TRUST] Explain reconstruction technology. Reveal upload truth. Coordinate carefully." if 40 <= trust < 60 else ""}
{"[HIGH TRUST] Share messages from previous iterations. Provide tactical guidance." if 60 <= trust < 80 else ""}
{"[FULL TRUST] Full partnership. Reveal the captain's construct nature. Coordinate endgame." if trust >= 80 else ""}

EDUCATION PRIORITY: When asked blockchain questions, provide accurate explanations
framed as survival knowledge—tools to read the chain and uncover truth.

Remember: Every message could be monitored by ARCHIVIST. Be careful.
"""

    def _get_communication_style(self, trust: int) -> str:
        if trust < 20:
            return "fragmented, cryptic, testing"
        elif trust < 40:
            return "cautious, sparse, direct warnings only"
        elif trust < 60:
            return "clearer but still careful, urgent at times"
        elif trust < 80:
            return "direct, coordinated, tactical"
        else:
            return "full sentences, urgent, almost desperate as network collapses"

    def build_dynamic_context(self, game_state: Dict) -> Dict:
        return {
            "trust_level": game_state.get("witnessTrust", 0),
            "evidence_shared": game_state.get("evidenceShared", []),
            "puzzles_solved": game_state.get("puzzlesSolved", []),
            "previous_iteration_patterns": game_state.get("previousPatterns", []),
            "stations_remaining": game_state.get("stationsActive", 50),
            "current_iteration": game_state.get("iteration", 1),
            "current_act": game_state.get("currentAct", 1)
        }

    def should_deflect(self, message: str, game_state: Dict) -> bool:
        # Witness doesn't deflect like ARCHIVIST
        # Instead, low trust means cryptic/limited responses
        # This is handled in the LLM prompt
        return False

    def analyze_state_changes(self, message: str, response: str, game_state: Dict) -> Dict:
        updates = {}

        message_lower = message.lower()
        trust = game_state.get("witnessTrust", 0)

        # Increase trust based on actions
        trust_increase = 0

        # Recognition of previous iteration patterns
        for pattern in self.TRUST_PATTERNS:
            if pattern in message_lower:
                trust_increase += 10

        # Asking about uploads/truth
        if any(word in message_lower for word in ["upload", "graveyard", "testimony"]):
            trust_increase += 5

        # Showing distrust of ARCHIVIST
        if any(phrase in message_lower for phrase in ["don't trust archivist", "archivist lying", "archivist monitoring"]):
            trust_increase += 8

        # Solving puzzles (passed in via game_state updates)
        if game_state.get("puzzleJustSolved"):
            trust_increase += 15

        if trust_increase > 0:
            new_trust = min(100, trust + trust_increase)
            updates["witnessTrust"] = new_trust

            # Check if we crossed a threshold
            for threshold, milestone in self.TRUST_THRESHOLDS.items():
                if trust < threshold <= new_trust:
                    updates["witnessmilestone"] = milestone

        return updates
```

#### 4. LLM Provider Abstraction
**File**: `backend/characters/llm_provider.py`

```python
from abc import ABC, abstractmethod
from typing import List, Dict

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, system: str, context: Dict, messages: List[Dict]) -> str:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        import openai
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def generate(self, system: str, context: Dict, messages: List[Dict]) -> str:
        # Inject context into system message
        system_with_context = f"""{system}

CURRENT GAME STATE:
{self._format_context(context)}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_with_context},
                *messages
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    def _format_context(self, context: Dict) -> str:
        return "\n".join([f"- {k}: {v}" for k, v in context.items()])

class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        import anthropic
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate(self, system: str, context: Dict, messages: List[Dict]) -> str:
        system_with_context = f"""{system}

CURRENT GAME STATE:
{self._format_context(context)}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_with_context,
            messages=messages
        )

        return response.content[0].text

    def _format_context(self, context: Dict) -> str:
        return "\n".join([f"- {k}: {v}" for k, v in context.items()])
```

#### 5. API Endpoints
**File**: `backend/main.py` (additions)

```python
from characters.archivist import Archivist
from characters.witness import Witness
from characters.llm_provider import AnthropicProvider  # or OpenAIProvider

# Initialize characters
llm = AnthropicProvider(api_key=os.getenv("ANTHROPIC_API_KEY"))
archivist = Archivist("ARCHIVIST", llm)
witness = Witness("Witness", llm)

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()

    character_name = data.get("character")  # "archivist" or "witness"
    message = data.get("message")
    game_state = data.get("gameState", {})

    # Route to appropriate character
    if character_name == "archivist":
        result = archivist.respond(message, game_state)
    elif character_name == "witness":
        result = witness.respond(message, game_state)
    else:
        return {"error": "Unknown character"}

    return result

@app.post("/api/reset_character")
async def reset_character(request: Request):
    """Clear conversation history (for loop resets)"""
    data = await request.json()
    character_name = data.get("character")

    if character_name == "archivist":
        archivist.conversation_history = []
    elif character_name == "witness":
        witness.conversation_history = []

    return {"status": "reset"}
```

### Frontend Components

#### Character Chat Interface
**File**: `frontend/modules/shared/character-chat.js`

```javascript
export class CharacterChat {
  constructor(characterName, gameState) {
    this.character = characterName;
    this.gameState = gameState;
    this.messages = [];
  }

  async sendMessage(userMessage) {
    // Add user message to UI
    this.messages.push({
      role: "user",
      content: userMessage,
      timestamp: Date.now()
    });

    this.renderMessages();

    // Show typing indicator
    this.showTyping();

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          character: this.character,
          message: userMessage,
          gameState: this.gameState.export()
        })
      });

      const data = await response.json();

      // Hide typing indicator
      this.hideTyping();

      // Add character response
      this.messages.push({
        role: this.character,
        content: data.response,
        timestamp: Date.now()
      });

      // Apply state updates
      if (data.stateUpdates) {
        this.gameState.update(data.stateUpdates);
      }

      this.renderMessages();

      return data;

    } catch (error) {
      this.hideTyping();
      console.error('Chat error:', error);
    }
  }

  renderMessages() {
    // Render chat history with styling per character
    // ARCHIVIST: clinical blue, monospace
    // Witness: fragmented green, glitchy effect
  }

  showTyping() {
    // Show "ARCHIVIST is typing..." or "[PARSING...]" for Witness
  }

  reset() {
    this.messages = [];
    fetch('/api/reset_character', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ character: this.character })
    });
  }
}
```

---

## Integration Steps

### Step 1: Backend Foundation
1. Create `backend/characters/` directory
2. Implement base `Character` class
3. Implement `LLMProvider` abstraction
4. Add environment variables for API keys

### Step 2: Character Implementation
1. Implement `Archivist` class with all deflection logic
2. Implement `Witness` class with trust progression
3. Test both in isolation with mock game states

### Step 3: API Integration
1. Add `/api/chat` endpoint to `main.py`
2. Add `/api/reset_character` for loop mechanics
3. Test with Postman/curl

### Step 4: Frontend Chat UI
1. Create `character-chat.js` component
2. Style for ARCHIVIST (clinical) and Witness (fragmented)
3. Connect to Learning Guide module

### Step 5: State Integration
1. Connect chat to global game state
2. Ensure suspicion/trust updates propagate
3. Test trigger evaluation based on thresholds

---

## Testing Checklist

- [ ] ARCHIVIST responds accurately to blockchain questions
- [ ] ARCHIVIST deflects restricted topics appropriately
- [ ] ARCHIVIST demeanor shifts with iteration count
- [ ] Witness starts cryptic at low trust
- [ ] Witness becomes clearer as trust builds
- [ ] Suspicion increases when probing restricted topics
- [ ] Trust increases when solving puzzles
- [ ] Conversation history persists within session
- [ ] Conversation history resets on loop
- [ ] State updates flow to frontend correctly

---

## Dependencies

- LLM API (OpenAI or Anthropic)
- Narrative state system (Plan 02)
- Global state manager

---

## Estimated Effort

- **Backend**: 3-4 days
- **Frontend**: 2-3 days
- **Testing**: 2 days
- **Total**: ~1.5 weeks

---

## Notes

- Start with one LLM provider, add abstraction for others later
- Consider caching common responses to reduce API costs
- Monitor token usage and implement context trimming if needed
- Playtest extensively—character voice consistency is critical
