#!/bin/bash
# Run Interstellar Archive Terminal locally

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🚀 INTERSTELLAR ARCHIVE TERMINAL 🚀     ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
echo ""

# Get to project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

# Check if port 8000 is in use
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠  Port 8000 is already in use${NC}"
    EXISTING_PID=$(lsof -t -i:8000 | head -1)
    PROCESS_NAME=$(ps -p $EXISTING_PID -o comm= 2>/dev/null || echo "unknown")
    echo -e "   Process: ${PROCESS_NAME} (PID: ${EXISTING_PID})"
    echo ""
    echo -ne "${YELLOW}Stop it and continue? (y/n): ${NC}"
    read -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [[ "$PROCESS_NAME" == "python"* ]] || [[ "$PROCESS_NAME" == "uvicorn"* ]] || [[ "$PROCESS_NAME" == "uv"* ]]; then
            kill $EXISTING_PID 2>/dev/null || true
            sleep 1
            echo -e "${GREEN}✓${NC} Port cleared"
        else
            echo -e "${RED}✗${NC} Cannot safely kill '$PROCESS_NAME'"
            echo "   Please close it manually and run this script again"
            exit 1
        fi
    else
        echo -e "${YELLOW}Exiting...${NC}"
        exit 0
    fi
fi

echo -e "${BLUE}▶${NC} Starting server..."
echo ""

# Start server in background
uv run python backend/main.py > /dev/null 2>&1 &
SERVER_PID=$!

# Save PID for stop script
echo $SERVER_PID > /tmp/archive-server.pid

# Wait for server to be ready
echo -e "${BLUE}⏳${NC} Waiting for server to start..."
for i in {1..10}; do
    if curl -s http://localhost:8000/ > /dev/null 2>&1; then
        break
    fi

    # Check if process died
    if ! kill -0 $SERVER_PID 2>/dev/null; then
        echo -e "${RED}✗${NC} Server failed to start"
        rm -f /tmp/archive-server.pid
        exit 1
    fi

    sleep 1
done

# Test if server is responding
if ! curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo -e "${RED}✗${NC} Server not responding after 10 seconds"
    kill $SERVER_PID 2>/dev/null || true
    rm -f /tmp/archive-server.pid
    exit 1
fi

echo -e "${GREEN}✓${NC} Server is running!"
echo ""

# Open browser
echo -e "${BLUE}▶${NC} Opening browser..."
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:8000 2>/dev/null &
elif command -v open > /dev/null; then
    open http://localhost:8000 2>/dev/null &
else
    echo -e "${YELLOW}⚠${NC}  Could not auto-open browser"
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         ✓ READY TO EXPLORE!               ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${BLUE}Local URL:${NC}     http://localhost:8000"
echo -e "  ${BLUE}Server PID:${NC}    $SERVER_PID"
echo ""
echo -e "${RED}╔═══════════════════════════════════════════╗${NC}"
echo -e "${RED}║  Press Ctrl+C to stop the server          ║${NC}"
echo -e "${RED}╚═══════════════════════════════════════════╝${NC}"
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo ""
    echo -e "${BLUE}▶${NC} Shutting down..."
    kill $SERVER_PID 2>/dev/null || true
    sleep 1
    kill -9 $SERVER_PID 2>/dev/null || true
    rm -f /tmp/archive-server.pid
    echo -e "${GREEN}✓${NC} Server stopped"
    echo ""
}

trap cleanup INT TERM

# Wait for Ctrl+C
wait $SERVER_PID
