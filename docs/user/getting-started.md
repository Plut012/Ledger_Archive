# Getting Started with Chain of Truth

Complete installation and setup guide.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [First Run](#first-run)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: Linux, macOS, or Windows (WSL2)
- **Python**: 3.12 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB for dependencies and data
- **Docker**: Latest version for MongoDB
- **Internet**: Required for LLM API calls

### Required Software
```bash
# Check your versions
python3 --version      # Should be 3.12+
docker --version       # Any recent version
```

### API Access
You need an API key from either:
- **Anthropic** (recommended) - Claude 3 Haiku available on all tiers
- **OpenAI** - GPT-3.5/GPT-4

---

## Installation

### Step 1: Clone or Navigate to Project

```bash
cd /path/to/chain
```

### Step 2: Install UV Package Manager

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Or using pip:**
```bash
pip install uv
```

**Verify installation:**
```bash
uv --version
```

### Step 3: Install Python Dependencies

```bash
cd backend
uv pip install -r requirements.txt
```

This installs:
- FastAPI - Web framework
- uvicorn - ASGI server
- anthropic/openai - LLM clients
- pymongo - MongoDB driver
- cryptography - Crypto operations
- pytest - Testing framework

### Step 4: Start MongoDB

**Using the provided script:**
```bash
./backend/start_mongodb.sh
```

**Or manually with Docker:**
```bash
docker run -d \
  -p 27017:27017 \
  --name chain-mongodb \
  mongo:latest
```

**Verify MongoDB is running:**
```bash
docker ps | grep mongo
```

You should see:
```
CONTAINER ID   IMAGE          ... STATUS         PORTS
abc123def456   mongo:latest   ... Up 5 seconds  0.0.0.0:27017->27017/tcp
```

---

## Configuration

### Create Environment File

```bash
# From project root
cp backend/.env.example .env
```

**IMPORTANT**: The `.env` file must be in the **project root**, not in `backend/`.

### Configure API Key

Edit `.env` with your preferred provider:

#### Option A: Anthropic Claude (Recommended)

```env
# Anthropic Configuration
ANTHROPIC_API_KEY=sk-ant-your_actual_key_here
LLM_PROVIDER=anthropic

# Optional: Specify model (default is haiku)
ANTHROPIC_MODEL=claude-3-haiku-20240307
# ANTHROPIC_MODEL=claude-3-sonnet-20240229  # Requires higher tier
# ANTHROPIC_MODEL=claude-3-opus-20240229     # Requires higher tier
```

**Get an API key:**
1. Visit https://console.anthropic.com/
2. Sign up for an account
3. Navigate to API Keys
4. Create new key
5. Copy key (starts with `sk-ant-`)

**Note**: Claude 3 Haiku is available on all API tiers, including free tier.

#### Option B: OpenAI

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your_actual_key_here
LLM_PROVIDER=openai

# Optional: Specify model (default is gpt-3.5-turbo)
OPENAI_MODEL=gpt-3.5-turbo
# OPENAI_MODEL=gpt-4
# OPENAI_MODEL=gpt-4-turbo
```

**Get an API key:**
1. Visit https://platform.openai.com/
2. Sign up for an account
3. Navigate to API keys
4. Create new secret key
5. Copy key (starts with `sk-`)

### Optional Configuration

```env
# MongoDB (usually don't need to change)
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=chain_of_truth

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Development
DEBUG=false
LOG_LEVEL=INFO
```

For detailed API setup instructions, see: [`backend/API_KEY_SETUP.md`](../../backend/API_KEY_SETUP.md)

---

## First Run

### Option 1: Quick Start (Recommended)

```bash
./start-simple.sh
```

This script:
- Checks Python installation
- Verifies dependencies
- Tests backend imports
- Starts the server
- Shows clear next steps

### Option 2: All-in-One (Requires tmux)

```bash
./start-all.sh
```

Starts backend and frontend in a single tmux session.

### Option 3: Manual Start

```bash
# Start backend
uv run python backend/main.py

# Server starts at http://localhost:8000
```

### What You'll See

```
╔═══════════════════════════════════════════════════════════╗
║   ██████╗██╗  ██╗ █████╗ ██╗███╗   ██╗                  ║
║  ██╔════╝██║  ██║██╔══██╗██║████╗  ██║                  ║
║  ██║     ███████║███████║██║██╔██╗ ██║                  ║
║  ██║     ██╔══██║██╔══██║██║██║╚██╗██║                  ║
║  ╚██████╗██║  ██║██║  ██║██║██║ ╚████║                  ║
║   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝                  ║
║                                                           ║
║  ╔═══════════════════════════════════════════════════╗  ║
║  ║         Chain of Truth - Backend Server          ║  ║
║  ╚═══════════════════════════════════════════════════╝  ║
╚═══════════════════════════════════════════════════════════╝

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Access the Application

Open your browser to:
```
http://localhost:8000
```

You should see the retro terminal interface load.

---

## Verification

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok"}
```

### 2. Test Character System

```bash
cd backend
uv run python test_character_system.py
```

Expected output:
```
============================================================
Testing Character System
============================================================

[1/8] Creating session...
✓ Session created: abc-123-def-456

[2/8] Testing ARCHIVIST chat...
✓ ARCHIVIST response received

... (more tests)

============================================================
✓ All tests passed!
============================================================
```

### 3. Run Full Test Suite

```bash
./test-backend.sh
```

You should see 150+ tests passing:
```
===== test session starts =====
collected 152 items

backend/test_blockchain.py .................... [ 13%]
backend/test_character_system.py ........ [ 18%]
backend/test_narrative_state.py ...... [ 22%]
... (more tests)

===== 152 passed in 2.34s =====
```

### 4. Check API Documentation

Visit:
```
http://localhost:8000/docs
```

You should see the Swagger UI with all API endpoints documented.

### 5. Test the Interface

In your browser at `http://localhost:8000`:

1. **Home module** loads with boot sequence
2. **Chain Viewer** shows first few blocks
3. **Crypto Vault** allows key generation
4. **Network Monitor** shows 50 stations
5. **Station Shell** accepts commands like `ls`
6. **Learning Guide** displays tutorial content

---

## Troubleshooting

### MongoDB Issues

**Problem**: `Connection refused` or MongoDB not starting

```bash
# Check if MongoDB container exists
docker ps -a | grep mongo

# If it exists but stopped, restart it
docker start chain-mongodb

# If it doesn't exist, create it
docker run -d -p 27017:27017 --name chain-mongodb mongo:latest

# Check logs if still failing
docker logs chain-mongodb
```

### API Key Issues

**Problem**: Characters not responding or API errors

**Checklist**:
1. ✓ Is `.env` in project root? (not backend/)
2. ✓ Does API key start with correct prefix?
   - Anthropic: `sk-ant-`
   - OpenAI: `sk-`
3. ✓ Is `LLM_PROVIDER` set correctly? (`anthropic` or `openai`)
4. ✓ Is the API key active on the provider dashboard?
5. ✓ Do you have credits/quota remaining?

**Test API key manually**:
```bash
# For Anthropic
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-haiku-20240307","max_tokens":10,"messages":[{"role":"user","content":"Hi"}]}'

# For OpenAI
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"Hi"}],"max_tokens":10}'
```

### Port Already in Use

**Problem**: `Address already in use: 8000`

```bash
# Stop all services
./stop-all.sh

# Or manually kill processes
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

### Import Errors

**Problem**: `ModuleNotFoundError` or import failures

```bash
# Reinstall dependencies
cd backend
uv pip install -r requirements.txt --force-reinstall

# Or use pip if uv has issues
python -m pip install -r requirements.txt
```

### Python Version Issues

**Problem**: Wrong Python version or not found

```bash
# Check version
python3 --version

# If < 3.12, install newer version
# Ubuntu/Debian:
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev

# macOS:
brew install python@3.12

# Update symlink
sudo ln -sf /usr/bin/python3.12 /usr/bin/python3
```

### Permission Issues

**Problem**: Docker permission denied

```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER
newgrp docker

# Or run with sudo (not recommended)
sudo docker run -d -p 27017:27017 --name chain-mongodb mongo:latest
```

### Frontend Not Loading

**Problem**: Blank page or connection errors

1. **Check backend is running**: `curl http://localhost:8000/health`
2. **Check browser console** for errors (F12)
3. **Clear browser cache** and hard reload (Ctrl+Shift+R)
4. **Try different browser** (Chrome, Firefox)
5. **Check firewall** isn't blocking localhost:8000

### Still Having Issues?

1. **Check logs**: Backend server output shows all errors
2. **Run diagnostics**: `./test-backend.sh`
3. **Verify environment**: `cat .env` (check API key is set)
4. **Check Docker**: `docker ps` (MongoDB should be running)
5. **Review documentation**: See [QUICKSTART.md](../../QUICKSTART.md)

---

## Next Steps

### For Players
- See [Gameplay Guide](gameplay-guide.md) for how to play
- Check [Tutorial](tutorial.md) for complete walkthrough
- Read [FAQ](faq.md) for common questions

### For Developers
- Read [Developer Guide](../developer/architecture.md)
- Check [API Reference](../developer/api-reference.md)
- Review [Testing Guide](../developer/testing-guide.md)

---

**Installation complete! Ready to discover the truth.**

*"The chain remembers everything. Your consciousness persists."*
