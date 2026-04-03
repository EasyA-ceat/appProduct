#!/bin/bash
set -e

if [ ! -f .env ]; then
    echo "Error: .env file not found. Please create it from .env.example"
    exit 1
fi

echo "Starting App Product Workflow..."

docker-compose up -d

echo "Workflow started. Check logs with: docker-compose logs -f"
