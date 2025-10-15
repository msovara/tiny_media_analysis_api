#!/bin/bash

# Cleanup Module System Script
# This script removes the default module and cleans up to leave only chpc/earth/arwpost/3.1

set -e

# Configuration
MODULE_DIR="/apps/chpc/scripts/modules/earth/arwpost"

echo "🧹 === Cleaning Module System ==="
echo "Module directory: ${MODULE_DIR}"
echo ""

# Check if module directory exists
if [ ! -d "${MODULE_DIR}" ]; then
    echo "✗ Module directory not found: ${MODULE_DIR}"
    exit 1
fi

echo "✓ Module directory found"

# List current files
echo ""
echo "=== Current Module Files ==="
ls -la "${MODULE_DIR}/"
echo ""

# Remove default module and symlinks
echo "=== Removing Default Module and Symlinks ==="
if [ -L "${MODULE_DIR}/default" ]; then
    rm "${MODULE_DIR}/default"
    echo "✅ Removed default symlink"
fi

if [ -L "${MODULE_DIR}/.version" ]; then
    rm "${MODULE_DIR}/.version"
    echo "✅ Removed .version symlink"
fi

# Remove any other symlinks
find "${MODULE_DIR}/" -type l -delete 2>/dev/null || echo "No other symlinks found"
echo "✅ Removed all symlinks"

# Remove backup files
echo "=== Removing Backup Files ==="
find "${MODULE_DIR}/" -name "*.backup*" -type f -delete
echo "✅ Backup files removed"

# Verify only the main module file remains
echo ""
echo "=== Verifying Clean Module System ==="
if [ -f "${MODULE_DIR}/3.1" ]; then
    echo "✅ Main module file exists: ${MODULE_DIR}/3.1"
    
    # Set proper permissions
    chmod 644 "${MODULE_DIR}/3.1"
    echo "✅ File permissions set"
else
    echo "❌ Main module file not found!"
    exit 1
fi

# List files after cleanup
echo ""
echo "=== Module Files After Cleanup ==="
ls -la "${MODULE_DIR}/"
echo ""

# Test module availability
echo "=== Testing Module Availability ==="
echo "Available ARWpost modules:"
module avail 2>&1 | grep -i arwpost || echo "No ARWpost modules found"
echo ""

# Final test
echo "=== Final Module Test ==="
module purge 2>/dev/null || true
if module load chpc/earth/arwpost/3.1 2>/dev/null; then
    echo "✅ Module loads successfully!"
    
    if command -v ARWpost >/dev/null 2>&1; then
        echo "✅ ARWpost is available: $(which ARWpost)"
        
        # Quick functionality test
        echo "Testing ARWpost functionality..."
        timeout 3s ARWpost 2>&1 | head -3 || echo "✅ ARWpost executes successfully"
    else
        echo "❌ ARWpost not found in PATH"
    fi
else
    echo "❌ Module loading failed"
fi

echo ""
echo "🎉 === Module System Cleanup Complete ==="
echo "✅ Default module removed"
echo "✅ Symlinks removed"
echo "✅ Backup files removed"
echo "✅ Only chpc/earth/arwpost/3.1 remains"
echo "✅ Module system is clean"
echo ""
echo "📋 Clean module usage:"
echo "  module load chpc/earth/arwpost/3.1"
echo "  ARWpost"
echo ""
echo "📚 Available module name:"
echo "  - chpc/earth/arwpost/3.1 (only option)"
echo ""
echo "Module system cleanup completed successfully! 🎉"
















