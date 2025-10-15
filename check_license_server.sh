#!/bin/bash
# Script to check FlexNet license server status
# Run this to verify your license server is working correctly

# Configuration
LICENSE_SERVER_DIR="/home/apps/chpc/earth/RLM-3D/aksusbd-10.11.1"
PORT="5053"
HOSTNAME=$(hostname)

echo "=== FlexNet License Server Status Check ==="
echo ""

# Check if we're in the right directory
if [ ! -d "$LICENSE_SERVER_DIR" ]; then
    echo "Error: License server directory not found: $LICENSE_SERVER_DIR"
    echo "Please update the LICENSE_SERVER_DIR variable in this script"
    exit 1
fi

cd "$LICENSE_SERVER_DIR"

echo "Server Information:"
echo "=================="
echo "Hostname: $HOSTNAME"
echo "Port: $PORT"
echo "Directory: $LICENSE_SERVER_DIR"
echo ""

# Check if RLM daemon is running
echo "1. Checking if RLM daemon is running..."
if pgrep -f "rlm.*$PORT" > /dev/null; then
    echo "✓ RLM daemon is running"
    echo "Process IDs:"
    pgrep -f "rlm.*$PORT" | xargs ps -p
else
    echo "✗ RLM daemon is not running"
fi
echo ""

# Check if port is listening
echo "2. Checking if port $PORT is listening..."
if netstat -tlnp 2>/dev/null | grep ":$PORT " > /dev/null; then
    echo "✓ Port $PORT is listening"
    netstat -tlnp 2>/dev/null | grep ":$PORT "
else
    echo "✗ Port $PORT is not listening"
fi
echo ""

# Check if RLM utilities exist
echo "3. Checking RLM utilities..."
if [ -f "./bin/rlmutil" ]; then
    echo "✓ rlmutil found"
else
    echo "✗ rlmutil not found"
fi

if [ -f "./bin/rlm" ]; then
    echo "✓ rlm daemon found"
else
    echo "✗ rlm daemon not found"
fi
echo ""

# Try to get license server status
echo "4. Attempting to get license server status..."
if [ -f "./bin/rlmutil" ]; then
    echo "Running: ./bin/rlmutil lmstat -a -c ${PORT}@${HOSTNAME}"
    echo ""
    ./bin/rlmutil lmstat -a -c "${PORT}@${HOSTNAME}"
    echo ""
else
    echo "Cannot check license status - rlmutil not found"
fi

# Check for log files
echo "5. Checking for log files..."
LOG_FILES=("$LICENSE_SERVER_DIR/../rlm.log" "$LICENSE_SERVER_DIR/rlm.log" "/tmp/rlm.log")
for log_file in "${LOG_FILES[@]}"; do
    if [ -f "$log_file" ]; then
        echo "✓ Found log file: $log_file"
        echo "Last 10 lines:"
        tail -10 "$log_file"
        echo ""
    fi
done

# Check environment variables
echo "6. Checking environment variables..."
if [ -n "$LM_LICENSE_FILE" ]; then
    echo "✓ LM_LICENSE_FILE is set: $LM_LICENSE_FILE"
else
    echo "⚠ LM_LICENSE_FILE is not set"
    echo "   You may need to set: export LM_LICENSE_FILE=${PORT}@${HOSTNAME}"
fi
echo ""

# Test network connectivity
echo "7. Testing network connectivity..."
if command -v telnet >/dev/null 2>&1; then
    echo "Testing connection to ${HOSTNAME}:${PORT}..."
    timeout 5 bash -c "</dev/tcp/${HOSTNAME}/${PORT}" && echo "✓ Connection successful" || echo "✗ Connection failed"
else
    echo "telnet not available, skipping connectivity test"
fi
echo ""

echo "=== Summary ==="
if pgrep -f "rlm.*$PORT" > /dev/null && netstat -tlnp 2>/dev/null | grep ":$PORT " > /dev/null; then
    echo "✓ License server appears to be running correctly"
else
    echo "✗ License server has issues - check the details above"
fi
echo ""
echo "For troubleshooting, check:"
echo "- License file configuration"
echo "- MAC address in license file"
echo "- Firewall settings"
echo "- Log files for error messages"


