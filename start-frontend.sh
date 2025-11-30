#!/bin/bash

# Chain of Truth - Frontend Startup Script
# Starts the Vite development server

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

log_info() { echo -e "${CYAN}ℹ${NC} $1"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }
log_step() { echo -e "${MAGENTA}▸${NC} $1"; }

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    log_error "frontend/ directory not found!"
    exit 1
fi

echo -e "${BOLD}${CYAN}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  CHAIN OF TRUTH - Frontend Startup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${NC}"

# Check Node.js
log_step "Checking Node.js installation..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    log_success "Node.js found: $NODE_VERSION"
else
    log_error "Node.js not found!"
    log_info "Please install Node.js: https://nodejs.org/"
    exit 1
fi

# Check npm
log_step "Checking npm installation..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    log_success "npm found: v$NPM_VERSION"
else
    log_error "npm not found!"
    exit 1
fi

# Check if node_modules exists
log_step "Checking dependencies..."
if [ ! -d "frontend/node_modules" ]; then
    log_warning "node_modules not found - installing dependencies..."
    cd frontend
    npm install
    cd ..
    log_success "Dependencies installed"
else
    log_success "Dependencies found"
fi

# Kill any existing processes on port 5173
log_step "Checking for existing services on port 5173..."
if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1; then
    log_warning "Port 5173 in use - stopping existing service..."
    pkill -f "vite" 2>/dev/null || true
    sleep 2
    log_success "Cleared port 5173"
else
    log_success "Port 5173 available"
fi

# Start frontend
log_step "Starting Vite development server..."
echo ""
log_info "Frontend logs will appear below:"
echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

cd frontend && npm run dev 2>&1 | while IFS= read -r line; do
    if echo "$line" | grep -q "error"; then
        echo -e "${RED}[ERROR]${NC} $line"
    elif echo "$line" | grep -q "warning"; then
        echo -e "${YELLOW}[WARN]${NC} $line"
    elif echo "$line" | grep -q "Local:.*http"; then
        echo -e "${GREEN}[READY]${NC} $line"
        echo ""
        echo -e "${BOLD}${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${BOLD}${GREEN}  ✓ FRONTEND READY${NC}"
        echo -e "${BOLD}${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
        echo ""
        echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    else
        echo -e "${CYAN}[INFO]${NC} $line"
    fi
done
