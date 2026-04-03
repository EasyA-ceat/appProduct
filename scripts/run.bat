@echo off

if not exist .env (
    echo Error: .env file not found. Please create it from .env.example
    exit /b 1
)

echo Starting App Product Workflow...

docker-compose up -d

if %ERRORLEVEL% NEQ 0 (
    echo Failed to start workflow!
    exit /b 1
)

echo Workflow started. Check logs with: docker-compose logs -f
