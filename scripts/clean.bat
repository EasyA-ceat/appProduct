@echo off
echo Cleaning up...

docker-compose down -v

docker rmi app-product-workflow:latest 2>nul

echo Cleanup completed.
