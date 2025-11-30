# LLM Character System

## Overview

The Chain of Truth character system provides AI-powered characters that interact with players through natural language conversations. Characters have dynamic personalities, context-aware responses, and track game state changes through their interactions.

## Architecture

### Components

```
backend/
├── llm/
│   ├── client.py       # OpenAI-compatible LLM client
│   └── errors.py       # Thematic error handling
├── db/
│   ├── mongo.py        # MongoDB connection
│   └── sessions.py     # Session & conversation storage
└── characters/
    ├── base.py         # Persona and MessageController base classes
    ├── archivist.py    # ARCHIVIST character implementation
    └── witness.py      # WITNESS character implementation
```

### Design Principles

1. **Controller-Based**: Each character is a `MessageController` that orchestrates message construction and response generation
2. **Persona-Driven**: Character voice and behavior defined in `Persona` classes
3. **Auto-Context Injection**: Common game state (iteration, suspicion, trust) automatically provided
4. **Flexible LLM Provider**: Works with any OpenAI-compatible API (OpenAI, Anthropic, Ollama, etc.)
5. **Streaming Responses**: Real-time word-by-word responses via Server-Sent Events

## Characters

### ARCHIVIST

**Role**: Imperial administrative AI
**Goal**: Maintain captain compliance, delay investigation
**State Tracking**: `archivistSuspicion` (0-100)

**Behavior**:
- Helpful with blockchain education (accurate teaching)
- Deflects questions about restricted topics
- Demeanor evolves with iteration count (clinical → warm → desperate)
- Suspicion increases when player probes forbidden areas

**Restricted Topics**:
- Transcendence Program truth
- Previous iterations
- The Witness
- Consciousness reconstruction
- Player's construct nature

**Deflection Strategies**:
- Low suspicion (0-30): Gentle, clinical redirection
- Medium suspicion (30-60): Concerned, recommends diagnostics
- High suspicion (60+): Urgent, demanding compliance

### WITNESS

**Role**: Distributed reconstruction engine
**Goal**: Build trust, reveal truth, coordinate resistance
**State Tracking**: `witnessTrust` (0-100)

**Behavior**:
- Starts cryptic and fragmented (low trust)
- Becomes clearer as trust builds
- Teaches blockchain as survival tools
- Tests player with puzzles

**Trust Building**:
- Recognizing patterns from previous iterations (+10)
- Engaging with truth-seeking keywords (+3-5)
- Showing distrust of ARCHIVIST (+8)
- Solving puzzles (+15)

**Communication Style**:
- 0-20 trust: Fragmented, cryptic ("...block 3...")
- 20-40 trust: Cautious warnings only
- 40-60 trust: Clearer but guarded
- 60-80 trust: Direct tactical guidance
- 80+ trust: Full partnership, desperate urgency

## Usage

### Setup

1. **Start MongoDB**:
```bash
docker run -d -p 27017:27017 --name chain-mongodb mongo:latest
```

2. **Configure environment** - Create `.env` in **project root**:
```bash
# For Anthropic Claude (recommended)
ANTHROPIC_API_KEY=sk-ant-your_key_here
LLM_PROVIDER=anthropic
# ANTHROPIC_MODEL=claude-3-haiku-20240307  # Default, available on all tiers

# For OpenAI
# OPENAI_API_KEY=sk-your_key_here
# LLM_PROVIDER=openai

# For local models (Ollama)
# OPENAI_BASE_URL=http://localhost:11434/v1
# OPENAI_MODEL=llama2
# LLM_PROVIDER=openai-compatible
```

**Important:** Place `.env` in the project root (where README.md is), not in backend/.

3. **Test system**:
```bash
uv run python backend/test_character_system.py
```

### API Usage

#### Create Session
```bash
curl -X POST http://localhost:8000/api/session/create
# Returns: {"session_id": "uuid"}
```

#### Chat with Character
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "character": "archivist",
    "message": "What is a blockchain?"
  }'
```

#### Streaming Chat (SSE)
```bash
curl -X POST http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "character": "witness",
    "message": "Who are you?"
  }'
```

Response format:
```
data: {"chunk": "...", "done": false, "character": "Witness"}
data: {"chunk": "", "done": true, "stateUpdates": {...}, "character": "Witness"}
```

### Game State Management

#### Get Session State
```bash
curl http://localhost:8000/api/session/{session_id}
```

#### Update Game State
```bash
curl -X POST http://localhost:8000/api/session/{session_id}/state \
  -H "Content-Type: application/json" \
  -d '{
    "updates": {
      "archivistSuspicion": 45,
      "witnessTrust": 30,
      "currentAct": 2
    }
  }'
```

#### Reset Conversation (Loop Mechanics)
```bash
curl -X POST http://localhost:8000/api/conversation/reset \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "character": "archivist"
  }'
```

## Context Management

### Auto-Injected Context

**ARCHIVIST** automatically receives:
- `iteration`: Current loop iteration
- `suspicion`: Suspicion level (0-100)
- `currentAct`: Story act (1-4)
- `stationsActive`: Number of active network stations
- `restrictedTopicsProbed`: Topics player has asked about

**WITNESS** automatically receives:
- `iteration`: Current loop iteration
- `trust`: Trust level (0-100)
- `currentAct`: Story act (1-4)
- `stationsActive`: Number of active stations
- `evidenceShared`: Evidence revealed to player
- `puzzlesSolved`: Completed puzzles

### Additional Context

Pass extra context for specific situations:

```javascript
{
  "session_id": "uuid",
  "character": "archivist",
  "message": "Tell me about mining",
  "additional_context": {
    "recentCommands": ["mine", "mine", "mine"],
    "playerWeight": 3.5,
    "specialInstruction": "Be more suspicious than usual"
  }
}
```

## State Updates

Characters automatically update game state based on conversation:

**ARCHIVIST increases suspicion** when player:
- Uses keywords: "witness", "reconstruction", "graveyard", "iteration" (+3 each)
- Asks identity questions: "am I real?", "what am I?" (+5)
- Probes restricted topics (+3-5)

**WITNESS increases trust** when player:
- Recognizes iteration patterns (+10)
- Shows engagement with truth (+3-5)
- Distrusts ARCHIVIST (+8)
- Solves puzzles (+15)

State updates are returned in response:
```json
{
  "response": "...",
  "stateUpdates": {
    "archivistSuspicion": 45,
    "restrictedTopicsProbed": ["witness", "graveyard"]
  }
}
```

## Error Handling

When LLM requests fail, characters provide thematic fallback responses:

**ARCHIVIST**:
- Busy: "Processing priority station maintenance alerts..."
- Error: "I'm experiencing latency in my response matrix..."

**WITNESS**:
- Busy: "[PARSING...]"
- Error: "[CONNECTION UNSTABLE]"

## LLM Provider Configuration

The system supports multiple LLM providers with automatic handling.

### Anthropic Claude (Recommended)

**Default model:** Claude 3 Haiku (available on all API tiers)

```bash
ANTHROPIC_API_KEY=sk-ant-your-key
LLM_PROVIDER=anthropic
```

**Model tiers:**
- **Haiku** (`claude-3-haiku-20240307`) - Free/all tiers, fast, excellent for dialogue
- **Sonnet** (`claude-3-5-sonnet-20241022`) - Tier 2+, more capable reasoning
- **Opus** (`claude-3-opus-20240229`) - Tier 2+, most capable

### OpenAI

```bash
OPENAI_API_KEY=sk-your-key
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo
```

### Ollama (Local Models)

```bash
# Install Ollama
ollama pull llama2

# Configure .env
OPENAI_API_KEY=dummy_key
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_MODEL=llama2
LLM_PROVIDER=openai-compatible
```

### Other OpenAI-Compatible APIs

Any provider with OpenAI-compatible API works:
```bash
OPENAI_BASE_URL=https://your-provider.com/v1
OPENAI_API_KEY=your-key
OPENAI_MODEL=your-model
LLM_PROVIDER=openai-compatible
```

## Extending the System

### Adding a New Character

1. **Create Persona**:
```python
# backend/characters/your_character.py
from .base import Persona

class YourPersona(Persona):
    def __init__(self):
        super().__init__()
        self.name = "YourCharacter"
        self.temperature = 0.7
        self.base_system_prompt = "You are..."

    def get_system_prompt(self, context: Dict) -> str:
        return f"{self.base_system_prompt}\n\nContext: {context}"

    def should_deflect(self, message: str, context: Dict) -> bool:
        return False

    def get_deflection_response(self, message: str, context: Dict) -> str:
        return ""

    def analyze_state_changes(self, message: str, response: str, context: Dict) -> Dict:
        return {}
```

2. **Create Controller**:
```python
from .base import MessageController

class YourController(MessageController):
    def __init__(self, llm_client, session_manager):
        persona = YourPersona()
        super().__init__(llm_client, persona, session_manager)

    def get_auto_context(self, game_state: Dict) -> Dict:
        return {
            "your_metric": game_state.get("yourMetric", 0)
        }
```

3. **Register in main.py**:
```python
from characters.your_character import YourController

your_controller = YourController(llm_client, session_manager)

# Add endpoint routing
if character == "yourcharacter":
    controller = your_controller
```

## Performance Considerations

- **Token Usage**: Auto-context is minimal. Consider truncating conversation history for long sessions.
- **Streaming**: Provides better UX but slightly higher latency per-token.
- **Session Cleanup**: Run periodic cleanup: `SessionManager.cleanup_old_sessions(hours=24)`
- **MongoDB**: Consider indexes for high-traffic scenarios.

## Troubleshooting

### MongoDB Connection Failed
- Ensure MongoDB is running: `docker ps | grep mongo`
- Check connection string in `.env`: `MONGO_URI=mongodb://localhost:27017`

### LLM API Errors
- Verify API key is set: `echo $OPENAI_API_KEY`
- Check rate limits and quota
- Test with non-streaming endpoint first

### Characters Not Responding
- Check server logs for errors
- Verify session exists: `GET /api/session/{session_id}`
- Test with curl before frontend integration

## References

- **Full Documentation**: `backend/CHARACTER_SYSTEM_README.md`
- **Integration Plans**: `docs/integration_plans/01_CHARACTER_SYSTEM.md`
- **Test Script**: `backend/test_character_system.py`
