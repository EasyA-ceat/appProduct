@echo off
echo Stopping App Product Workflow...

docker-compose down

if %ERRORLEVEL% NEQ 0 (
    echo Failed to stop workflow!
    exit /b 1
)

echo Workflow stopped.
