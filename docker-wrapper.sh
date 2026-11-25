#!/bin/bash

# Wrapper script to simplify Docker usage for ai-fixed-points
# Usage: ./docker-wrapper.sh [file_path]

set -e  # Exit on any error

# Default image name
IMAGE_NAME="ai-fixed-points"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH"
    exit 1
fi

# Check if image exists locally
if ! docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "^${IMAGE_NAME}:$"; then
    echo "Building Docker image..."
    docker build -t ${IMAGE_NAME} .
fi

# If no file provided, show help
if [ $# -eq 0 ]; then
    echo "Usage: $0 [file_path]"
    echo "Example: $0 /path/to/your/code.py"
    echo ""
    echo "To run with specific Docker options:"
    echo "  $0 --help"
    exit 1
fi

# Show help
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Docker wrapper for ai-fixed-points"
    echo ""
    echo "Usage:"
    echo "  $0 [file_path]              # Run on specified file"
    echo "  $0 --help                   # Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 src/ai_fixed_points/base.py"
    echo "  $0 /home/user/my_code.py"
    echo "  $0 ./test.py"
    exit 0
fi

# Get the file path
FILE_PATH="$1"

# Check if file exists
if [ ! -f "$FILE_PATH" ]; then
    echo "Error: File '$FILE_PATH' not found"
    exit 1
fi

# Get absolute path for Docker volume mounting
ABSOLUTE_PATH=$(realpath "$FILE_PATH")

# Extract filename for the container
FILENAME=$(basename "$FILE_PATH")

echo "Running ai-fixed-points on: $FILE_PATH"
echo "Using Docker image: $IMAGE_NAME"

# Run with Docker, mounting the file directory
docker run --rm \
    -v "$ABSOLUTE_PATH:/work/input.py" \
    "$IMAGE_NAME" \
    /work/input.py