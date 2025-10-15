#!/bin/bash
# Script to start FlexNet license server
# Run this on your chosen license server (chpclic1 or login1)

# Configuration
LICENSE_SERVER_DIR="/home/apps/chpc/earth/RLM-3D/aksusbd-10.11.1"
LICENSE_FILE="/home/apps/chpc/earth/RLM-3D/license.lic"
LOG_FILE="/home/apps/chpc/earth/RLM-3D/rlm.log"
PORT="5053"

echo "=== FlexNet License Server Startup Script ==="
echo ""

# Check if we're in the right directory
if [ ! -d "$LICENSE_SERVER_DIR" ]; then
    echo "Error: License server directory not found: $LICENSE_SERVER_DIR"
    echo "Please update the LICENSE_SERVER_DIR variable in this script"
    exit 1
fi

cd "$LICENSE_SERVER_DIR"

# Check if license file exists
if [ ! -f "$LICENSE_FILE" ]; then
    echo "Warning: License file not found: $LICENSE_FILE"
    echo "Please create your license file first"
    echo ""
    echo "Example license file content:"
    echo "SERVER $(hostname) <MAC_ADDRESS> $PORT"
    echo "VENDOR <vendor_name> $LICENSE_SERVER_DIR/bin/<vendor_daemon>"
    echo "FEATURE <feature_name> <vendor_name> <version> <expiry> <num_licenses> HOSTID=<MAC_ADDRESS>"
    echo ""
    read -p "Do you want to continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if RLM daemon exists
if [ ! -f "./bin/rlm" ]; then
    echo "Error: RLM daemon not found: ./bin/rlm"
    echo "Please check your installation"
    exit 1
fi

# Check if server is already running
if pgrep -f "rlm.*$PORT" > /dev/null; then
    echo "Warning: License server appears to be already running on port $PORT"
    echo "Processes:"
    pgrep -f "rlm.*$PORT" | xargs ps -p
    echo ""
    read -p "Do you want to stop existing server and start new one? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Stopping existing license server..."
        pkill -f "rlm.*$PORT"
        sleep 2
    else
        echo "Exiting..."
        exit 0
    fi
fi

# Create log directory if it doesn't exist
LOG_DIR=$(dirname "$LOG_FILE")
mkdir -p "$LOG_DIR"

# Start the license server
echo "Starting FlexNet license server..."
echo "Directory: $LICENSE_SERVER_DIR"
echo "License file: $LICENSE_FILE"
echo "Log file: $LOG_FILE"
echo "Port: $PORT"
echo ""

# Start RLM daemon
if [ -f "$LICENSE_FILE" ]; then
    nohup ./bin/rlm -c "$LICENSE_FILE" -dlog "$LOG_FILE" > /dev/null 2>&1 &
else
    nohup ./bin/rlm -dlog "$LOG_FILE" > /dev/null 2>&1 &
fi

SERVER_PID=$!

# Wait a moment for server to start
sleep 3

# Check if server started successfully
if kill -0 $SERVER_PID 2>/dev/null; then
    echo "✓ License server started successfully!"
    echo "Process ID: $SERVER_PID"
    echo ""
    
    # Check if port is listening
    if netstat -tlnp 2>/dev/null | grep ":$PORT " > /dev/null; then
        echo "✓ Server is listening on port $PORT"
    else
        echo "⚠ Warning: Server may not be listening on port $PORT yet"
    fi
    
    echo ""
    echo "=== Server Information ==="
    echo "Hostname: $(hostname)"
    echo "Port: $PORT"
    echo "License file: $LICENSE_FILE"
    echo "Log file: $LOG_FILE"
    echo ""
    
    echo "=== Useful Commands ==="
    echo "Check server status: ./bin/rlmutil lmstat -a -c ${PORT}@$(hostname)"
    echo "View logs: tail -f $LOG_FILE"
    echo "Stop server: kill $SERVER_PID"
    echo "Check processes: ps aux | grep rlm"
    echo ""
    
    echo "=== Environment Variable for Clients ==="
    echo "Add this to your shell profile (.bashrc, .bash_profile):"
    echo "export LM_LICENSE_FILE=${PORT}@$(hostname)"
    echo ""
    
    # Save PID to file for easy management
    echo $SERVER_PID > "$LOG_DIR/rlm.pid"
    echo "PID saved to: $LOG_DIR/rlm.pid"
    
else
    echo "✗ Failed to start license server"
    echo "Check the log file: $LOG_FILE"
    exit 1
fi


