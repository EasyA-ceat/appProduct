#!/bin/bash
set -e

echo "Cleaning up..."

docker-compose down -v

docker rmi app-product-workflow:latest 2>/dev/null || true

echo "Cleanup completed."
