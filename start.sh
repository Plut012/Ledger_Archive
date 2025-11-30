#!/bin/bash

# Chain of Truth - Startup Script
# Starts all backend components with clear logs

set -e  # Exit on error

# Color codes for readable output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Logging functions
log_header() {
    echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${CYAN}  $1${NC}"
    echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

log_info() {
    echo -e "${CYAN}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

log_step() {
    echo -e "${MAGENTA}▸${NC} $1"
}

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
║              OF TRUTH - Startup Script                   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    log_error "Not in project root directory!"
    log_info "Please run this script from /home/pluto/dev/chain/"
    exit 1
fi

log_header "PRE-FLIGHT CHECKS"

# Check Python
log_step "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    log_success "Python found: $PYTHON_VERSION"
else
    log_error "Python 3 not found!"
    exit 1
fi

# Check uv
log_step "Checking uv package manager..."
if command -v uv &> /dev/null; then
    UV_VERSION=$(uv --version)
    log_success "uv found: $UV_VERSION"
else
    log_warning "uv not found - falling back to pip"
    USE_UV=false
fi

# Check if virtual environment exists
log_step "Checking virtual environment..."
if [ -d ".venv" ]; then
    log_success "Virtual environment found"
else
    log_warning "Virtual environment not found - will create one"
    log_step "Creating virtual environment..."
    python3 -m venv .venv
    log_success "Virtual environment created"
fi

# Activate virtual environment
log_step "Activating virtual environment..."
source .venv/bin/activate
log_success "Virtual environment activated"

log_header "DEPENDENCY CHECK"

# Install/update dependencies
log_step "Checking dependencies..."
if [ "$USE_UV" = false ]; then
    log_info "Installing dependencies with pip..."
    if [ -f "requirements.txt" ]; then
        pip install -q -r requirements.txt 2>&1 | grep -v "Requirement already satisfied" || true
    elif [ -f "pyproject.toml" ]; then
        pip install -q -e . 2>&1 | grep -v "Requirement already satisfied" || true
    fi
else
    log_info "Syncing dependencies with uv..."
    if [ -f "pyproject.toml" ]; then
        uv sync --quiet 2>&1 || log_warning "uv sync failed, continuing anyway..."
    elif [ -f "requirements.txt" ]; then
        uv pip install -r requirements.txt --quiet 2>&1 || log_warning "uv install failed, continuing anyway..."
    fi
fi
log_success "Dependencies ready"

log_header "ENVIRONMENT SETUP"

# Check for .env file
log_step "Checking environment configuration..."
if [ -f "backend/.env" ]; then
    log_success ".env file found"

    # Check for required variables
    if grep -q "ANTHROPIC_API_KEY" backend/.env; then
        API_KEY=$(grep "ANTHROPIC_API_KEY" backend/.env | cut -d '=' -f2)
        if [ -n "$API_KEY" ] && [ "$API_KEY" != "your_api_key_here" ]; then
            log_success "ANTHROPIC_API_KEY configured"
        else
            log_warning "ANTHROPIC_API_KEY not set (LLM features disabled)"
        fi
    else
        log_warning "ANTHROPIC_API_KEY not found in .env"
    fi
else
    log_warning ".env file not found"
    log_info "Creating default .env file..."
    cat > backend/.env << 'ENVEOF'
# Chain of Truth - Environment Configuration

# LLM Configuration
ANTHROPIC_API_KEY=your_api_key_here
# Uncomment to use OpenAI instead:
# OPENAI_API_KEY=your_openai_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Database (optional - defaults to IndexedDB in browser)
# DATABASE_URL=sqlite:///./chain_of_truth.db
ENVEOF
    log_success "Created backend/.env (please configure API keys)"
fi

log_header "STARTING BACKEND SERVICES"

# Kill any existing processes on port 8000
log_step "Checking for existing services on port 8000..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    log_warning "Port 8000 in use - stopping existing service..."
    pkill -f "uvicorn backend.main:app" 2>/dev/null || true
    sleep 2
    log_success "Cleared port 8000"
else
    log_success "Port 8000 available"
fi

# Test backend imports first
log_step "Testing backend imports..."
cd backend
if ! python -c "import main" 2>/dev/null; then
    log_error "Backend import failed!"
    echo ""
    log_info "Running diagnostic..."
    python -c "import main" 2>&1 | head -20
    echo ""
    log_error "Please fix the import errors above before starting"
    exit 1
fi
log_success "Backend imports OK"
cd ..

# Start backend
log_step "Starting FastAPI backend server..."
echo ""
log_info "Backend logs will appear below:"
echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Start uvicorn with formatted output
cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level info 2>&1 | while IFS= read -r line; do
    # Color-code different log types
    if echo "$line" | grep -q "ERROR"; then
        echo -e "${RED}[ERROR]${NC} $line"
    elif echo "$line" | grep -q "WARNING"; then
        echo -e "${YELLOW}[WARN]${NC} $line"
    elif echo "$line" | grep -q "INFO.*Application startup complete"; then
        echo -e "${GREEN}[INFO]${NC} $line"
        echo ""
        echo -e "${BOLD}${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${BOLD}${GREEN}  ✓ BACKEND READY${NC}"
        echo -e "${BOLD}${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        echo -e "${CYAN}API Documentation:${NC}  http://localhost:8000/docs"
        echo -e "${CYAN}Health Check:${NC}      http://localhost:8000/health"
        echo -e "${CYAN}Frontend (if running):${NC} http://localhost:5173"
        echo ""
        echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
        echo ""
        echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    elif echo "$line" | grep -q "INFO"; then
        echo -e "${CYAN}[INFO]${NC} $line"
    else
        echo "$line"
    fi
done
