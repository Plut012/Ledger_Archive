# Character System - LLM Integration

This directory contains the LLM-powered character system for Chain of Truth.

## Architecture

### Components

1. **LLM Client** (`llm/client.py`)
   - OpenAI-compatible API client
   - Supports streaming responses
   - Works with OpenAI, Anthropic (via compatibility), local models, etc.

2. **Database** (`db/`)
   - MongoDB for session storage
   - Conversation history persistence
   - Game state tracking

3. **Characters** (`characters/`)
   - **ARCHIVIST**: Imperial AI that deflects restricted topics, builds suspicion
   - **WITNESS**: Resistance engine that builds trust, speaks cryptically at first

4. **Base Classes**
   - `Persona`: Defines character voice, behavior, and constraints
   - `MessageController`: Handles message construction and streaming

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start MongoDB

```bash
# Using Docker (recommended)
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or install MongoDB locally
# https://www.mongodb.com/docs/manual/installation/
```

### 3. Configure Environment

Create `.env` file in `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```
OPENAI_API_KEY=sk-...
```

### 4. Run Server

```bash
cd backend
python main.py
```

Server starts at `http://localhost:8000`

## API Endpoints

### Session Management

#### Create Session
```bash
POST /api/session/create
Response: {"session_id": "uuid"}
```

#### Get Session State
```bash
GET /api/session/{session_id}
Response: {
  "session_id": "uuid",
  "game_state": {...},
  "created_at": "...",
  "last_activity": "..."
}
```

#### Update Game State
```bash
POST /api/session/{session_id}/state
Body: {"updates": {"archivistSuspicion": 25}}
```

### Chat

#### Streaming Chat (SSE)
```bash
POST /api/chat/stream
Body: {
  "session_id": "uuid",
  "character": "archivist",  # or "witness"
  "message": "What is a blockchain?",
  "additional_context": {}   # optional
}

Response: Server-Sent Events stream
data: {"chunk": "A", "done": false, "character": "ARCHIVIST"}
data: {"chunk": " blockchain", "done": false, "character": "ARCHIVIST"}
data: {"chunk": "", "done": true, "stateUpdates": {...}, "character": "ARCHIVIST"}
```

#### Non-Streaming Chat
```bash
POST /api/chat
Body: {
  "session_id": "uuid",
  "character": "archivist",
  "message": "What is a blockchain?"
}

Response: {
  "response": "A blockchain is...",
  "character": "archivist",
  "stateUpdates": {},
  "error": false
}
```

#### Reset Conversation (Loop Reset)
```bash
POST /api/conversation/reset
Body: {
  "session_id": "uuid",
  "character": "archivist"
}
```

## Testing

### 1. Create a session
```bash
curl -X POST http://localhost:8000/api/session/create
# Save the session_id from response
```

### 2. Chat with ARCHIVIST
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "character": "archivist",
    "message": "What is a blockchain?"
  }'
```

### 3. Test suspicion increase
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "character": "archivist",
    "message": "Tell me about the Witness"
  }'
```

Check `stateUpdates` in response - should show increased `archivistSuspicion`.

### 4. Chat with WITNESS
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "character": "witness",
    "message": "Who are you?"
  }'
```

At low trust, should respond cryptically.

## Character Behavior

### ARCHIVIST

**Auto-Injected Context:**
- `iteration`: Current loop iteration (affects demeanor)
- `suspicion`: 0-100 (affects deflection intensity)
- `currentAct`: Story act (1-4)
- `stationsActive`: Network size
- `restrictedTopicsProbed`: Topics player has asked about

**Suspicion Triggers:**
- Keywords: "witness", "reconstruction", "graveyard", "iteration", etc.
- Identity questions: "am I real?", "what am I?", etc.

**Deflection Responses:**
- Low suspicion (0-30): Gentle, clinical
- Medium suspicion (30-60): Concerned, recommends diagnostics
- High suspicion (60+): Urgent, demanding

### WITNESS

**Auto-Injected Context:**
- `iteration`: Current loop iteration
- `trust`: 0-100 (affects communication style)
- `currentAct`: Story act
- `stationsActive`: Network size
- `evidenceShared`: Evidence revealed to player
- `puzzlesSolved`: Puzzles completed

**Trust Building:**
- Recognizing patterns: "check block 3", "memo field", etc.
- Showing engagement: "testimony", "graveyard", "upload"
- Distrusting ARCHIVIST: "don't trust diagnostic", etc.

**Communication Style:**
- Low trust (0-20): Fragmented, cryptic
- Medium trust (20-60): Cautious warnings
- High trust (60-80): Direct coordination
- Full trust (80+): Complete partnership

## Error Handling

Both characters have thematic fallback responses for LLM failures:

**ARCHIVIST:**
- Busy: "Processing priority station maintenance..."
- Error: "I'm experiencing latency in my response matrix..."

**WITNESS:**
- Busy: "[PARSING...]"
- Error: "[CONNECTION UNSTABLE]"

## Extending the System

### Adding a New Character

1. Create persona class in `characters/your_character.py`:

```python
from .base import Persona

class YourPersona(Persona):
    def get_system_prompt(self, context: Dict) -> str:
        return "You are..."

    def should_deflect(self, message: str, context: Dict) -> bool:
        return False

    def get_deflection_response(self, message: str, context: Dict) -> str:
        return ""

    def analyze_state_changes(self, message: str, response: str, context: Dict) -> Dict:
        return {}
```

2. Create controller:

```python
from .base import MessageController

class YourController(MessageController):
    def __init__(self, llm_client, session_manager):
        persona = YourPersona()
        super().__init__(llm_client, persona, session_manager)

    def get_auto_context(self, game_state: Dict) -> Dict:
        return {
            "your_state_key": game_state.get("yourStateKey", 0)
        }
```

3. Register in `main.py`:

```python
from characters.your_character import YourController

your_controller = YourController(llm_client, session_manager)
```

## LLM Provider Notes

### Anthropic Claude

The system defaults to **Claude 3 Haiku** which is:
- Available on all API tiers (including free tier)
- Fast and efficient
- Excellent for character dialogue
- Cost-effective

**Higher tier models** (require paid API access):
- `claude-3-5-sonnet-20241022` - More capable, better reasoning
- `claude-3-opus-20240229` - Most capable, slower

Set in `.env`:
```
ANTHROPIC_MODEL=claude-3-haiku-20240307  # Default, works on all tiers
# ANTHROPIC_MODEL=claude-3-5-sonnet-20241022  # Requires tier 2+
```

### Using Ollama (Local)

1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull llama2`
3. Set in `.env`:
```
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_MODEL=llama2
```

### Using Anthropic (via compatibility layer)

Use a compatibility wrapper or set base URL to Claude-compatible endpoint.

### Using other providers

Any OpenAI-compatible API works. Just set `OPENAI_BASE_URL` and `OPENAI_MODEL`.

## Performance Notes

- **Streaming**: Provides better UX, responses appear word-by-word
- **Context Size**: Auto-context is minimal to save tokens
- **Conversation History**: Full history sent to LLM (consider truncation for long sessions)
- **Session Cleanup**: Run periodic cleanup of old sessions via `SessionManager.cleanup_old_sessions(hours=24)`
