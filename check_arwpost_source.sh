#!/bin/bash
# Check ARWpost Source Files
# This script checks what source files are available in the ARWpost directory

echo "=== ARWpost Source File Check ==="
echo "Checking available source files..."
echo ""

SOURCE_DIR="/home/msovara/lustre/SoftwareBuilds/ARWpost-download"

if [ ! -d "${SOURCE_DIR}/ARWpost" ]; then
    echo "✗ ARWpost source directory not found at: ${SOURCE_DIR}/ARWpost"
    exit 1
fi

echo "Source directory: ${SOURCE_DIR}/ARWpost"
echo ""

# Check for source files
echo "Checking for source files..."
cd "${SOURCE_DIR}/ARWpost"

if [ -d "src" ]; then
    echo "✓ src directory found"
    echo "Source files in src directory:"
    ls -la src/*.f90 2>/dev/null || echo "No .f90 files found"
    ls -la src/*.f 2>/dev/null || echo "No .f files found"
    echo ""
    
    # Check for specific modules
    echo "Checking for specific modules:"
    echo "gridinfo_module.f90: $(ls src/gridinfo_module.f90 2>/dev/null || echo 'NOT FOUND')"
    echo "process_domain_module.f90: $(ls src/process_domain_module.f90 2>/dev/null || echo 'NOT FOUND')"
    echo "input_module.f90: $(ls src/input_module.f90 2>/dev/null || echo 'NOT FOUND')"
    echo "output_module.f90: $(ls src/output_module.f90 2>/dev/null || echo 'NOT FOUND')"
    echo "ARWpost.f90: $(ls src/ARWpost.f90 2>/dev/null || echo 'NOT FOUND')"
    echo ""
    
    # Check for configure script
    echo "Checking for configure script:"
    echo "configure: $(ls configure 2>/dev/null || echo 'NOT FOUND')"
    echo ""
    
    # Check for Makefile
    echo "Checking for Makefile:"
    echo "Makefile: $(ls Makefile 2>/dev/null || echo 'NOT FOUND')"
    echo ""
    
    # List all source files
    echo "All source files:"
    find src -name "*.f90" -o -name "*.f" | sort
    echo ""
    
else
    echo "✗ src directory not found"
    echo "Directory contents:"
    ls -la
fi

echo "=== Source File Check Complete ==="









