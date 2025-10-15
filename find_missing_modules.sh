#!/bin/bash
# Find Missing ARWpost Modules
# This script searches for the missing modules in the source code

echo "=== Find Missing ARWpost Modules ==="
echo "Searching for missing modules in the source code..."
echo ""

SOURCE_DIR="/home/msovara/lustre/SoftwareBuilds/ARWpost-download"

if [ ! -d "${SOURCE_DIR}/ARWpost" ]; then
    echo "✗ ARWpost source directory not found at: ${SOURCE_DIR}/ARWpost"
    exit 1
fi

cd "${SOURCE_DIR}/ARWpost"

echo "Searching for gridinfo_module..."
echo "Files that contain 'gridinfo_module':"
grep -l "gridinfo_module" src/*.f90 2>/dev/null || echo "No files contain 'gridinfo_module'"

echo ""
echo "Files that contain 'MODULE gridinfo_module':"
grep -l "MODULE gridinfo_module" src/*.f90 2>/dev/null || echo "No files contain 'MODULE gridinfo_module'"

echo ""
echo "Files that contain 'gridinfo_module' (with context):"
grep -n "gridinfo_module" src/*.f90 2>/dev/null || echo "No files contain 'gridinfo_module'"

echo ""
echo "Searching for process_domain_module..."
echo "Files that contain 'process_domain_module':"
grep -l "process_domain_module" src/*.f90 2>/dev/null || echo "No files contain 'process_domain_module'"

echo ""
echo "Files that contain 'MODULE process_domain_module':"
grep -l "MODULE process_domain_module" src/*.f90 2>/dev/null || echo "No files contain 'MODULE process_domain_module'"

echo ""
echo "Files that contain 'process_domain_module' (with context):"
grep -n "process_domain_module" src/*.f90 2>/dev/null || echo "No files contain 'process_domain_module'"

echo ""
echo "Searching for input_module..."
echo "Files that contain 'input_module':"
grep -l "input_module" src/*.f90 2>/dev/null || echo "No files contain 'input_module'"

echo ""
echo "Files that contain 'MODULE input_module':"
grep -l "MODULE input_module" src/*.f90 2>/dev/null || echo "No files contain 'MODULE input_module'"

echo ""
echo "Files that contain 'input_module' (with context):"
grep -n "input_module" src/*.f90 2>/dev/null || echo "No files contain 'input_module'"

echo ""
echo "Searching for output_module..."
echo "Files that contain 'output_module':"
grep -l "output_module" src/*.f90 2>/dev/null || echo "No files contain 'output_module'"

echo ""
echo "Files that contain 'MODULE output_module':"
grep -l "MODULE output_module" src/*.f90 2>/dev/null || echo "No files contain 'MODULE output_module'"

echo ""
echo "Files that contain 'output_module' (with context):"
grep -n "output_module" src/*.f90 2>/dev/null || echo "No files contain 'output_module'"

echo ""
echo "=== Missing Modules Search Complete ==="








