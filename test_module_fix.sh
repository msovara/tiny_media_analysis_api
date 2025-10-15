#!/bin/bash

# Test ARWpost Module Fix Script
# This script tests the corrected module file

echo "=== Testing ARWpost Module Fix ==="
echo ""

# First, purge all modules
echo "1. Purging all modules..."
module purge
echo "✓ Modules purged"
echo ""

# Check current modules
echo "2. Current loaded modules:"
module list
echo ""

# Try to load the ARWpost module
echo "3. Loading ARWpost module..."
module load chpc/earth/arwpost/3.1
echo ""

# Check loaded modules
echo "4. Loaded modules after ARWpost:"
module list
echo ""

# Test ARWpost executable
echo "5. Testing ARWpost executable:"
if command -v ARWpost >/dev/null 2>&1; then
    echo "✓ ARWpost found in PATH"
    echo "Location: $(which ARWpost)"
    echo ""
    echo "6. Testing ARWpost execution (should show help/usage):"
    timeout 10s ARWpost 2>&1 | head -20 || echo "ARWpost executed (may have shown help/usage)"
else
    echo "✗ ARWpost not found in PATH"
    echo "Checking installation directory..."
    ls -la /home/apps/chpc/earth/ARWpost/bin/
fi
echo ""

# Test wrapper script
echo "7. Testing wrapper script:"
if command -v run_arwpost >/dev/null 2>&1; then
    echo "✓ run_arwpost wrapper found"
    echo "Location: $(which run_arwpost)"
else
    echo "✗ run_arwpost wrapper not found"
fi
echo ""

# Check environment variables
echo "8. ARWpost environment variables:"
echo "ARWPOST_ROOT: ${ARWPOST_ROOT:-'Not set'}"
echo "ARWPOST_VERSION: ${ARWPOST_VERSION:-'Not set'}"
echo "ARWPOST_COMPILER: ${ARWPOST_COMPILER:-'Not set'}"
echo ""

echo "=== Module Test Complete ==="
echo "If no dependency errors appeared above, the module fix was successful!"
echo ""
echo "To use ARWpost:"
echo "  module load chpc/earth/arwpost/3.1"
echo "  ARWpost"
















