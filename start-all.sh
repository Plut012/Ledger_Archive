#!/bin/bash

# Chain of Truth - Complete Startup Script
# Starts both backend and frontend in parallel with tmux

# Don't exit on error - we want to show helpful messages
set +e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

log_info() { echo -e "${CYAN}ℹ${NC} $1"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }

# Banner
clear
echo -e "${BOLD}${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██████╗██╗  ██╗ █████╗ ██╗███╗   ██╗                  ║
║  ██╔════╝██║  ██║██╔══██╗██║████╗  ██║                  ║
║  ██║     ███████║███████║██║██╔██╗ ██║                  ║
║  ██║     ██╔══██║██╔══██║██║██║╚██╗██║                  ║
║  ╚██████╗██║  ██║██║  ██║██║██║ ╚████║                  ║
║   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝                  ║
║                                                           ║
║         OF TRUTH - Complete System Startup               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"
echo ""

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    log_error "tmux is required to run backend and frontend together"
    echo ""
    log_info "Install tmux with one of these commands:"
    echo -e "  ${CYAN}sudo apt install tmux${NC}     # Ubuntu/Debian"
    echo -e "  ${CYAN}brew install tmux${NC}         # macOS"
    echo -e "  ${CYAN}sudo yum install tmux${NC}     # CentOS/RHEL"
    echo ""
    log_info "OR run backend and frontend in separate terminals:"
    echo ""
    echo -e "  ${YELLOW}Terminal 1:${NC} ./start.sh"
    echo -e "  ${YELLOW}Terminal 2:${NC} ./start-frontend.sh"
    echo ""
    echo -e "${YELLOW}Press any key to exit...${NC}"
    read -n 1 -s
    exit 0
fi

# Check if session already exists
if tmux has-session -t chain 2>/dev/null; then
    log_info "Existing 'chain' tmux session found"
    echo ""
    echo "Options:"
    echo "  1) Kill existing session and start fresh"
    echo "  2) Attach to existing session"
    echo "  3) Cancel"
    echo ""
    read -p "Choice (1/2/3): " choice

    case $choice in
        1)
            log_info "Killing existing session..."
            tmux kill-session -t chain
            log_success "Session killed"
            ;;
        2)
            log_info "Attaching to existing session..."
            echo ""
            echo -e "${YELLOW}Commands:${NC}"
            echo "  Ctrl+B then D - Detach from session"
            echo "  Ctrl+B then 0 - Switch to backend window"
            echo "  Ctrl+B then 1 - Switch to frontend window"
            echo "  Ctrl+C in window - Stop that server"
            echo ""
            sleep 2
            tmux attach-session -t chain
            exit 0
            ;;
        *)
            log_info "Cancelled"
            exit 0
            ;;
    esac
fi

log_info "Starting Chain of Truth in tmux session..."
echo ""

# Create new tmux session
tmux new-session -d -s chain -n backend

# Start backend in first window
log_info "Launching backend server..."
tmux send-keys -t chain:backend "./start.sh" C-m

# Wait a moment for backend to initialize
sleep 2

# Create new window for frontend
tmux new-window -t chain -n frontend

# Start frontend in second window
log_info "Launching frontend server..."
tmux send-keys -t chain:frontend "./start-frontend.sh" C-m

# Wait for services to start
log_info "Waiting for services to initialize..."
sleep 3

# Show status
echo ""
echo -e "${BOLD}${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}${GREEN}  ✓ CHAIN OF TRUTH STARTED${NC}"
echo -e "${BOLD}${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${CYAN}Services running in tmux session 'chain':${NC}"
echo ""
echo -e "  ${GREEN}✓${NC} Backend:  http://localhost:8000"
echo -e "  ${GREEN}✓${NC} Frontend: http://localhost:5173"
echo -e "  ${GREEN}✓${NC} API Docs: http://localhost:8000/docs"
echo ""
echo -e "${BOLD}${YELLOW}tmux Commands:${NC}"
echo -e "  ${CYAN}tmux attach -t chain${NC}      - Attach to session (view logs)"
echo -e "  ${CYAN}Ctrl+B then D${NC}             - Detach from session (keeps running)"
echo -e "  ${CYAN}Ctrl+B then 0${NC}             - Switch to backend window"
echo -e "  ${CYAN}Ctrl+B then 1${NC}             - Switch to frontend window"
echo -e "  ${CYAN}tmux kill-session -t chain${NC} - Stop everything"
echo ""
echo -e "${BOLD}${YELLOW}Quick Actions:${NC}"
echo -e "  ${CYAN}./stop-all.sh${NC}             - Stop all services"
echo -e "  ${CYAN}./start-all.sh${NC}            - Restart all services"
echo ""

# Attach to session
echo -e "${YELLOW}Attaching to tmux session in 3 seconds...${NC}"
echo -e "${YELLOW}(Press Ctrl+C now to cancel)${NC}"
sleep 3

tmux attach-session -t chain
