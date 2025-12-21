@echo off
REM ============================================================
REM Environmental Law Chatbot - Auto Start Script (Windows)
REM ============================================================
echo ============================================================
echo    ENVIRONMENTAL LAW CHATBOT - STARTING ALL SERVICES
echo ============================================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

REM Start Redis if not running
echo [1/4] Starting Redis...
docker ps -a | findstr "redis-cache" >nul 2>&1
if %errorlevel% neq 0 (
    docker run -d --name redis-cache -p 6379:6379 redis
) else (
    docker start redis-cache 2>nul
)
echo      Redis started on port 6379

REM Check Neo4j
echo [2/4] Checking Neo4j...
echo      Please ensure Neo4j is running on bolt://localhost:7687
echo      (Start Neo4j Desktop or Neo4j Docker container manually)

REM Start Backend
echo [3/4] Starting Backend API...
cd /d "%~dp0MediXLM\BE"
if not exist ".env" (
    echo      Creating .env from template...
    copy ".env.example" ".env"
)
start "Backend API" cmd /k "python -m uvicorn main_standalone:app --reload --host 0.0.0.0 --port 8000"
echo      Backend started on http://localhost:8000

REM Wait for backend to initialize
echo      Waiting 5 seconds for backend...
timeout /t 5 /nobreak >nul

REM Start Frontend
echo [4/4] Starting Frontend...
cd /d "%~dp0FE"
if not exist ".env.local" (
    echo      Creating .env.local from template...
    if exist "env.example" (
        copy "env.example" ".env.local"
    ) else (
        echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
    )
)
start "Frontend" cmd /k "npm run dev"
echo      Frontend started on http://localhost:3000

REM Done
echo.
echo ============================================================
echo    ALL SERVICES STARTED!
echo ============================================================
echo.
echo    Frontend:  http://localhost:3000
echo    Backend:   http://localhost:8000
echo    Neo4j:     http://localhost:7474
echo    Redis:     localhost:6379
echo.
echo    Press any key to open the chatbot in browser...
pause >nul

start http://localhost:3000/chatbot
