#!/bin/bash
# ============================================================
# Environmental Law Chatbot - Auto Start Script (macOS/Linux)
# ============================================================

echo "============================================================"
echo "   ENVIRONMENTAL LAW CHATBOT - STARTING ALL SERVICES"
echo "============================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}[ERROR] Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Start Redis if not running
echo "[1/4] Starting Redis..."
if ! docker ps | grep -q redis-cache; then
    if docker ps -a | grep -q redis-cache; then
        docker start redis-cache
    else
        docker run -d --name redis-cache -p 6379:6379 redis
    fi
fi
echo -e "${GREEN}      Redis started on port 6379${NC}"

# Check Neo4j
echo "[2/4] Checking Neo4j..."
echo "      Please ensure Neo4j is running on bolt://localhost:7687"

# Start Backend
echo "[3/4] Starting Backend API..."
cd "$SCRIPT_DIR/MediXLM/BE"
if [ ! -f ".env" ]; then
    echo "      Creating .env from template..."
    cp ".env.example" ".env"
fi
python -m uvicorn main_standalone:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo -e "${GREEN}      Backend started on http://localhost:8000 (PID: $BACKEND_PID)${NC}"

# Wait for backend to initialize
echo "      Waiting 5 seconds for backend..."
sleep 5

# Start Frontend
echo "[4/4] Starting Frontend..."
cd "$SCRIPT_DIR/FE"
if [ ! -f ".env.local" ]; then
    echo "      Creating .env.local from template..."
    if [ -f "env.example" ]; then
        cp "env.example" ".env.local"
    else
        echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
    fi
fi
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}      Frontend started on http://localhost:3000 (PID: $FRONTEND_PID)${NC}"

# Done
echo ""
echo "============================================================"
echo "   ALL SERVICES STARTED!"
echo "============================================================"
echo ""
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   Neo4j:     http://localhost:7474"
echo "   Redis:     localhost:6379"
echo ""
echo "   Press Ctrl+C to stop all services..."
echo ""

# Open browser
if command -v open > /dev/null; then
    open http://localhost:3000/chatbot
elif command -v xdg-open > /dev/null; then
    xdg-open http://localhost:3000/chatbot
fi

# Wait for Ctrl+C
wait
