#!/bin/bash
# Script to stop FlexNet license server
# Run this to safely stop the license server

# Configuration
LICENSE_SERVER_DIR="/home/apps/chpc/earth/RLM-3D/aksusbd-10.11.1"
PORT="5053"
PID_FILE="$LICENSE_SERVER_DIR/../rlm.pid"

echo "=== FlexNet License Server Stop Script ==="
echo ""

# Check if we're in the right directory
if [ ! -d "$LICENSE_SERVER_DIR" ]; then
    echo "Error: License server directory not found: $LICENSE_SERVER_DIR"
    echo "Please update the LICENSE_SERVER_DIR variable in this script"
    exit 1
fi

cd "$LICENSE_SERVER_DIR"

# Check if server is running
echo "Checking if license server is running..."
if pgrep -f "rlm.*$PORT" > /dev/null; then
    echo "✓ License server is running"
    echo "Process IDs:"
    pgrep -f "rlm.*$PORT" | xargs ps -p
    echo ""
    
    # Try to stop gracefully first
    echo "Attempting graceful shutdown..."
    pkill -TERM -f "rlm.*$PORT"
    
    # Wait a moment
    sleep 3
    
    # Check if still running
    if pgrep -f "rlm.*$PORT" > /dev/null; then
        echo "Graceful shutdown failed, forcing termination..."
        pkill -KILL -f "rlm.*$PORT"
        sleep 2
    fi
    
    # Final check
    if pgrep -f "rlm.*$PORT" > /dev/null; then
        echo "✗ Failed to stop license server"
        echo "Remaining processes:"
        pgrep -f "rlm.*$PORT" | xargs ps -p
        exit 1
    else
        echo "✓ License server stopped successfully"
    fi
else
    echo "License server is not running"
fi

# Remove PID file if it exists
if [ -f "$PID_FILE" ]; then
    echo "Removing PID file: $PID_FILE"
    rm -f "$PID_FILE"
fi

# Check if port is still listening
echo ""
echo "Checking if port $PORT is still listening..."
if netstat -tlnp 2>/dev/null | grep ":$PORT " > /dev/null; then
    echo "⚠ Warning: Port $PORT is still listening"
    echo "This might be from another process"
    netstat -tlnp 2>/dev/null | grep ":$PORT "
else
    echo "✓ Port $PORT is no longer listening"
fi

echo ""
echo "=== Summary ==="
echo "License server has been stopped"
echo ""
echo "To restart the server, run: ./start_license_server.sh"


