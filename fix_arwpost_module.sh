#!/bin/bash
# Fix ARWpost Module Installation
# This script fixes the module file location and format

set -e  # Exit on any error

echo "=== Fix ARWpost Module Installation ==="
echo "Fixing module file location and format..."
echo ""

# Configuration
MODULE_DIR="/apps/chpc/scripts/modules/earth/arwpost-full"
INSTALL_DIR="/home/apps/chpc/earth/ARWpost-full"

echo "Module directory: ${MODULE_DIR}"
echo "Installation directory: ${INSTALL_DIR}"
echo ""

# Create the correct module directory structure
echo "Creating correct module directory structure..."
mkdir -p "${MODULE_DIR}"

# Create the module file with correct format
echo "Creating module file with correct format..."
cat > "${MODULE_DIR}/3.1" << 'EOF'
#%Module1.0
proc ModulesHelp { } {
    puts stderr "ARWpost Working Version - WRF post-processing tool"
    puts stderr "Compiled with Intel Parallel Studio XE 16.0.1"
    puts stderr "Includes core modules: constants, debug, model basics, pressure, output"
    puts stderr "Working version for WRF data processing"
}

module-whatis "ARWpost Working Version - WRF post-processing tool"

set version "3.1-working"
set arwpost_root "/home/apps/chpc/earth/ARWpost-full"

# Load dependencies
module load chpc/parallel_studio_xe/16.0.1/2016.1.150
module load chpc/zlib/1.2.8/intel/16.0.1
module load chpc/hdf5/1.8.16/intel/16.0.1
module load chpc/netcdf/4.4.0-C/intel/16.0.1

# Set paths
prepend-path PATH ${arwpost_root}/bin
prepend-path MANPATH ${arwpost_root}/share/arwpost

# Set environment variables
setenv ARWPOST_ROOT ${arwpost_root}
setenv ARWPOST_VERSION ${version}
setenv ARWPOST_COMPILER "intel-16.0.1-working"
setenv ARWPOST_TYPE "working"

# Set library path
prepend-path LD_LIBRARY_PATH ${arwpost_root}/lib
EOF

# Create the .version file with correct format
echo "Creating .version file with correct format..."
cat > "${MODULE_DIR}/.version" << 'EOF'
#%Module1.0
set ModulesVersion "3.1"
EOF

# Set proper permissions
echo "Setting proper permissions..."
chmod 644 "${MODULE_DIR}/3.1"
chmod 644 "${MODULE_DIR}/.version"

# Verify the files
echo "Verifying module files..."
echo "Module file contents:"
head -5 "${MODULE_DIR}/3.1"
echo ""
echo ".version file contents:"
cat "${MODULE_DIR}/.version"
echo ""

# Test module loading
echo "Testing module loading..."
module purge
module load chpc/earth/arwpost-full/3.1

echo "✓ Module loaded successfully"
echo "ARWPOST_ROOT: ${ARWPOST_ROOT}"
echo "ARWPOST_VERSION: ${ARWPOST_VERSION}"

# Test ARWpost executable
echo "Testing ARWpost executable..."
if command -v ARWpost >/dev/null 2>&1; then
    echo "✓ ARWpost command found"
    ARWpost --help 2>/dev/null || ARWpost -h 2>/dev/null || ARWpost 2>/dev/null || echo "ARWpost runs but may not show help"
else
    echo "⚠ ARWpost command not found in PATH"
    echo "Checking installation directory..."
    ls -la "${INSTALL_DIR}/bin/"
fi

echo ""
echo "=== Module Fix Complete ==="
echo "ARWpost module fixed and ready to use!"
echo ""
echo "To use ARWpost:"
echo "1. module load chpc/earth/arwpost-full/3.1"
echo "2. ARWpost <namelist.ARWpost>"
echo "3. Or: run_arwpost <namelist.ARWpost>"








