#!/bin/bash
# Master ARWpost Build Script for Lengau Cluster
# This script orchestrates the complete ARWpost build process

set -e  # Exit on any error

echo "=== Master ARWpost Build Script ==="
echo "This script will build the complete ARWpost with all modules"
echo ""

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOWNLOAD_SCRIPT="${SCRIPT_DIR}/download_arwpost_source.sh"
BUILD_SCRIPT="${SCRIPT_DIR}/build_arwpost.sh"
INSTALL_SCRIPT="${SCRIPT_DIR}/install_arwpost.sh"
TEST_SCRIPT="${SCRIPT_DIR}/test_arwpost.sh"

# Check if all scripts exist
echo "Checking for required scripts..."
for script in "${DOWNLOAD_SCRIPT}" "${BUILD_SCRIPT}" "${INSTALL_SCRIPT}" "${TEST_SCRIPT}"; do
    if [ -f "${script}" ]; then
        echo "✓ Found: $(basename "${script}")"
    else
        echo "✗ Missing: $(basename "${script}")"
        exit 1
    fi
done

# Make scripts executable
echo "Making scripts executable..."
chmod +x "${DOWNLOAD_SCRIPT}"
chmod +x "${BUILD_SCRIPT}"
chmod +x "${INSTALL_SCRIPT}"
chmod +x "${TEST_SCRIPT}"

echo ""
echo "=== Step 1: Download ARWpost Source ==="
echo "Running: ${DOWNLOAD_SCRIPT}"
"${DOWNLOAD_SCRIPT}"

if [ $? -eq 0 ]; then
    echo "✓ Download completed successfully"
else
    echo "✗ Download failed"
    exit 1
fi

echo ""
echo "=== Step 2: Build ARWpost ==="
echo "Running: ${BUILD_SCRIPT}"
"${BUILD_SCRIPT}"

if [ $? -eq 0 ]; then
    echo "✓ Build completed successfully"
else
    echo "✗ Build failed"
    exit 1
fi

echo ""
echo "=== Step 3: Install ARWpost ==="
echo "Running: ${INSTALL_SCRIPT}"
"${INSTALL_SCRIPT}"

if [ $? -eq 0 ]; then
    echo "✓ Installation completed successfully"
else
    echo "✗ Installation failed"
    exit 1
fi

echo ""
echo "=== Step 4: Test ARWpost ==="
echo "Running: ${TEST_SCRIPT}"
"${TEST_SCRIPT}"

if [ $? -eq 0 ]; then
    echo "✓ Testing completed successfully"
else
    echo "✗ Testing failed"
    exit 1
fi

echo ""
echo "=== Master ARWpost Build Complete ==="
echo "All steps completed successfully!"
echo ""
echo "ARWpost is now ready to use:"
echo "1. module load chpc/earth/arwpost-complete/3.1"
echo "2. ARWpost"
echo "3. Or: run_arwpost"
echo ""
echo "Master ARWpost build completed successfully!"









