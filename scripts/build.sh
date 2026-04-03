#!/bin/bash
set -e

echo "Building App Product Workflow..."

docker build -t app-product-workflow:latest .

echo "Build completed successfully!"
echo "Image: app-product-workflow:latest"
