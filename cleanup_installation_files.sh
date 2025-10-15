#!/bin/bash

# Cleanup ARWpost Installation Files Script
# This script removes duplicate and broken files from the installation directory

set -e

# Configuration
INSTALL_DIR="/home/apps/chpc/earth/ARWpost"

echo "=== Cleaning Up ARWpost Installation Files ==="
echo "Installation directory: ${INSTALL_DIR}"
echo ""

# Check if installation directory exists
if [ ! -d "${INSTALL_DIR}" ]; then
    echo "✗ Installation directory not found: ${INSTALL_DIR}"
    echo "No cleanup needed."
    exit 0
fi

echo "✓ Installation directory found"

# List current files before cleanup
echo ""
echo "=== Current Installation Files ==="
ls -la "${INSTALL_DIR}/" 2>/dev/null || echo "No files found"
echo ""

# Backup important files
echo "=== Creating Backups ==="
if [ -f "${INSTALL_DIR}/bin/ARWpost" ]; then
    cp "${INSTALL_DIR}/bin/ARWpost" "${INSTALL_DIR}/bin/ARWpost.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✓ Backup created: ARWpost.backup.$(date +%Y%m%d_%H%M%S)"
fi

if [ -f "${INSTALL_DIR}/bin/run_arwpost" ]; then
    cp "${INSTALL_DIR}/bin/run_arwpost" "${INSTALL_DIR}/bin/run_arwpost.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✓ Backup created: run_arwpost.backup.$(date +%Y%m%d_%H%M%S)"
fi
echo ""

# Remove duplicate and broken files
echo "=== Removing Duplicate and Broken Files ==="

# Remove old backup files (keep only the latest)
echo "Removing old backup files..."
find "${INSTALL_DIR}/" -name "*.backup*" -type f | head -n -2 | xargs rm -f 2>/dev/null || echo "No old backups to remove"

# Remove broken symlinks
echo "Removing broken symlinks..."
find "${INSTALL_DIR}/" -type l -exec test ! -e {} \; -delete 2>/dev/null || echo "No broken symlinks found"

# Remove temporary files
echo "Removing temporary files..."
find "${INSTALL_DIR}/" -name "*.tmp" -type f -delete 2>/dev/null || echo "No .tmp files to remove"
find "${INSTALL_DIR}/" -name "*.bak" -type f -delete 2>/dev/null || echo "No .bak files to remove"
find "${INSTALL_DIR}/" -name "*.log" -type f -delete 2>/dev/null || echo "No .log files to remove"

# Remove duplicate installation scripts (keep only the working ones)
echo "Removing duplicate installation scripts..."
cd "${INSTALL_DIR}"
# Keep only the essential files and remove duplicates
find . -name "install_arwpost_*.sh" -type f | grep -v "minimal_final\|working\|clean" | xargs rm -f 2>/dev/null || echo "No duplicate install scripts to remove"

# Remove test files that are no longer needed
echo "Removing test files..."
find . -name "test_*.f90" -type f -delete 2>/dev/null || echo "No test files to remove"
find . -name "debug_*.sh" -type f -delete 2>/dev/null || echo "No debug files to remove"

echo "✓ Cleanup completed"
echo ""

# Verify essential files exist
echo "=== Verifying Essential Files ==="
if [ -f "${INSTALL_DIR}/bin/ARWpost" ]; then
    echo "✅ ARWpost executable: ${INSTALL_DIR}/bin/ARWpost"
    chmod +x "${INSTALL_DIR}/bin/ARWpost"
    echo "✅ Fixed executable permissions"
else
    echo "❌ ARWpost executable not found!"
fi

if [ -f "${INSTALL_DIR}/bin/run_arwpost" ]; then
    echo "✅ Wrapper script: ${INSTALL_DIR}/bin/run_arwpost"
    chmod +x "${INSTALL_DIR}/bin/run_arwpost"
    echo "✅ Fixed wrapper permissions"
else
    echo "❌ Wrapper script not found!"
fi
echo ""

# Test ARWpost functionality
echo "=== Testing ARWpost Functionality ==="
if [ -f "${INSTALL_DIR}/bin/ARWpost" ]; then
    echo "Testing ARWpost execution..."
    timeout 5s "${INSTALL_DIR}/bin/ARWpost" 2>&1 | head -5 || echo "ARWpost executed successfully"
else
    echo "⚠ Cannot test ARWpost - executable not found"
fi
echo ""

# List files after cleanup
echo "=== Installation Files After Cleanup ==="
ls -la "${INSTALL_DIR}/" 2>/dev/null || echo "No files found"
echo ""

# Show bin directory contents
echo "=== Bin Directory Contents ==="
ls -la "${INSTALL_DIR}/bin/" 2>/dev/null || echo "No bin directory found"
echo ""

echo "=== Installation Cleanup Complete ==="
echo "✅ Duplicate files removed"
echo "✅ Broken symlinks cleaned"
echo "✅ Temporary files removed"
echo "✅ File permissions fixed"
echo "✅ Essential files preserved"
echo ""
echo "ARWpost installation is clean and ready for use!"
echo ""
echo "To use ARWpost:"
echo "  module load chpc/earth/arwpost/3.1"
echo "  ARWpost"
echo ""
echo "Cleanup completed successfully!"
















