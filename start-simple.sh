#!/bin/bash

# Chain of Truth - Simple Startup (No tmux required)
# Starts backend only, with instructions for frontend

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
║         OF TRUTH - Simple Startup (Backend Only)         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"
echo ""

log_info "Starting backend server..."
echo ""
log_info "To also run the frontend, open a second terminal and run:"
echo -e "  ${YELLOW}./start-frontend.sh${NC}"
echo ""
echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Start backend
./start.sh
