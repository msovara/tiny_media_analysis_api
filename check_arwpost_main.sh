#!/bin/bash
# Check ARWpost Main Program Dependencies
# This script examines what modules the main program actually needs

echo "=== ARWpost Main Program Dependencies ==="
echo "Checking what modules the main program needs..."
echo ""

SOURCE_DIR="/home/msovara/lustre/SoftwareBuilds/ARWpost-download"

if [ ! -f "${SOURCE_DIR}/ARWpost/src/ARWpost.f90" ]; then
    echo "✗ Main program not found at: ${SOURCE_DIR}/ARWpost/src/ARWpost.f90"
    exit 1
fi

echo "Examining main program: ${SOURCE_DIR}/ARWpost/src/ARWpost.f90"
echo ""

# Show the first 20 lines to see what modules it uses
echo "First 20 lines of ARWpost.f90:"
head -20 "${SOURCE_DIR}/ARWpost/src/ARWpost.f90"
echo ""

# Look for USE statements
echo "Modules used by main program:"
grep -n "USE " "${SOURCE_DIR}/ARWpost/src/ARWpost.f90" || echo "No USE statements found"
echo ""

# Look for module dependencies in all source files
echo "Checking for module dependencies in all source files..."
cd "${SOURCE_DIR}/ARWpost"

echo "Files that contain 'gridinfo_module':"
grep -l "gridinfo_module" src/*.f90 2>/dev/null || echo "No files contain 'gridinfo_module'"

echo "Files that contain 'process_domain_module':"
grep -l "process_domain_module" src/*.f90 2>/dev/null || echo "No files contain 'process_domain_module'"

echo "Files that contain 'input_module':"
grep -l "input_module" src/*.f90 2>/dev/null || echo "No files contain 'input_module'"

echo "Files that contain 'output_module':"
grep -l "output_module" src/*.f90 2>/dev/null || echo "No files contain 'output_module'"

echo ""
echo "=== Main Program Dependencies Check Complete ==="








