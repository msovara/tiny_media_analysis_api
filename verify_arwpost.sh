#!/bin/bash

# ARWpost Verification Script for Lengau Cluster
# This script verifies the ARWpost installation

set -e  # Exit on any error

# Configuration
INSTALL_DIR="/mnt/lustre/users/msovara/SoftwareBuilds/ARWpost"

echo "=== ARWpost Verification Script ==="
echo "Installation directory: ${INSTALL_DIR}"
echo ""

# Check if installation directory exists
if [ ! -d "${INSTALL_DIR}" ]; then
    echo "✗ Installation directory not found: ${INSTALL_DIR}"
    exit 1
fi

echo "✓ Installation directory exists"

# Check executable
if [ -f "${INSTALL_DIR}/bin/ARWpost" ]; then
    echo "✓ ARWpost executable found: ${INSTALL_DIR}/bin/ARWpost"
    echo "  File size: $(ls -lh ${INSTALL_DIR}/bin/ARWpost | awk '{print $5}')"
    echo "  File type: $(file ${INSTALL_DIR}/bin/ARWpost)"
else
    echo "✗ ARWpost executable not found!"
    exit 1
fi

# Check if executable is runnable
if [ -x "${INSTALL_DIR}/bin/ARWpost" ]; then
    echo "✓ ARWpost executable is executable"
else
    echo "✗ ARWpost executable is not executable!"
    exit 1
fi

# Check source files
if [ -d "${INSTALL_DIR}/share/arwpost" ]; then
    echo "✓ Source files directory exists: ${INSTALL_DIR}/share/arwpost"
    echo "  Number of files: $(find ${INSTALL_DIR}/share/arwpost -type f | wc -l)"
else
    echo "✗ Source files directory not found!"
    exit 1
fi

# Check module file
if [ -f "${INSTALL_DIR}/modulefiles/arwpost-lengau" ]; then
    echo "✓ Module file exists: ${INSTALL_DIR}/modulefiles/arwpost-lengau"
else
    echo "✗ Module file not found!"
    exit 1
fi

# Check setup script
if [ -f "${INSTALL_DIR}/setup_arwpost_lengau.sh" ]; then
    echo "✓ Setup script exists: ${INSTALL_DIR}/setup_arwpost_lengau.sh"
    if [ -x "${INSTALL_DIR}/setup_arwpost_lengau.sh" ]; then
        echo "✓ Setup script is executable"
    else
        echo "✗ Setup script is not executable!"
    fi
else
    echo "✗ Setup script not found!"
    exit 1
fi

# Check installation log
if [ -f "${INSTALL_DIR}/install_log.txt" ]; then
    echo "✓ Installation log exists: ${INSTALL_DIR}/install_log.txt"
    echo "  Installation date: $(grep "Installation Date:" ${INSTALL_DIR}/install_log.txt | cut -d: -f2-)"
else
    echo "✗ Installation log not found!"
    exit 1
fi

# Check build info
if [ -f "${INSTALL_DIR}/build_info.txt" ]; then
    echo "✓ Build info exists: ${INSTALL_DIR}/build_info.txt"
    echo "  Download date: $(grep "Download Date:" ${INSTALL_DIR}/build_info.txt | cut -d: -f2-)"
else
    echo "✗ Build info not found!"
    exit 1
fi

# Test ARWpost execution (if environment is set up)
echo ""
echo "Testing ARWpost execution..."
if command -v ARWpost &> /dev/null; then
    echo "✓ ARWpost is in PATH"
    ARWpost --help 2>/dev/null || echo "  Note: ARWpost help not available (this is normal)"
else
    echo "⚠ ARWpost is not in PATH (run setup script first)"
    echo "  To add to PATH: source ${INSTALL_DIR}/setup_arwpost_lengau.sh"
fi

echo ""
echo "=== Verification Complete ==="
echo "ARWpost installation appears to be complete and correct!"
echo ""
echo "To use ARWpost:"
echo "1. Load the module: module load ${INSTALL_DIR}/modulefiles/arwpost-lengau"
echo "2. Or source the setup script: source ${INSTALL_DIR}/setup_arwpost_lengau.sh"
echo "3. Run ARWpost: ARWpost"
echo ""
echo "Installation files verified:"
echo "- Executable: ${INSTALL_DIR}/bin/ARWpost"
echo "- Source files: ${INSTALL_DIR}/share/arwpost/"
echo "- Module file: ${INSTALL_DIR}/modulefiles/arwpost-lengau"
echo "- Setup script: ${INSTALL_DIR}/setup_arwpost_lengau.sh"
echo "- Installation log: ${INSTALL_DIR}/install_log.txt"
echo "- Build info: ${INSTALL_DIR}/build_info.txt"


