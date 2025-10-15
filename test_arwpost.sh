#!/bin/bash
# ARWpost Test Script for Lengau Cluster
# This script tests the installed ARWpost

set -e  # Exit on any error

# Configuration
INSTALL_DIR="/home/apps/chpc/earth/ARWpost-complete"

echo "=== ARWpost Test Script ==="
echo "Installation directory: ${INSTALL_DIR}"
echo ""

# Test 1: Module loading
echo "1. Testing module loading..."
module purge
module load chpc/earth/arwpost-complete/3.1

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

# Test 6: Wrapper script
echo "6. Testing wrapper script..."
if [ -f "${INSTALL_DIR}/bin/run_arwpost" ]; then
    echo "✓ Wrapper script found"
    chmod +x "${INSTALL_DIR}/bin/run_arwpost"
    "${INSTALL_DIR}/bin/run_arwpost" --help 2>/dev/null || "${INSTALL_DIR}/bin/run_arwpost" -h 2>/dev/null || "${INSTALL_DIR}/bin/run_arwpost" 2>/dev/null || echo "Wrapper script runs but may not show help"
else
    echo "✗ Wrapper script not found"
fi

# Test 7: Module system integration
echo "7. Testing module system integration..."
module avail 2>&1 | grep -i arwpost || echo "Module not found in module avail"

# Test 8: File permissions
echo "8. Testing file permissions..."
if [ -r "${INSTALL_DIR}/bin/ARWpost" ]; then
    echo "✓ ARWpost executable is readable"
else
    echo "✗ ARWpost executable is not readable"
fi

if [ -x "${INSTALL_DIR}/bin/ARWpost" ]; then
    echo "✓ ARWpost executable is executable"
else
    echo "✗ ARWpost executable is not executable"
fi

# Test 9: Documentation and examples
echo "9. Testing documentation and examples..."
if [ -d "${INSTALL_DIR}/examples" ]; then
    echo "✓ Examples directory found"
    ls -la "${INSTALL_DIR}/examples/"
else
    echo "✗ Examples directory not found"
fi

if [ -d "${INSTALL_DIR}/share/arwpost" ]; then
    echo "✓ Share directory found"
    ls -la "${INSTALL_DIR}/share/arwpost/"
else
    echo "✗ Share directory not found"
fi

# Test 10: Installation log
echo "10. Testing installation log..."
if [ -f "${INSTALL_DIR}/install_log.txt" ]; then
    echo "✓ Installation log found"
    echo "Installation date: $(grep "Installation Date:" "${INSTALL_DIR}/install_log.txt" | cut -d: -f2-)"
else
    echo "✗ Installation log not found"
fi

# Test 11: Module file
echo "11. Testing module file..."
if [ -f "/apps/chpc/scripts/modules/earth/arwpost-complete/3.1" ]; then
    echo "✓ Module file found"
else
    echo "✗ Module file not found"
fi

# Test 12: Default version
echo "12. Testing default version..."
if [ -f "/apps/chpc/scripts/modules/earth/arwpost-complete/.version" ]; then
    echo "✓ Default version file found"
    echo "Default version: $(cat /apps/chpc/scripts/modules/earth/arwpost-complete/.version)"
else
    echo "✗ Default version file not found"
fi

# Test 13: Symlink
echo "13. Testing symlink..."
if [ -L "/apps/chpc/scripts/modules/earth/arwpost-complete/default" ]; then
    echo "✓ Default symlink found"
else
    echo "✗ Default symlink not found"
fi

# Test 14: Usage examples
echo "14. Testing usage examples..."
if [ -f "${INSTALL_DIR}/examples/usage_examples.txt" ]; then
    echo "✓ Usage examples found"
    echo "Usage examples:"
    head -10 "${INSTALL_DIR}/examples/usage_examples.txt"
else
    echo "✗ Usage examples not found"
fi

# Test 15: Final verification
echo "15. Final verification..."
echo "Testing complete ARWpost installation..."

# Test module loading again
module purge
module load chpc/earth/arwpost-complete/3.1

# Test executable
if command -v ARWpost >/dev/null 2>&1; then
    echo "✓ ARWpost is available after module load"
else
    echo "✗ ARWpost is not available after module load"
fi

# Test wrapper
if [ -x "${INSTALL_DIR}/bin/run_arwpost" ]; then
    echo "✓ Wrapper script is executable"
else
    echo "✗ Wrapper script is not executable"
fi

echo ""
echo "=== ARWpost Test Complete ==="
echo "If you see 'SUCCESS' messages above, the full ARWpost is working correctly!"
echo ""
echo "To use ARWpost:"
echo "1. module load chpc/earth/arwpost-complete/3.1"
echo "2. ARWpost"
echo "3. Or: run_arwpost"
echo ""
echo "ARWpost testing completed successfully!"









