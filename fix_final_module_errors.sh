#!/bin/bash

# Fix Final Module Errors Script
# This script fixes the remaining Tcl syntax errors in the module file

set -e

# Configuration
MODULE_DIR="/apps/chpc/scripts/modules/earth/arwpost"
INSTALL_DIR="/home/apps/chpc/earth/ARWpost"
MODULE_VERSION="3.1"

echo "=== Fixing Final Module Errors ==="
echo "Module directory: ${MODULE_DIR}"
echo "Installation directory: ${INSTALL_DIR}"
echo "Module version: ${MODULE_VERSION}"
echo ""

# Check if installation exists
if [ ! -f "${INSTALL_DIR}/bin/ARWpost" ]; then
    echo "✗ ARWpost installation not found at: ${INSTALL_DIR}/bin/ARWpost"
    echo "Please run the installation script first."
    exit 1
fi

echo "✓ ARWpost installation found"

# Create module directory
echo "Creating module directory..."
mkdir -p "${MODULE_DIR}"

# Create the completely fixed module file with proper Tcl syntax
echo "Creating final fixed module file..."
cat > "${MODULE_DIR}/${MODULE_VERSION}" << 'EOF'
#%Module1.0
##
## ARWpost 3.1 module for Lengau Cluster
##

proc ModulesHelp { } {
    puts stderr "This module loads ARWpost 3.1 (WRF post-processing tool)."
    puts stderr "Compiled with Intel Parallel Studio XE 16.0.1"
    puts stderr "NetCDF: /apps/chpc/earth/netcdf-4.1.3-intel2016"
    puts stderr ""
    puts stderr "Usage:"
    puts stderr "  ARWpost                    # Run ARWpost"
    puts stderr "  run_arwpost               # Run with wrapper script"
    puts stderr ""
    puts stderr "Available calculation modules:"
    puts stderr "  - CAPE (Convective Available Potential Energy)"
    puts stderr "  - Cloud fraction"
    puts stderr "  - Radar reflectivity (dBZ)"
    puts stderr "  - Height calculations"
    puts stderr "  - Pressure calculations"
    puts stderr "  - Relative humidity (surface and 2m)"
    puts stderr "  - Sea level pressure"
    puts stderr "  - Temperature conversions"
    puts stderr "  - Dew point (surface and 2m)"
    puts stderr "  - Potential temperature"
    puts stderr "  - Kinetic energy"
    puts stderr "  - Wind components (u, v)"
    puts stderr "  - Wind direction"
    puts stderr "  - Wind speed"
}

module-whatis "Loads ARWpost 3.1 - WRF post-processing tool"

# Load required modules in most compatible order
module purge
module load chpc/parallel_studio_xe/16.0.1/2016.1.150
module load chpc/zlib/1.2.8/intel/16.0.1
module load chpc/hdf5/1.8.16/intel/16.0.1
module load chpc/netcdf/4.4.0-C/intel/16.0.1

# Set ARWpost environment
set arwpost_root "/home/apps/chpc/earth/ARWpost"
setenv ARWPOST_ROOT $arwpost_root
setenv ARWPOST_VERSION "3.1"
setenv ARWPOST_COMPILER "intel-16.0.1-minimal"

# Add to PATH
prepend-path PATH $arwpost_root/bin

# Set library path for runtime
prepend-path LD_LIBRARY_PATH "/apps/chpc/earth/netcdf-4.1.3-intel2016/lib"

# Print status message - using simple puts without variable expansion
puts stderr "ARWpost 3.1 loaded successfully"
puts stderr "Installation: /home/apps/chpc/earth/ARWpost"
puts stderr "Compiler: intel-16.0.1-minimal"
puts stderr "Executable: ARWpost"
puts stderr ""
puts stderr "To run ARWpost:"
puts stderr "  ARWpost                    # Direct execution"
puts stderr "  run_arwpost               # With wrapper script"
EOF

echo "✓ Final fixed module file created: ${MODULE_DIR}/${MODULE_VERSION}"

# Set proper permissions
chmod 644 "${MODULE_DIR}/${MODULE_VERSION}"

# Create a default module file (latest version)
echo "Creating default module file..."
ln -sf "${MODULE_VERSION}" "${MODULE_DIR}/.version"

# Also create a symlink for easier access
echo "Creating symlink for easier access..."
ln -sf "${MODULE_DIR}/${MODULE_VERSION}" "${MODULE_DIR}/default"

echo ""
echo "=== Final Module Fix Complete ==="
echo "Key fixes applied:"
echo "1. ✅ Removed all variable expansion in puts stderr commands"
echo "2. ✅ Used hardcoded paths instead of variables"
echo "3. ✅ Simplified Tcl syntax to avoid errors"
echo "4. ✅ Maintained all functionality"
echo ""
echo "=== Testing Instructions ==="
echo "To test the final fixed module:"
echo "1. module purge"
echo "2. module load chpc/earth/arwpost/3.1"
echo "3. ARWpost"
echo ""
echo "Expected result: Clean loading with NO Tcl errors!"
echo ""
echo "Module fix completed successfully!"
















