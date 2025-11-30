# Chain of Truth - Startup Guide

Quick reference for starting and managing the Chain of Truth development environment.

---

## 🚀 Quick Start

### Option 1: Start Everything (Recommended)
```bash
./start-all.sh
```
Starts both backend and frontend in a tmux session with beautiful logs.

### Option 2: Start Components Separately

**Terminal 1 - Backend:**
```bash
./start.sh
```

**Terminal 2 - Frontend:**
```bash
./start-frontend.sh
```

---

## 📋 Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `start-all.sh` | Start backend + frontend in tmux | `./start-all.sh` |
| `start.sh` | Start backend only | `./start.sh` |
| `start-frontend.sh` | Start frontend only | `./start-frontend.sh` |
| `stop-all.sh` | Stop all services | `./stop-all.sh` |

---

## 🎯 What Each Script Does

### `start-all.sh` - Complete System
- ✅ Creates tmux session named 'chain'
- ✅ Starts backend in window 0
- ✅ Starts frontend in window 1
- ✅ Shows color-coded logs
- ✅ Auto-attaches to session

**After starting:**
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

### `start.sh` - Backend Server
- ✅ Checks Python installation
- ✅ Creates/activates virtual environment
- ✅ Installs dependencies (uv or pip)
- ✅ Loads .env configuration
- ✅ Starts FastAPI server on port 8000
- ✅ Color-coded logs (errors, warnings, info)

**Pre-flight checks:**
- Python 3.x installed
- Virtual environment exists/created
- Dependencies installed
- Port 8000 available
- .env file exists

### `start-frontend.sh` - Frontend Server
- ✅ Checks Node.js installation
- ✅ Installs npm dependencies if needed
- ✅ Starts Vite dev server on port 5173
- ✅ Color-coded logs

**Pre-flight checks:**
- Node.js installed
- npm installed
- Dependencies installed
- Port 5173 available

### `stop-all.sh` - Stop Everything
- ✅ Kills tmux session
- ✅ Stops any remaining backend processes
- ✅ Stops any remaining frontend processes
- ✅ Verifies ports are clear

---

## 🎨 Log Color Coding

All scripts use color-coded logs for easy reading:

- 🔵 **CYAN** `ℹ` - Info messages
- 🟢 **GREEN** `✓` - Success messages
- 🟡 **YELLOW** `⚠` - Warnings
- 🔴 **RED** `✗` - Errors
- 🟣 **MAGENTA** `▸` - Step indicators

**Example output:**
```
ℹ Checking Python installation...
✓ Python found: Python 3.11.5
▸ Starting FastAPI backend server...
✓ BACKEND READY
```

---

## 🔧 Using tmux (start-all.sh)

### Essential tmux Commands

| Command | Description |
|---------|-------------|
| `tmux attach -t chain` | Attach to running session |
| `Ctrl+B` then `D` | Detach (keeps running in background) |
| `Ctrl+B` then `0` | Switch to backend window |
| `Ctrl+B` then `1` | Switch to frontend window |
| `Ctrl+C` (in window) | Stop that specific server |
| `tmux kill-session -t chain` | Stop everything |

### Workflow Example

```bash
# Start everything
./start-all.sh

# You're now in tmux session viewing backend logs
# Press Ctrl+B then 1 to see frontend logs
# Press Ctrl+B then 0 to go back to backend

# Detach to return to normal terminal (servers keep running)
# Press: Ctrl+B then D

# Do other work...

# Reattach to view logs
tmux attach -t chain

# When done, stop everything
./stop-all.sh
```

---

## 🐛 Troubleshooting

### "Port already in use"
```bash
# Stop all services
./stop-all.sh

# Try starting again
./start-all.sh
```

### "Python not found"
```bash
# Install Python 3
sudo apt install python3 python3-venv  # Linux
brew install python3                    # macOS
```

### "Node.js not found"
```bash
# Install Node.js from https://nodejs.org/
# Or use version manager:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install node
```

### "tmux not found"
```bash
# Install tmux
sudo apt install tmux     # Linux
brew install tmux         # macOS
```

### "Dependencies installation failed"
```bash
# Backend - try manual installation
source .venv/bin/activate
pip install -r requirements.txt

# Frontend - try manual installation
cd frontend
npm install
```

### "Backend starts but shows errors"
```bash
# Check .env file exists
ls -la backend/.env

# Edit and add API keys
nano backend/.env

# Required:
ANTHROPIC_API_KEY=your_actual_key_here
```

### View logs without starting
```bash
# Backend logs
tail -f backend/logs/*.log

# tmux session logs (if running)
tmux attach -t chain
```

---

## ⚙️ Configuration

### Backend (.env)
Located at: `backend/.env`

Required for LLM features:
```bash
ANTHROPIC_API_KEY=sk-ant-...
```

Optional:
```bash
# Use OpenAI instead
OPENAI_API_KEY=sk-...

# Server config
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Database (optional)
DATABASE_URL=sqlite:///./chain_of_truth.db
```

### Frontend (vite.config.js)
Located at: `frontend/vite.config.js`

Default port: 5173
Backend proxy configured automatically

---

## 📊 Service URLs

Once started, access:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:5173 | Main game interface |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Health Check** | http://localhost:8000/health | Server status |

---

## 🔍 Monitoring

### Check if services are running
```bash
# Check backend
curl http://localhost:8000/health

# Check frontend
curl http://localhost:5173

# Check processes
ps aux | grep uvicorn
ps aux | grep vite
```

### View real-time logs
```bash
# Backend (if running in tmux)
tmux attach -t chain
# Press Ctrl+B then 0

# Frontend (if running in tmux)
tmux attach -t chain
# Press Ctrl+B then 1
```

---

## 🚦 Development Workflow

### Standard Development Session
```bash
# 1. Start everything
./start-all.sh

# 2. Detach from tmux (Ctrl+B then D)

# 3. Open your editor
code .

# 4. Make changes - servers auto-reload

# 5. Check logs if needed
tmux attach -t chain

# 6. When done
./stop-all.sh
```

### Running Tests
```bash
# Backend tests (while servers are running or stopped)
source .venv/bin/activate
pytest backend/tests/ -v

# Frontend tests
cd frontend
npm test
```

### Database Reset (if needed)
```bash
# Stop servers
./stop-all.sh

# Delete database
rm backend/chain_of_truth.db

# Restart - will create fresh database
./start-all.sh
```

---

## 📝 Script Maintenance

All scripts follow DEVELOPMENT_PRINCIPLES.md:
- ✅ Simple, readable code
- ✅ Clear execution paths
- ✅ Helpful error messages
- ✅ Color-coded output for UX

To modify scripts, edit:
- `start.sh` - Backend startup
- `start-frontend.sh` - Frontend startup
- `start-all.sh` - Combined startup with tmux
- `stop-all.sh` - Shutdown procedures

---

## 💡 Tips

### Faster Restarts
```bash
# Just restart backend (faster than full restart)
tmux kill-window -t chain:backend
tmux new-window -t chain -n backend
tmux send-keys -t chain:backend "./start.sh" C-m
```

### Background Operation
```bash
# Start in background
./start-all.sh
# Immediately detach: Ctrl+B then D

# Work all day, servers running in background

# Check status anytime
tmux attach -t chain
```

### Multiple Environments
```bash
# Run different branches in different tmux sessions
tmux new-session -d -s chain-feature-x
tmux send-keys -t chain-feature-x:0 "./start.sh" C-m

tmux new-session -d -s chain-main
tmux send-keys -t chain-main:0 "./start.sh" C-m

# List sessions
tmux ls
```

---

## ✨ Features

### Auto-reload
- **Backend**: uvicorn watches for Python file changes
- **Frontend**: Vite watches for JS/CSS changes

### Smart Port Management
- Scripts automatically detect and clear ports
- No manual cleanup needed

### Environment Isolation
- Virtual environment for Python
- Node modules isolated in frontend/

### Dependency Management
- Auto-detects uv or falls back to pip
- Auto-installs missing dependencies

---

**For more information, see:**
- `docs/integration_plans/DEVELOPMENT_PRINCIPLES.md` - Development guidelines
- `docs/integration_plans/SYSTEM_ARCHITECTURE.md` - System overview
- `backend/README.md` - Backend documentation
- `frontend/README.md` - Frontend documentation
