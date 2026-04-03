@echo off
echo Building App Product Workflow...

docker build -t app-product-workflow:latest .

if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    exit /b 1
)

echo Build completed successfully!
echo Image: app-product-workflow:latest
