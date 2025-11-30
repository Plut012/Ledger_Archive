#!/bin/bash

# Chain of Truth - Stop All Services Script

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info() { echo -e "${CYAN}ℹ${NC} $1"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠${NC} $1"; }

echo ""
log_info "Stopping Chain of Truth services..."
echo ""

# Kill tmux session if it exists
if tmux has-session -t chain 2>/dev/null; then
    log_info "Killing tmux session 'chain'..."
    tmux kill-session -t chain
    log_success "tmux session stopped"
fi

# Kill any remaining processes
log_info "Checking for remaining processes..."

# Kill backend
if pgrep -f "uvicorn backend.main:app" > /dev/null; then
    log_info "Stopping backend server..."
    pkill -f "uvicorn backend.main:app"
    log_success "Backend stopped"
fi

# Kill frontend
if pgrep -f "vite" > /dev/null; then
    log_info "Stopping frontend server..."
    pkill -f "vite"
    log_success "Frontend stopped"
fi

# Check ports
sleep 1

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    log_warning "Port 8000 still in use"
else
    log_success "Port 8000 clear"
fi

if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1; then
    log_warning "Port 5173 still in use"
else
    log_success "Port 5173 clear"
fi

echo ""
log_success "All services stopped"
echo ""
