#!/bin/bash
# Deploy Interstellar Archive Terminal locally with public URL

# DON'T exit on error - we want to handle errors gracefully
# set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ${NC}  $1"
}

log_success() {
    echo -e "${GREEN}✓${NC}  $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC}  $1"
}

log_error() {
    echo -e "${RED}✗${NC}  $1"
}

log_step() {
    echo -e "\n${BOLD}${BLUE}▶${NC} ${BOLD}$1${NC}"
}

log_substep() {
    echo -e "  ${DIM}→${NC} $1"
}

# Error handler that doesn't exit immediately
handle_error() {
    echo ""
    log_error "$1"
    if [ -n "$2" ]; then
        echo -e "  ${DIM}$2${NC}"
    fi
    echo ""
    echo -e "${YELLOW}Press Enter to exit...${NC}"
    read
    exit 1
}

# Banner
echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                           ║${NC}"
echo -e "${CYAN}║    ${BOLD}✦ INTERSTELLAR ARCHIVE TERMINAL DEPLOYER ✦${NC}${CYAN}       ║${NC}"
echo -e "${CYAN}║                                                           ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Log timestamp
log_info "Deployment started at $(date '+%Y-%m-%d %H:%M:%S')"

# Check if cloudflared is installed
log_step "Checking dependencies..."
log_substep "Looking for cloudflared..."

if ! command -v cloudflared &> /dev/null; then
    handle_error "cloudflared not found" \
"cloudflared is required to create a public tunnel.

Installation instructions:

  macOS:
    brew install cloudflare/cloudflare/cloudflared

  Linux (Debian/Ubuntu):
    wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    sudo dpkg -i cloudflared-linux-amd64.deb

  Linux (Generic):
    wget -O cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
    sudo mv cloudflared /usr/local/bin/
    sudo chmod +x /usr/local/bin/cloudflared

  Or visit: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"
fi

CLOUDFLARED_VERSION=$(cloudflared --version 2>&1 | head -1)
log_success "cloudflared found: $CLOUDFLARED_VERSION"

# Check for uv
log_substep "Looking for uv (Python package manager)..."
if ! command -v uv &> /dev/null; then
    handle_error "uv not found" \
"uv is required to run the Python backend.

Installation: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi
log_success "uv found: $(uv --version)"

# Get to project root
log_step "Locating project..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

if [ ! -f "$PROJECT_ROOT/backend/main.py" ]; then
    handle_error "Backend not found" "Could not find backend/main.py in $PROJECT_ROOT"
fi

cd "$PROJECT_ROOT"
log_success "Project root: $PROJECT_ROOT"

# Check if port 8000 is already in use
log_step "Checking port availability..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    log_warning "Port 8000 is already in use"
    echo ""
    EXISTING_PID=$(lsof -t -i:8000 | head -1)
    log_info "Process ID: $EXISTING_PID"

    echo -ne "${YELLOW}Kill existing process and continue? (y/n): ${NC}"
    read -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_substep "Stopping process $EXISTING_PID..."

        # Check what process this is before killing
        PROCESS_NAME=$(ps -p $EXISTING_PID -o comm= 2>/dev/null || echo "unknown")
        log_substep "Process is: $PROCESS_NAME"

        # Only kill if it looks like our server, otherwise warn
        if [[ "$PROCESS_NAME" == "python"* ]] || [[ "$PROCESS_NAME" == "uvicorn"* ]] || [[ "$PROCESS_NAME" == "uv"* ]]; then
            kill $EXISTING_PID 2>/dev/null || true
            sleep 2

            # Verify it's dead
            if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
                log_warning "Process didn't stop gracefully, forcing..."
                kill -9 $EXISTING_PID 2>/dev/null || true
                sleep 1
            fi

            log_success "Port 8000 is now available"
        else
            log_warning "Process '$PROCESS_NAME' doesn't look like our server"
            log_warning "Please close it manually and run this script again"
            handle_error "Cannot safely kill process" "Refusing to kill non-Python process to prevent data loss"
        fi
    else
        handle_error "Deployment cancelled" "Port 8000 must be available to continue"
    fi
else
    log_success "Port 8000 is available"
fi

# Create log directory
LOG_DIR="/tmp/archive-terminal-logs"
mkdir -p "$LOG_DIR"
SERVER_LOG="$LOG_DIR/server-$(date +%Y%m%d-%H%M%S).log"
TUNNEL_LOG="$LOG_DIR/tunnel-$(date +%Y%m%d-%H%M%S).log"

log_substep "Logs will be stored in: $LOG_DIR"

# Start backend server
log_step "Starting backend server..."
log_substep "Running: uv run python backend/main.py"
log_substep "Log file: $SERVER_LOG"

uv run python backend/main.py > "$SERVER_LOG" 2>&1 &
SERVER_PID=$!

log_success "Server started with PID: $SERVER_PID"

# Wait for server to be ready with progress indicator
log_substep "Waiting for server to be ready..."

SERVER_READY=false
for i in {1..15}; do
    if curl -s http://localhost:8000/ > /dev/null 2>&1; then
        SERVER_READY=true
        break
    fi

    # Check if process is still alive
    if ! kill -0 $SERVER_PID 2>/dev/null; then
        echo ""
        log_error "Server process died unexpectedly"
        echo ""
        echo -e "${YELLOW}Last 20 lines of server log:${NC}"
        echo -e "${DIM}─────────────────────────────────────────────${NC}"
        tail -20 "$SERVER_LOG" 2>/dev/null || echo "No logs available"
        echo -e "${DIM}─────────────────────────────────────────────${NC}"
        echo ""
        handle_error "Server failed to start" "Check the full logs: tail -f $SERVER_LOG"
    fi

    echo -ne "  ${DIM}→ Attempt $i/15...${NC}\r"
    sleep 1
done

if [ "$SERVER_READY" = false ]; then
    echo ""
    log_error "Server didn't respond after 15 seconds"
    echo ""
    echo -e "${YELLOW}Last 20 lines of server log:${NC}"
    echo -e "${DIM}─────────────────────────────────────────────${NC}"
    tail -20 "$SERVER_LOG" 2>/dev/null || echo "No logs available"
    echo -e "${DIM}─────────────────────────────────────────────${NC}"
    echo ""
    kill $SERVER_PID 2>/dev/null || true
    handle_error "Server startup timeout" "Check the full logs: tail -f $SERVER_LOG"
fi

echo "" # Clear the progress line
log_success "Server is responding on http://localhost:8000"

# Test server health
log_substep "Testing server health..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)
if [ "$HTTP_CODE" = "200" ]; then
    log_success "Server health check passed (HTTP $HTTP_CODE)"
else
    log_warning "Server returned HTTP $HTTP_CODE (expected 200, but continuing...)"
fi

# Start cloudflare tunnel
log_step "Creating Cloudflare Tunnel..."
log_substep "Running: cloudflared tunnel --url http://localhost:8000"
log_substep "Log file: $TUNNEL_LOG"

cloudflared tunnel --url http://localhost:8000 > "$TUNNEL_LOG" 2>&1 &
TUNNEL_PID=$!

log_success "Tunnel started with PID: $TUNNEL_PID"
log_substep "Waiting for public URL (this may take 10-30 seconds)..."

# Wait for URL to appear in logs
PUBLIC_URL=""
for i in {1..30}; do
    if grep -q "https://" "$TUNNEL_LOG" 2>/dev/null; then
        PUBLIC_URL=$(grep -oP 'https://[^\s]+\.trycloudflare\.com' "$TUNNEL_LOG" | head -1)
        if [ -n "$PUBLIC_URL" ]; then
            break
        fi
    fi

    # Check if tunnel process is still alive
    if ! kill -0 $TUNNEL_PID 2>/dev/null; then
        echo ""
        log_error "Tunnel process died unexpectedly"
        echo ""
        echo -e "${YELLOW}Last 20 lines of tunnel log:${NC}"
        echo -e "${DIM}─────────────────────────────────────────────${NC}"
        tail -20 "$TUNNEL_LOG" 2>/dev/null || echo "No logs available"
        echo -e "${DIM}─────────────────────────────────────────────${NC}"
        echo ""
        kill $SERVER_PID 2>/dev/null || true
        handle_error "Tunnel failed to start" "Check the full logs: tail -f $TUNNEL_LOG"
    fi

    echo -ne "  ${DIM}→ Waiting for URL... ($i/30 seconds)${NC}\r"
    sleep 1
done

echo "" # Clear the progress line

if [ -z "$PUBLIC_URL" ]; then
    echo ""
    log_error "Failed to get public URL after 30 seconds"
    echo ""
    echo -e "${YELLOW}Last 30 lines of tunnel log:${NC}"
    echo -e "${DIM}─────────────────────────────────────────────${NC}"
    tail -30 "$TUNNEL_LOG" 2>/dev/null || echo "No logs available"
    echo -e "${DIM}─────────────────────────────────────────────${NC}"
    echo ""
    kill $SERVER_PID 2>/dev/null || true
    kill $TUNNEL_PID 2>/dev/null || true
    handle_error "Tunnel URL not found" "Check the full logs: tail -f $TUNNEL_LOG"
fi

log_success "Public URL obtained!"

# Test tunnel connectivity
log_substep "Testing public URL connectivity..."
sleep 2  # Give it a moment to fully initialize

TUNNEL_TEST=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$PUBLIC_URL" 2>/dev/null || echo "000")
if [ "$TUNNEL_TEST" = "200" ]; then
    log_success "Tunnel is publicly accessible (HTTP $TUNNEL_TEST)"
elif [ "$TUNNEL_TEST" = "000" ]; then
    log_warning "Could not test tunnel (timeout or network error)"
else
    log_warning "Tunnel returned HTTP $TUNNEL_TEST (may still work)"
fi

# SUCCESS BANNER
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}║              ${BOLD}✓ DEPLOYMENT SUCCESSFUL!${NC}${GREEN}                   ║${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Display URLs in a nice box
echo -e "${BOLD}${CYAN}┌───────────────────────────────────────────────────────────┐${NC}"
echo -e "${BOLD}${CYAN}│${NC} ${BOLD}🌍 YOUR PUBLIC SHAREABLE LINK:${NC}                          ${BOLD}${CYAN}│${NC}"
echo -e "${BOLD}${CYAN}└───────────────────────────────────────────────────────────┘${NC}"
echo ""
echo -e "   ${BOLD}${GREEN}$PUBLIC_URL${NC}"
echo ""
echo -e "${DIM}   Copy and share this link with anyone!${NC}"
echo -e "${DIM}   The link is publicly accessible from anywhere in the world.${NC}"
echo ""

echo -e "${BOLD}${BLUE}┌───────────────────────────────────────────────────────────┐${NC}"
echo -e "${BOLD}${BLUE}│${NC} ${BOLD}💻 LOCAL ACCESS:${NC}                                          ${BOLD}${BLUE}│${NC}"
echo -e "${BOLD}${BLUE}└───────────────────────────────────────────────────────────┘${NC}"
echo ""
echo -e "   ${BOLD}http://localhost:8000${NC}"
echo ""

echo -e "${BOLD}${YELLOW}┌───────────────────────────────────────────────────────────┐${NC}"
echo -e "${BOLD}${YELLOW}│${NC} ${BOLD}📊 MONITORING & LOGS:${NC}                                    ${BOLD}${YELLOW}│${NC}"
echo -e "${BOLD}${YELLOW}└───────────────────────────────────────────────────────────┘${NC}"
echo ""
echo -e "   ${DIM}Server log:${NC}  tail -f $SERVER_LOG"
echo -e "   ${DIM}Tunnel log:${NC}  tail -f $TUNNEL_LOG"
echo -e "   ${DIM}All logs:${NC}    ls -lh $LOG_DIR"
echo ""

echo -e "${BOLD}${CYAN}┌───────────────────────────────────────────────────────────┐${NC}"
echo -e "${BOLD}${CYAN}│${NC} ${BOLD}ℹ  PROCESS INFO:${NC}                                          ${BOLD}${CYAN}│${NC}"
echo -e "${BOLD}${CYAN}└───────────────────────────────────────────────────────────┘${NC}"
echo ""
echo -e "   ${DIM}Server PID:${NC}   $SERVER_PID"
echo -e "   ${DIM}Tunnel PID:${NC}   $TUNNEL_PID"
echo -e "   ${DIM}Started at:${NC}   $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Save PIDs and URLs for cleanup
echo "$SERVER_PID" > /tmp/archive-server.pid
echo "$TUNNEL_PID" > /tmp/cloudflared.pid
echo "$PUBLIC_URL" > /tmp/archive-public-url.txt

echo -e "${BOLD}${RED}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${RED}║${NC}  ${BOLD}Press Ctrl+C to stop the deployment${NC}                      ${BOLD}${RED}║${NC}"
echo -e "${BOLD}${RED}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Trap Ctrl+C and cleanup
cleanup() {
    echo ""
    echo ""
    log_step "Shutting down..."

    log_substep "Stopping tunnel (PID: $TUNNEL_PID)..."
    kill $TUNNEL_PID 2>/dev/null || true
    sleep 1
    kill -9 $TUNNEL_PID 2>/dev/null || true
    log_success "Tunnel stopped"

    log_substep "Stopping server (PID: $SERVER_PID)..."
    kill $SERVER_PID 2>/dev/null || true
    sleep 1
    kill -9 $SERVER_PID 2>/dev/null || true
    log_success "Server stopped"

    log_substep "Cleaning up..."
    rm -f /tmp/archive-server.pid /tmp/cloudflared.pid /tmp/archive-public-url.txt

    echo ""
    log_success "Deployment stopped cleanly"
    echo ""
    echo -e "${DIM}Logs preserved at: $LOG_DIR${NC}"
    echo ""

    # Don't exit - return to shell prompt
    return 0
}

trap cleanup INT TERM

# Keep script running and show live connection count if possible
log_info "Monitoring deployment... (Ctrl+C to stop)"
echo ""

# Keep script running
wait
