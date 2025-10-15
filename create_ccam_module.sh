#!/bin/bash

# Create CCAM Module File Script
# This script creates a module file for CCAM in the correct location

set -e

# Configuration
MODULE_DIR="/apps/chpc/scripts/modules/earth/ccam"
INSTALL_DIR="/mnt/lustre/users/msovara/SoftwareBuilds/CCAM"
MODULE_VERSION="2023"

echo "=== Creating CCAM Module File ==="
echo "Module directory: ${MODULE_DIR}"
echo "Installation directory: ${INSTALL_DIR}"
echo "Module version: ${MODULE_VERSION}"
echo ""

# Check if installation exists
if [ ! -d "${INSTALL_DIR}" ]; then
    echo "✗ CCAM installation not found at: ${INSTALL_DIR}"
    echo "Please run the installation script first."
    exit 1
fi

echo "✓ CCAM installation found"

# Create module directory
echo "Creating module directory..."
mkdir -p "${MODULE_DIR}"

# Create the module file
echo "Creating module file..."
cat > "${MODULE_DIR}/${MODULE_VERSION}" << EOF
#%Module1.0
##
## CCAM ${MODULE_VERSION} module for Lengau Cluster
##

proc ModulesHelp { } {
    puts stderr "This module loads CCAM ${MODULE_VERSION} (Conformal Cubic Atmospheric Model)."
    puts stderr "Compiled with Intel Parallel Studio XE 2018.2.046"
    puts stderr "NetCDF: Compatible with CHPC NetCDF modules"
    puts stderr ""
    puts stderr "Usage:"
    puts stderr "  ccam                    # Run CCAM"
    puts stderr "  ccam -h                 # Show help"
    puts stderr ""
    puts stderr "CCAM Features:"
    puts stderr "  - Conformal cubic grid for global atmospheric modeling"
    puts stderr "  - High-resolution climate simulations"
    puts stderr "  - Regional downscaling capabilities"
    puts stderr "  - OpenMP parallelization"
    puts stderr "  - MPI support for distributed computing"
    puts stderr ""
    puts stderr "Model Components:"
    puts stderr "  - Atmospheric dynamics"
    puts stderr "  - Radiation scheme"
    puts stderr "  - Land surface model"
    puts stderr "  - Ocean coupling (if enabled)"
    puts stderr "  - Aerosol and chemistry modules"
}

module-whatis "Loads CCAM ${MODULE_VERSION} - Conformal Cubic Atmospheric Model"

# Load required modules
module purge
module load chpc/parallel_studio_xe/18.0.2/2018.2.046
module load chpc/netcdf/4.7.4
module load chpc/hdf5/1.12.0

# Set CCAM environment
set ccam_root "${INSTALL_DIR}"
setenv CCAM_ROOT \$ccam_root
setenv CCAM_VERSION "${MODULE_VERSION}"
setenv CCAM_COMPILER "intel-2018.2.046"

# Add to PATH
prepend-path PATH \${ccam_root}/bin

# Set library path for runtime
prepend-path LD_LIBRARY_PATH \${ccam_root}/lib

# Set OpenMP environment
setenv OMP_NUM_THREADS 1
setenv OMP_STACKSIZE 64M

# Print status message
puts stderr "CCAM ${MODULE_VERSION} loaded successfully"
puts stderr "Installation: \${CCAM_ROOT}"
puts stderr "Compiler: \${CCAM_COMPILER}"
puts stderr "Executable: \$(which ccam 2>/dev/null || echo 'ccam not found in PATH')"
puts stderr ""
puts stderr "To run CCAM:"
puts stderr "  ccam                    # Direct execution"
puts stderr "  ccam -h                 # Show help and options"
puts stderr ""
puts stderr "For parallel execution:"
puts stderr "  export OMP_NUM_THREADS=4    # Set OpenMP threads"
puts stderr "  mpirun -np 8 ccam           # MPI parallel execution"
EOF

echo "✓ Module file created: ${MODULE_DIR}/${MODULE_VERSION}"

# Set proper permissions
chmod 644 "${MODULE_DIR}/${MODULE_VERSION}"

# Create a default module file (latest version)
echo "Creating default module file..."
ln -sf "${MODULE_VERSION}" "${MODULE_DIR}/.version"

# Test the module
echo ""
echo "=== Testing Module ==="
echo "To test the module, run:"
echo "module load ccam/${MODULE_VERSION}"
echo "ccam -h"
echo ""

echo "=== Module Creation Complete ==="
echo "Module file: ${MODULE_DIR}/${MODULE_VERSION}"
echo "Default version: ${MODULE_DIR}/.version"
echo ""
echo "To use CCAM:"
echo "1. Load the module: module load ccam/${MODULE_VERSION}"
echo "2. Run CCAM: ccam"
echo "3. For help: ccam -h"
echo ""
echo "Module creation completed successfully!"




























