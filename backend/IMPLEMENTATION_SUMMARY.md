# LLM Character System - Implementation Summary

## What Was Built

A complete LLM-powered character system for Chain of Truth with two AI characters (ARCHIVIST and WITNESS), supporting dynamic narratives, state tracking, and streaming responses.

## Architecture

### Controller-Based Design
- **Persona classes**: Define character voice, behavior, and constraints
- **MessageController classes**: Orchestrate message construction and response generation
- **Auto-context injection**: Common game state automatically provided to LLM
- **Explicit context**: Additional context can be passed per-request

### Flexible LLM Integration
- **OpenAI-compatible client**: Works with OpenAI, Anthropic, Ollama, local models
- **Streaming support**: Real-time word-by-word responses via Server-Sent Events
- **Thematic error handling**: Character-specific fallback responses on failures

### Session Management
- **MongoDB storage**: Session data, conversation history, game state
- **Session-only data**: Simple approach for now, can expand to persistent later
- **Auto-cleanup**: Remove old sessions after 24 hours

## Components Created

```
backend/
├── llm/
│   ├── client.py           # OpenAI-compatible LLM client
│   └── errors.py           # Thematic error fallbacks
├── db/
│   ├── mongo.py            # MongoDB connection & client
│   └── sessions.py         # Session management
├── characters/
│   ├── base.py             # Persona & MessageController base classes
│   ├── archivist.py        # ARCHIVIST character (suspicion tracking)
│   └── witness.py          # WITNESS character (trust building)
├── main.py                 # Updated with character endpoints
├── requirements.txt        # Dependencies
├── .env.example            # Environment configuration template
├── start_mongodb.sh        # MongoDB startup script
├── test_character_system.py # Test suite
└── CHARACTER_SYSTEM_README.md # Full documentation
```

## API Endpoints Added

### Session Management
- `POST /api/session/create` - Create new game session
- `GET /api/session/{session_id}` - Get session state
- `POST /api/session/{session_id}/state` - Update game state

### Chat
- `POST /api/chat/stream` - Streaming chat (SSE)
- `POST /api/chat` - Non-streaming chat
- `POST /api/conversation/reset` - Reset conversation (loop mechanics)

## Characters

### ARCHIVIST
- **Role**: Imperial AI, blockchain educator
- **Behavior**: Helpful with education, deflects restricted topics
- **State**: Suspicion (0-100)
- **Evolution**: Demeanor changes with iteration count
- **Deflection**: Three levels based on suspicion

### WITNESS
- **Role**: Resistance reconstruction engine
- **Behavior**: Cryptic at low trust, clear at high trust
- **State**: Trust (0-100)
- **Evolution**: Communication style changes with trust
- **Trust Building**: Pattern recognition, puzzle solving, ARCHIVIST distrust

## Key Features

1. **Dynamic Context Injection**
   - Auto-injected: iteration, suspicion/trust, act, stations
   - Explicit: recent commands, puzzles, special instructions

2. **State Tracking**
   - Automatic state updates based on conversation
   - Keywords trigger suspicion/trust changes
   - State updates returned with responses

3. **Streaming Responses**
   - Server-Sent Events for real-time output
   - Character-specific typing indicators
   - State updates on completion

4. **Thematic Error Handling**
   - Character-specific fallback messages
   - Different messages for timeouts vs. errors
   - Maintains immersion during failures

5. **Provider Flexibility**
   - Environment-based configuration
   - Support for any OpenAI-compatible API
   - Easy to swap providers (OpenAI → Ollama → Anthropic)

## Testing

All tests passing:
- ✓ MongoDB connection
- ✓ Session creation and retrieval
- ✓ Game state updates
- ✓ Conversation storage
- ✓ Character persona initialization

Run: `uv run python backend/test_character_system.py`

## Setup Requirements

1. **MongoDB**: Docker container running on port 27017
2. **Dependencies**: `uv pip install -r requirements.txt`
3. **Environment**: `.env` file in **project root** with your API key

**Supported providers:**
- Anthropic Claude (Haiku on all tiers, Sonnet/Opus on tier 2+)
- OpenAI (GPT-4, GPT-3.5-turbo)
- Ollama (local models)
- Any OpenAI-compatible API

See [`API_KEY_SETUP.md`](API_KEY_SETUP.md) for detailed setup instructions.

## Usage Example

```bash
# Create session
SESSION_ID=$(curl -X POST http://localhost:8000/api/session/create | jq -r '.session_id')

# Chat with ARCHIVIST
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"character\": \"archivist\",
    \"message\": \"What is a blockchain?\"
  }"

# Response includes state updates
{
  "response": "A blockchain is...",
  "character": "archivist",
  "stateUpdates": {},
  "error": false
}
```

## Next Steps (Frontend Integration)

1. **Create chat UI component** (`frontend/modules/shared/character-chat.js`)
2. **Connect to streaming endpoint** with EventSource for SSE
3. **Display responses** in terminal-style interface
4. **Apply state updates** to game state manager
5. **Handle errors** with character-specific messages

## Documentation

- **Full API docs**: `backend/CHARACTER_SYSTEM_README.md`
- **Quick reference**: `docs/LLM_CHARACTER_SYSTEM.md`
- **Integration plan**: `docs/integration_plans/01_CHARACTER_SYSTEM.md`
- **Main README**: Updated with character system info

## Design Decisions

1. **Controller pattern**: Clear separation between character logic and API concerns
2. **MongoDB for sessions**: Simple, flexible schema for conversation/state storage
3. **Auto-context**: Common state always available, reduces boilerplate
4. **Streaming by default**: Better UX for terminal interface
5. **Thematic errors**: Maintain immersion even during failures
6. **Provider-agnostic**: Easy to switch between LLM providers

## Status

✅ **Complete and tested**
- All core functionality implemented
- Tests passing
- Documentation complete
- Ready for frontend integration
