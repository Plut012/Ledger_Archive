# Chain of Truth - Quick Start Guide

## 🚀 Easiest Way to Start

### Option 1: Simple Start (Recommended - No tmux needed)
```bash
./start-simple.sh
```
Starts the backend. Open a second terminal for frontend if needed.

### Option 2: Individual Components
**Terminal 1 - Backend:**
```bash
./start.sh
```

**Terminal 2 - Frontend (optional):**
```bash
./start-frontend.sh
```

### Option 3: Everything Together (Requires tmux)
```bash
./start-all.sh
```
Uses tmux to run both in one terminal. You'll need to install tmux first:
```bash
sudo apt install tmux     # Ubuntu/Debian
brew install tmux         # macOS
```

---

## ❓ Which Script to Use?

| Script | What it does | When to use |
|--------|-------------|-------------|
| `start-simple.sh` | Backend only, clear instructions | **Most people, easiest** |
| `start.sh` | Backend only | You want just the API |
| `start-frontend.sh` | Frontend only | Backend already running |
| `start-all.sh` | Both with tmux | You know tmux and want one terminal |
| `stop-all.sh` | Stop everything | Cleanup |

---

## 🎯 What You'll See

### Successful Start
```
╔═══════════════════════════════════════════════════════════╗
║   ██████╗██╗  ██╗ █████╗ ██╗███╗   ██╗                  ║
║  ...                                                      ║
╚═══════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PRE-FLIGHT CHECKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▸ Checking Python installation...
✓ Python found: Python 3.13.7
▸ Checking uv package manager...
✓ uv found: uv 0.8.23
✓ Backend imports OK

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✓ BACKEND READY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

API Documentation:  http://localhost:8000/docs
Health Check:       http://localhost:8000/health
Frontend:           http://localhost:5173
```

### If There's an Error
The script will show you exactly what's wrong:
```
✗ Backend import failed!

ℹ Running diagnostic...
Traceback (most recent call last):
  ...
  ImportError: cannot import name 'Network' from 'network'

✗ Please fix the import errors above before starting
```

---

## 🐛 Common Issues

### "start-all.sh closes my terminal"
**Cause:** tmux is not installed
**Fix:** Use `./start-simple.sh` instead, or install tmux:
```bash
sudo apt install tmux
```

### "Backend import failed"
**Cause:** Python code has errors
**Fix:** Look at the error message and fix the imports in your backend code

### "Port already in use"
**Fix:** Stop existing services:
```bash
./stop-all.sh
```

### "Python not found"
**Fix:** Install Python 3.12+:
```bash
sudo apt install python3 python3-venv
```

---

## 🎨 Understanding the Logs

All scripts use color-coded logs:

- 🔵 **ℹ** Info (cyan)
- 🟢 **✓** Success (green)
- 🟡 **⚠** Warning (yellow)
- 🔴 **✗** Error (red)
- 🟣 **▸** Step in progress (magenta)

---

## 🔧 Quick Commands

```bash
# Start (easiest)
./start-simple.sh

# Stop everything
./stop-all.sh

# Test backend health
curl http://localhost:8000/health

# View API docs
open http://localhost:8000/docs  # macOS
xdg-open http://localhost:8000/docs  # Linux
```

---

## 📚 More Documentation

- **Detailed startup guide:** `STARTUP_GUIDE.md`
- **Development principles:** `docs/integration_plans/DEVELOPMENT_PRINCIPLES.md`
- **System architecture:** `docs/integration_plans/SYSTEM_ARCHITECTURE.md`
- **Implementation status:** `docs/integration_plans/COMPLETE_IMPLEMENTATION_STATUS.md`

---

## 💡 Pro Tips

### For Development
Use two terminals side-by-side:
- Left: Backend (`./start.sh`)
- Right: Frontend (`./start-frontend.sh`)

Both will auto-reload when you save files.

### For Debugging
Run the test script first:
```bash
./test-backend.sh
```
Shows exactly what's wrong before starting.

### For Background Running
If you have tmux installed:
```bash
./start-all.sh
# Press Ctrl+B then D to detach
# Servers keep running in background
```

---

**Need help? The scripts show clear error messages and suggestions!**
