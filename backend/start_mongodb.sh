#!/bin/bash
# Start MongoDB for Chain of Truth development

echo "Starting MongoDB container..."

# Check if container already exists
if docker ps -a --format '{{.Names}}' | grep -q "^chain-mongodb$"; then
    echo "Container 'chain-mongodb' already exists. Starting it..."
    docker start chain-mongodb
else
    echo "Creating and starting new MongoDB container..."
    docker run -d -p 27017:27017 --name chain-mongodb mongo:latest
fi

# Wait a moment for MongoDB to be ready
sleep 3

# Check if it's running
if docker ps --format '{{.Names}}' | grep -q "^chain-mongodb$"; then
    echo "✓ MongoDB is running on port 27017"
else
    echo "✗ Failed to start MongoDB"
    exit 1
fi
