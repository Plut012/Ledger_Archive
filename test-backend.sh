#!/bin/bash

# Quick backend test script - checks if backend can start

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}Testing Backend...${NC}"
echo ""

# Activate venv
if [ ! -d ".venv" ]; then
    echo -e "${RED}✗ No virtual environment found${NC}"
    echo -e "${YELLOW}Run: python3 -m venv .venv${NC}"
    exit 1
fi

source .venv/bin/activate

# Test imports
echo -e "${CYAN}Testing Python imports...${NC}"
cd backend

python -c "
try:
    import fastapi
    print('✓ fastapi')
except ImportError as e:
    print(f'✗ fastapi: {e}')

try:
    import uvicorn
    print('✓ uvicorn')
except ImportError as e:
    print(f'✗ uvicorn: {e}')

try:
    import websockets
    print('✓ websockets')
except ImportError as e:
    print(f'✗ websockets: {e}')

try:
    import main
    print('✓ main.py imports successfully')
except Exception as e:
    print(f'✗ main.py import failed:')
    print(f'  {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()
    exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Backend imports working${NC}"
    echo ""
    echo -e "${CYAN}Starting server test (5 seconds)...${NC}"
    timeout 5 python -m uvicorn main:app --host 0.0.0.0 --port 8000 2>&1 | head -20 || true
    echo ""
    echo -e "${GREEN}✓ Backend test complete${NC}"
else
    echo ""
    echo -e "${RED}✗ Backend has import errors${NC}"
    echo -e "${YELLOW}Fix the import errors above before using start.sh${NC}"
    exit 1
fi
