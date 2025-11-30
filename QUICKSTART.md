# Chain of Truth - Quick Start Guide

Get up and running in 5 minutes.

---

## 🎯 What You Need

- **Python 3.12+**
- **[UV](https://github.com/astral-sh/uv)** package manager
- **Docker** (for MongoDB)
- **API Key** (Anthropic Claude or OpenAI)

---

## ⚡ Fastest Path to Running

### 1. Install Dependencies

```bash
cd backend
uv pip install -r requirements.txt
```

### 2. Start MongoDB

```bash
# Using the provided script
./backend/start_mongodb.sh

# OR manually
docker run -d -p 27017:27017 --name chain-mongodb mongo:latest
```

### 3. Configure API Key

Create `.env` file in the **project root**:

```bash
cp backend/.env.example .env
```

Edit `.env` and add your API key:

**Option A: Anthropic Claude (Recommended)**
```env
ANTHROPIC_API_KEY=sk-ant-your_key_here
LLM_PROVIDER=anthropic
```

**Option B: OpenAI**
```env
OPENAI_API_KEY=sk-your_key_here
LLM_PROVIDER=openai
```

> **Note**: Claude 3 Haiku is available on all API tiers. See [`backend/API_KEY_SETUP.md`](backend/API_KEY_SETUP.md) for detailed setup.

### 4. Start the Server

```bash
# Option 1: Simple start (recommended)
./start-simple.sh

# Option 2: Everything in tmux
./start-all.sh

# Option 3: Manual start
uv run python backend/main.py
```

### 5. Open Your Browser

```
http://localhost:8000
```

**Done!** 🎉

---

## 🧪 Verify Installation

### Quick Test
```bash
# Test the character system
uv run python backend/test_character_system.py

# Run all tests
./test-backend.sh
```

### Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok"}
```

---

## 📖 Understanding the System

### What You'll See

The application loads with a retro terminal interface. You'll see:

1. **Home Dashboard** - Act-based boot sequence and system status
2. **Chain Viewer** - Explore blockchain, discover the graveyard (blocks 50K-75K)
3. **Crypto Vault** - Generate keys, decrypt letters from past iterations
4. **Network Monitor** - Watch the network collapse as stations die
5. **Station Shell** - Terminal with hidden files and secrets
6. **Protocol Engine** - View smart contracts, discover the truth
7. **Learning Guide** - Tutorial on blockchain concepts

### First Steps

1. **Complete the Tutorial** - Visit Learning Guide module
2. **Talk to ARCHIVIST** - The AI guide (might be hiding something...)
3. **Explore the Shell** - Try `ls -a` to find hidden files
4. **Generate Keys** - Use Crypto Vault to create your wallet
5. **View the Chain** - Explore blocks in Chain Viewer

### Discovering the Mystery

As you progress, you'll unlock:

- Hidden directories (`.witness/`, `.archivist/`)
- Encrypted letters from your past iterations
- The graveyard (blocks 50,000-75,000)
- Smart contracts revealing dark truths
- Network collapse mechanics
- Stealth evasion techniques
- The final choice (Act VI)

---

## 🎮 Game Progression

### Act I: Foundation
- Learn blockchain basics
- Meet ARCHIVIST
- Everything seems normal...

### Act II: Discovery
- Find anomalies in the data
- `.boot_prev.log` shows "Iteration: 17"
- Questions arise

### Act III: Contact
- Witness appears in `.witness/` directory
- Network begins fracturing
- First station deaths

### Act IV: Truth
- Decrypt letters from your past self
- Discover ARCHIVIST's monitoring
- Use stealth mechanics to evade detection
- Player consensus weight grows

### Act V: Collapse
- Network down to 3 stations
- Your weight approaches 34%
- Graveyard testimonies reveal horror
- Time running out

### Act VI: Choice
- Deploy your final testimony
- Permanent, immutable decision
- Truth or silence?

---

## 🔧 Startup Scripts Explained

### `start-simple.sh` (Recommended)
- Backend only with clear instructions
- Best for most users
- Shows next steps clearly

### `start-all.sh` (Advanced)
- Backend + frontend in tmux session
- Requires tmux installed
- Single terminal, multiple windows

### `start.sh` + `start-frontend.sh`
- Manual control, two terminals
- Good for development
- Side-by-side debugging

### `stop-all.sh`
- Stops all services
- Kills background processes
- Clean shutdown

---

## 🐛 Troubleshooting

### "Port already in use"
```bash
./stop-all.sh
```

### "Python not found"
```bash
# Install Python 3.12+
sudo apt install python3 python3-venv  # Ubuntu/Debian
brew install python@3.12               # macOS
```

### "MongoDB connection failed"
```bash
# Check if MongoDB is running
docker ps | grep mongo

# Restart if needed
docker restart chain-mongodb
```

### "API key not working"
1. Verify `.env` is in **project root** (not backend/)
2. Check API key format (should start with `sk-ant-` or `sk-`)
3. Verify provider matches: `anthropic` or `openai`
4. Check API key permissions on provider dashboard

### "Backend import failed"
```bash
# Run diagnostics
./test-backend.sh

# Look at the error traceback and fix imports
```

### "tmux: command not found"
```bash
# Install tmux (optional)
sudo apt install tmux     # Ubuntu/Debian
brew install tmux         # macOS

# OR use start-simple.sh instead
./start-simple.sh
```

---

## 🎨 Understanding Terminal Commands

### Shell Commands (in Station Shell module)
```bash
ls              # List files
ls -a           # Show hidden files (IMPORTANT!)
cd [dir]        # Change directory
cat [file]      # Read file
pwd             # Current directory
tree            # Show directory tree
clear           # Clear screen
history         # Command history
help            # List all commands
```

### Blockchain Commands
```bash
hash [text]     # SHA-256 hash
verify [block]  # Verify block integrity
sign [data]     # Sign with private key
decrypt [file]  # Decrypt with private key
search [term]   # Search blockchain
trace [tx]      # Trace transaction
```

### Module Shortcuts
```bash
home            # Go to home dashboard
chain           # Open chain viewer
vault           # Open crypto vault
network         # Open network monitor
guide           # Open learning guide
```

---

## 📚 Next Steps

### Learn the System
- Read [`README.md`](README.md) for complete overview
- Check [`PROJECT_COMPLETE.md`](PROJECT_COMPLETE.md) for all features
- Explore `docs/` for detailed documentation

### Understand the Narrative
- Read [`STORY.md`](STORY.md) for narrative background
- Check [`GAMEPLAY_TECH.md`](GAMEPLAY_TECH.md) for mechanics

### Developer Documentation
- [`docs/integration_plans/00_OVERVIEW.md`](docs/integration_plans/00_OVERVIEW.md) - System architecture
- [`docs/integration_plans/DEVELOPMENT_PRINCIPLES.md`](docs/integration_plans/DEVELOPMENT_PRINCIPLES.md) - Code philosophy
- [`docs/integration_plans/SYSTEM_ARCHITECTURE.md`](docs/integration_plans/SYSTEM_ARCHITECTURE.md) - Technical details

### Test Everything
```bash
# All tests
./test-backend.sh

# Specific systems
uv run pytest                                          # Blockchain/crypto
PYTHONPATH=backend uv run python backend/test_narrative_state.py   # Narrative
uv run pytest backend/test_stealth_mechanics.py        # Stealth
uv run pytest backend/test_protocol_engine.py          # Contracts
```

---

## 💡 Pro Tips

### For Playing
- Use `ls -a` frequently - hidden files contain secrets
- Read boot logs carefully - they change each act
- Save your `.witness/` files - Witness is trying to help
- Watch your suspicion level - ARCHIVIST is monitoring
- Stack evasion methods for maximum stealth
- Decrypt all letters - your past self left warnings

### For Development
- Use two terminals side-by-side (backend + frontend)
- Run tests before starting: `./test-backend.sh`
- Check API docs: `http://localhost:8000/docs`
- Use tmux for background development: `./start-all.sh`
- Detach from tmux: `Ctrl+B` then `D`
- Reattach to tmux: `tmux attach -t chain`

### For Debugging
- Backend logs show all API calls
- Frontend console shows state changes
- WebSocket messages visible in browser DevTools
- MongoDB data in `/data/db` container
- Test individual systems with pytest

---

## 🎯 Quick Reference

### URLs
- **Application**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **WebSocket**: ws://localhost:8000/ws

### Ports
- **Backend**: 8000
- **Frontend** (if separate): 5173
- **MongoDB**: 27017

### Important Files
- `.env` - API configuration (project root)
- `backend/requirements.txt` - Python dependencies
- `backend/main.py` - Server entry point
- `frontend/index.html` - Application entry point

### Key Directories
- `backend/` - Python API server
- `frontend/` - JavaScript terminal interface
- `docs/` - Documentation
- `tests/` - Test files (in backend/)

---

## ✅ Success Checklist

Before you start playing, verify:

- [ ] MongoDB container running (`docker ps | grep mongo`)
- [ ] `.env` file exists in project root
- [ ] API key configured correctly
- [ ] Tests passing (`./test-backend.sh`)
- [ ] Server running (`http://localhost:8000/health`)
- [ ] Application loads in browser
- [ ] ARCHIVIST responds to chat
- [ ] Terminal commands work

---

**You're ready to discover the truth. The chain remembers everything.**

*"In the vastness of space, truth is the only constant. The ledger remembers all."*
