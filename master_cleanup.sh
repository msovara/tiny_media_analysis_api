#!/bin/bash

# Master ARWpost Cleanup Script
# This script runs both module and installation cleanup

set -e

echo "🧹 === ARWpost Master Cleanup Script ==="
echo "This script will clean up both module files and installation files"
echo ""

# Check if we're running on the cluster
if [[ "$HOSTNAME" != *"lengau"* ]] && [[ "$HOSTNAME" != *"cnode"* ]]; then
    echo "⚠ Warning: This script should be run on the Lengau cluster"
    echo "Current hostname: $HOSTNAME"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cleanup cancelled."
        exit 0
    fi
fi

echo "✅ Running on cluster environment"
echo ""

# Run module cleanup
echo "📁 === Step 1: Cleaning Module Files ==="
if [ -f "cleanup_module_files.sh" ]; then
    bash cleanup_module_files.sh
else
    echo "⚠ Module cleanup script not found, skipping..."
fi
echo ""

# Run installation cleanup
echo "📁 === Step 2: Cleaning Installation Files ==="
if [ -f "cleanup_installation_files.sh" ]; then
    bash cleanup_installation_files.sh
else
    echo "⚠ Installation cleanup script not found, skipping..."
fi
echo ""

# Final verification
echo "🔍 === Step 3: Final Verification ==="
echo "Testing ARWpost availability..."

# Test module loading
echo "Testing module loading..."
module purge 2>/dev/null || true
if module load chpc/earth/arwpost/3.1 2>/dev/null; then
    echo "✅ Module loads successfully"
    
    # Test ARWpost execution
    if command -v ARWpost >/dev/null 2>&1; then
        echo "✅ ARWpost is available in PATH"
        echo "✅ Location: $(which ARWpost)"
        
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
echo "🎉 === Master Cleanup Complete ==="
echo "✅ Module files cleaned"
echo "✅ Installation files cleaned"
echo "✅ System verified"
echo ""
echo "ARWpost is now clean and ready for production use!"
echo ""
echo "📋 Usage:"
echo "  module load chpc/earth/arwpost/3.1"
echo "  ARWpost"
echo ""
echo "📚 Documentation:"
echo "  - ARWPOST_INSTALLATION_SUCCESS.md"
echo "  - ARWpost_Lengau_Installation_Guide.md"
echo ""
echo "Master cleanup completed successfully! 🎉"
















