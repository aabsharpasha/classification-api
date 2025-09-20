#!/bin/bash

# Build script for Classification API Docker container

echo "Building Classification API Docker container..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Creating from env.example..."
    cp env.example .env
    echo "Please edit .env file with your actual API tokens before running the container."
fi

# Build the Docker image
docker build -t classification-api .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo ""
    echo "To run the container:"
    echo "  docker-compose up"
    echo ""
    echo "Or manually:"
    echo "  docker run -p 8000:8000 --env-file .env classification-api"
    echo ""
    echo "API will be available at: http://localhost:8000/docs"
else
    echo "❌ Docker build failed!"
    exit 1
fi

