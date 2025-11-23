#!/bin/bash
# Stop the deployed server and tunnel

# Don't exit on error - we want to try all cleanup steps
# set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
DIM='\033[2m'
NC='\033[0m'

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════${NC}"
echo -e "${YELLOW}  Stopping Archive Terminal Deployment${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════${NC}"
echo ""

STOPPED_SOMETHING=false

# Kill server if PID file exists
if [ -f /tmp/archive-server.pid ]; then
    SERVER_PID=$(cat /tmp/archive-server.pid)
    if kill -0 $SERVER_PID 2>/dev/null; then
        echo -e "${DIM}→ Stopping server (PID: $SERVER_PID)...${NC}"
        kill $SERVER_PID 2>/dev/null || true
        sleep 1
        # Force kill if still running
        if kill -0 $SERVER_PID 2>/dev/null; then
            kill -9 $SERVER_PID 2>/dev/null || true
        fi
        echo -e "${GREEN}✓${NC} Server stopped"
        STOPPED_SOMETHING=true
    else
        echo -e "${DIM}→ Server PID file exists but process is not running${NC}"
    fi
    rm -f /tmp/archive-server.pid
else
    echo -e "${DIM}→ No server PID file found${NC}"
fi

# Kill tunnel if PID file exists
if [ -f /tmp/cloudflared.pid ]; then
    TUNNEL_PID=$(cat /tmp/cloudflared.pid)
    if kill -0 $TUNNEL_PID 2>/dev/null; then
        echo -e "${DIM}→ Stopping tunnel (PID: $TUNNEL_PID)...${NC}"
        kill $TUNNEL_PID 2>/dev/null || true
        sleep 1
        # Force kill if still running
        if kill -0 $TUNNEL_PID 2>/dev/null; then
            kill -9 $TUNNEL_PID 2>/dev/null || true
        fi
        echo -e "${GREEN}✓${NC} Tunnel stopped"
        STOPPED_SOMETHING=true
    else
        echo -e "${DIM}→ Tunnel PID file exists but process is not running${NC}"
    fi
    rm -f /tmp/cloudflared.pid
else
    echo -e "${DIM}→ No tunnel PID file found${NC}"
fi

# Fallback: Check for Python processes on port 8000 (SAFELY)
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    EXISTING_PID=$(lsof -t -i:8000 | head -1)
    PROCESS_NAME=$(ps -p $EXISTING_PID -o comm= 2>/dev/null || echo "unknown")

    echo -e "${YELLOW}⚠${NC}  Found process on port 8000: $PROCESS_NAME (PID: $EXISTING_PID)"

    # Only kill if it's a Python/uvicorn process (not browsers!)
    if [[ "$PROCESS_NAME" == "python"* ]] || [[ "$PROCESS_NAME" == "uvicorn"* ]] || [[ "$PROCESS_NAME" == "uv"* ]]; then
        echo -e "${DIM}→ Stopping orphaned Python process...${NC}"
        kill $EXISTING_PID 2>/dev/null || true
        sleep 1
        kill -9 $EXISTING_PID 2>/dev/null || true
        echo -e "${GREEN}✓${NC} Cleaned up port 8000"
        STOPPED_SOMETHING=true
    else
        echo -e "${RED}⚠${NC}  Refusing to kill '$PROCESS_NAME' - please close it manually"
    fi
fi

# Kill any cloudflared tunnel processes (by name, not port)
if pgrep -f "cloudflared tunnel" >/dev/null 2>&1 ; then
    echo -e "${DIM}→ Stopping any stray cloudflared tunnels...${NC}"
    pkill -f "cloudflared tunnel" 2>/dev/null || true
    sleep 1
    echo -e "${GREEN}✓${NC} Cleaned up cloudflared processes"
    STOPPED_SOMETHING=true
fi

# Clean up URL file
rm -f /tmp/archive-public-url.txt

echo ""
if [ "$STOPPED_SOMETHING" = true ]; then
    echo -e "${GREEN}✓ Deployment stopped successfully${NC}"
else
    echo -e "${YELLOW}ℹ  No running deployment found${NC}"
fi
echo ""
