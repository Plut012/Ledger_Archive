╔═══════════════════════════════════════════════════════════╗
║              CHAIN OF TRUTH - HOW TO START                ║
╚═══════════════════════════════════════════════════════════╝

EASIEST WAY:
  ./start-simple.sh

This starts the backend. Open another terminal for frontend if you want.

OTHER OPTIONS:
  ./start.sh              Backend only
  ./start-frontend.sh     Frontend only
  ./start-all.sh          Both (needs tmux)
  ./stop-all.sh           Stop everything

FIRST TIME SETUP:
  1. Make sure Python 3.12+ is installed
  2. Run: ./start-simple.sh
  3. Follow any instructions shown

HELP:
  See QUICK_START.md for more details
  See STARTUP_GUIDE.md for full documentation

TROUBLESHOOTING:
  - "start-all closes terminal" → Use ./start-simple.sh instead
  - "Backend import failed" → Fix the Python errors shown
  - "Port in use" → Run ./stop-all.sh first
