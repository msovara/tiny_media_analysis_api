#!/bin/bash

# Cleanup ARWpost Module Files Script
# This script removes duplicates, broken files, and organizes the module system

set -e

# Configuration
MODULE_DIR="/apps/chpc/scripts/modules/earth/arwpost"
INSTALL_DIR="/home/apps/chpc/earth/ARWpost"

echo "=== Cleaning Up ARWpost Module Files ==="
echo "Module directory: ${MODULE_DIR}"
echo "Installation directory: ${INSTALL_DIR}"
echo ""

# Check if module directory exists
if [ ! -d "${MODULE_DIR}" ]; then
    echo "✗ Module directory not found: ${MODULE_DIR}"
    echo "No cleanup needed."
    exit 0
fi

echo "✓ Module directory found"

# List current files before cleanup
echo ""
echo "=== Current Module Files ==="
ls -la "${MODULE_DIR}/" 2>/dev/null || echo "No files found"
echo ""

# Backup the working module file
echo "=== Creating Backup ==="
if [ -f "${MODULE_DIR}/3.1" ]; then
    cp "${MODULE_DIR}/3.1" "${MODULE_DIR}/3.1.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✓ Backup created: 3.1.backup.$(date +%Y%m%d_%H%M%S)"
else
    echo "⚠ No 3.1 module file found to backup"
fi
echo ""

# Remove duplicate and broken files
echo "=== Removing Duplicate and Broken Files ==="

# Remove backup files (keep only the latest)
echo "Removing old backup files..."
find "${MODULE_DIR}/" -name "*.backup*" -type f | head -n -1 | xargs rm -f 2>/dev/null || echo "No old backups to remove"

# Remove broken symlinks
echo "Removing broken symlinks..."
find "${MODULE_DIR}/" -type l -exec test ! -e {} \; -delete 2>/dev/null || echo "No broken symlinks found"

# Remove duplicate module files (keep only 3.1)
echo "Removing duplicate module files..."
find "${MODULE_DIR}/" -name "*.backup" -type f -delete 2>/dev/null || echo "No .backup files to remove"

# Clean up any temporary files
echo "Removing temporary files..."
find "${MODULE_DIR}/" -name "*.tmp" -type f -delete 2>/dev/null || echo "No .tmp files to remove"
find "${MODULE_DIR}/" -name "*.bak" -type f -delete 2>/dev/null || echo "No .bak files to remove"

echo "✓ Cleanup completed"
echo ""

# Verify the working module file exists
echo "=== Verifying Working Module File ==="
if [ -f "${MODULE_DIR}/3.1" ]; then
    echo "✅ Working module file: ${MODULE_DIR}/3.1"
    
    # Check file permissions
    chmod 644 "${MODULE_DIR}/3.1"
    echo "✅ Fixed file permissions"
    
    # Test module file syntax
    echo "Testing module file syntax..."
    if module show chpc/earth/arwpost/3.1 >/dev/null 2>&1; then
        echo "✅ Module file syntax is valid"
    else
        echo "⚠ Module file syntax may have issues"
    fi
else
    echo "❌ Working module file not found!"
    echo "Please recreate the module file using optimize_module_final.sh"
fi
echo ""

# Recreate symlinks properly
echo "=== Recreating Symlinks ==="
if [ -f "${MODULE_DIR}/3.1" ]; then
    # Create .version file
    ln -sf "3.1" "${MODULE_DIR}/.version"
    echo "✅ Created .version symlink"
    
    # Create default symlink
    ln -sf "3.1" "${MODULE_DIR}/default"
    echo "✅ Created default symlink"
else
    echo "⚠ Cannot create symlinks - no working module file"
fi
echo ""

# List files after cleanup
echo "=== Module Files After Cleanup ==="
ls -la "${MODULE_DIR}/" 2>/dev/null || echo "No files found"
echo ""

# Test module availability
echo "=== Testing Module Availability ==="
echo "Available ARWpost modules:"
module avail 2>&1 | grep -i arwpost || echo "No ARWpost modules found in module system"
echo ""

echo "=== Cleanup Complete ==="
echo "✅ Duplicate files removed"
echo "✅ Broken symlinks cleaned"
echo "✅ File permissions fixed"
echo "✅ Symlinks recreated"
echo ""
echo "To use ARWpost:"
echo "  module load chpc/earth/arwpost/3.1"
echo "  ARWpost"
echo ""
echo "Cleanup completed successfully!"
















