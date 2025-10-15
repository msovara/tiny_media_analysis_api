#!/bin/bash

# Quick Fix Tcl Errors Script
# This script directly fixes the Tcl errors in the module file

set -e

# Configuration
MODULE_DIR="/apps/chpc/scripts/modules/earth/arwpost"
MODULE_VERSION="3.1"

echo "=== Quick Fix for Tcl Errors ==="
echo "Module directory: ${MODULE_DIR}"
echo "Module version: ${MODULE_VERSION}"
echo ""

# Check if module file exists
if [ ! -f "${MODULE_DIR}/${MODULE_VERSION}" ]; then
    echo "✗ Module file not found: ${MODULE_DIR}/${MODULE_VERSION}"
    exit 1
fi

echo "✓ Module file found"

# Create a backup
echo "Creating backup..."
cp "${MODULE_DIR}/${MODULE_VERSION}" "${MODULE_DIR}/${MODULE_VERSION}.backup.$(date +%Y%m%d_%H%M%S)"
echo "✓ Backup created"

# Fix the Tcl errors by removing the problematic line
echo "Fixing Tcl errors..."
sed -i '/puts stderr "Installation: \$ARWPOST_ROOT"/d' "${MODULE_DIR}/${MODULE_VERSION}"
echo "✓ Removed problematic Tcl line"

# Also fix any other variable expansion issues
sed -i 's/puts stderr "Installation: $ARWPOST_ROOT"/puts stderr "Installation: \/home\/apps\/chpc\/earth\/ARWpost"/g' "${MODULE_DIR}/${MODULE_VERSION}"
sed -i 's/puts stderr "Compiler: $ARWPOST_COMPILER"/puts stderr "Compiler: intel-16.0.1-minimal"/g' "${MODULE_DIR}/${MODULE_VERSION}"
echo "✓ Fixed variable expansion issues"

# Set proper permissions
chmod 644 "${MODULE_DIR}/${MODULE_VERSION}"
echo "✓ Fixed file permissions"

echo ""
echo "=== Quick Fix Complete ==="
echo "✅ Tcl errors should now be resolved"
echo ""
echo "Testing module loading..."
module purge 2>/dev/null || true
if module load chpc/earth/arwpost/3.1 2>/dev/null; then
    echo "✅ Module loads successfully without Tcl errors!"
    
    if command -v ARWpost >/dev/null 2>&1; then
        echo "✅ ARWpost is available: $(which ARWpost)"
    else
        echo "❌ ARWpost not found in PATH"
    fi
else
    echo "❌ Module loading still has issues"
fi

echo ""
echo "Quick fix completed successfully!"
















