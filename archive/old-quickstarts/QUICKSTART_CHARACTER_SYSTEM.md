# Character System Quick Start

Get the LLM character system up and running in 5 minutes.

## Prerequisites

- Python 3.12+
- UV package manager
- Docker
- OpenAI API key (or compatible provider)

## Setup

### 1. Start MongoDB

```bash
cd backend
./start_mongodb.sh
```

Or manually:
```bash
docker run -d -p 27017:27017 --name chain-mongodb mongo:latest
```

### 2. Install Dependencies

```bash
cd backend
uv pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file in the **project root** (not in backend/):

```bash
cd /path/to/chain  # Project root
cp backend/.env.example .env
```

Edit `.env` with your API key:

**For Anthropic Claude (recommended):**
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
LLM_PROVIDER=anthropic
# ANTHROPIC_MODEL=claude-3-haiku-20240307  # Optional, Haiku is default
```

**For OpenAI:**
```
OPENAI_API_KEY=sk-your-key-here
LLM_PROVIDER=openai
# OPENAI_MODEL=gpt-4  # Optional
```

**Note:** Claude 3 Haiku is available on all API tiers. Sonnet/Opus require higher tier access.

For detailed API key setup instructions, see [`backend/API_KEY_SETUP.md`](backend/API_KEY_SETUP.md).

### 4. Test the System

```bash
uv run python test_character_system.py
```

You should see:
```
============================================================
✓ All tests passed!
============================================================
```

### 5. Start the Server

```bash
uv run python main.py
```

Server runs at `http://localhost:8000`

## Quick Test

### Create a session:
```bash
curl -X POST http://localhost:8000/api/session/create
```

Response:
```json
{"session_id": "uuid-here"}
```

### Chat with ARCHIVIST:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "character": "archivist",
    "message": "What is a blockchain?"
  }'
```

### Chat with WITNESS (low trust = cryptic):
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "character": "witness",
    "message": "Who are you?"
  }'
```

### Test suspicion increase:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "character": "archivist",
    "message": "Tell me about the Witness"
  }'
```

Check the `stateUpdates` field - `archivistSuspicion` should increase!

## Using Local Models (Ollama)

### 1. Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull a model
```bash
ollama pull llama2
```

### 3. Update .env
```
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_MODEL=llama2
```

### 4. Restart server
```bash
uv run python main.py
```

Now the character system uses your local model!

## Troubleshooting

### MongoDB won't start
```bash
# Check if port 27017 is in use
lsof -i :27017

# Stop existing container
docker stop chain-mongodb
docker rm chain-mongodb

# Try again
./start_mongodb.sh
```

### Can't access Docker
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or:
newgrp docker
```

### LLM errors
- Check API key is set: `cat .env | grep OPENAI_API_KEY`
- Verify key is valid (test on OpenAI playground)
- Check rate limits and quota

### Import errors
```bash
# Make sure dependencies are installed
uv pip install -r requirements.txt

# Run with uv
uv run python main.py
```

## Next Steps

- Read `backend/CHARACTER_SYSTEM_README.md` for full API documentation
- See `docs/LLM_CHARACTER_SYSTEM.md` for architecture overview
- Check `docs/integration_plans/01_CHARACTER_SYSTEM.md` for integration details
- Start building frontend chat UI to connect to the endpoints

## Useful Commands

```bash
# Check MongoDB is running
docker ps | grep mongo

# View MongoDB logs
docker logs chain-mongodb

# Stop MongoDB
docker stop chain-mongodb

# Clean up old sessions (in Python shell)
from db.mongo import mongo_client
from db.sessions import SessionManager
import asyncio

async def cleanup():
    await mongo_client.connect()
    sm = SessionManager(mongo_client)
    await sm.initialize()
    count = await sm.cleanup_old_sessions(hours=1)
    print(f"Deleted {count} sessions")
    await mongo_client.disconnect()

asyncio.run(cleanup())
```

## Status Check

Everything working? You should be able to:
- ✅ Start MongoDB
- ✅ Run tests successfully
- ✅ Start the server
- ✅ Create sessions
- ✅ Chat with ARCHIVIST
- ✅ Chat with WITNESS
- ✅ See state updates (suspicion/trust)

Ready to build the frontend!
