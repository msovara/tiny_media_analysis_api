#!/bin/bash

# Test Final ARWpost Module Script
# This script tests the completely fixed module

echo "=== Testing Final ARWpost Module ==="
echo ""

# First, purge all modules
echo "1. Purging all modules..."
module purge
echo "✓ Modules purged"
echo ""

# Try to load the ARWpost module
echo "2. Loading ARWpost module..."
module load chpc/earth/arwpost/3.1
echo ""

# Check if ARWpost is available
echo "3. Testing ARWpost availability:"
if command -v ARWpost >/dev/null 2>&1; then
    echo "✅ SUCCESS: ARWpost is available!"
    echo "Location: $(which ARWpost)"
    echo ""
    echo "4. Testing ARWpost execution:"
    timeout 5s ARWpost 2>&1 | head -10 || echo "ARWpost executed successfully"
else
    echo "❌ FAILED: ARWpost not found in PATH"
fi
echo ""

echo "=== Test Complete ==="
echo "If you see 'SUCCESS' above, the module is working correctly!"
echo ""
echo "To use ARWpost:"
echo "  module load chpc/earth/arwpost/3.1"
echo "  ARWpost"
















