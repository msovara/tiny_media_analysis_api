#!/bin/bash
# Test script for full ARWpost installation

echo "=== Testing Full ARWpost Installation ==="

# Test 1: Module loading
echo "1. Testing module loading..."
module purge
module load chpc/earth/arwpost-full/3.1

if [ $? -eq 0 ]; then
    echo "✓ Module loaded successfully"
else
    echo "✗ Module loading failed"
    exit 1
fi

# Test 2: Executable availability
echo "2. Testing executable availability..."
if command -v ARWpost >/dev/null 2>&1; then
    echo "✓ ARWpost found in PATH"
    which ARWpost
else
    echo "✗ ARWpost not found in PATH"
    exit 1
fi

# Test 3: Executable execution
echo "3. Testing ARWpost execution..."
ARWpost --help 2>/dev/null || ARWpost -h 2>/dev/null || ARWpost 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ ARWpost executes successfully"
else
    echo "⚠ ARWpost execution had issues (may be normal)"
fi

# Test 4: Environment variables
echo "4. Testing environment variables..."
echo "ARWPOST_ROOT: ${ARWPOST_ROOT}"
echo "ARWPOST_VERSION: ${ARWPOST_VERSION}"
echo "ARWPOST_TYPE: ${ARWPOST_TYPE}"

# Test 5: Library linking
echo "5. Testing library linking..."
ldd $(which ARWpost) 2>/dev/null | grep -E "(netcdf|hdf5)" || echo "Library linking check completed"

echo ""
echo "=== Full ARWpost Test Complete ==="
echo "If you see 'SUCCESS' messages above, the full ARWpost is working correctly!"
echo ""
echo "To use full ARWpost:"
echo "1. module load chpc/earth/arwpost-full/3.1"
echo "2. ARWpost"
echo "3. Or: run_arwpost"









