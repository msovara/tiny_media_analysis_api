#!/bin/bash

# Create RLM3D Module File Script
# This script creates a module file for RLM3D in the correct location

set -e

# Configuration
MODULE_DIR="/apps/chpc/scripts/modules/earth/rlm3d"
INSTALL_DIR="/mnt/lustre/users/msovara/SoftwareBuilds/RLM3D"
MODULE_VERSION="2024"

echo "=== Creating RLM3D Module File ==="
echo "Module directory: ${MODULE_DIR}"
echo "Installation directory: ${INSTALL_DIR}"
echo "Module version: ${MODULE_VERSION}"
echo ""

# Check if installation exists
if [ ! -d "${INSTALL_DIR}" ]; then
    echo "✗ RLM3D installation not found at: ${INSTALL_DIR}"
    echo "Please ensure RLM3D is installed in the specified directory."
    echo "Expected structure:"
    echo "  ${INSTALL_DIR}/bin/rlm3d"
    echo "  ${INSTALL_DIR}/lib/"
    echo "  ${INSTALL_DIR}/include/"
    exit 1
fi

# Check for RLM3D executable
if [ ! -f "${INSTALL_DIR}/bin/rlm3d" ]; then
    echo "⚠️  RLM3D executable not found at: ${INSTALL_DIR}/bin/rlm3d"
    echo "Please ensure the RLM3D executable is in the bin directory."
    echo "Continuing with module creation..."
fi

echo "✓ RLM3D installation directory found"

# Create module directory
echo "Creating module directory..."
mkdir -p "${MODULE_DIR}"

# Create the module file
echo "Creating module file..."
cat > "${MODULE_DIR}/${MODULE_VERSION}" << EOF
#%Module1.0
##
## RLM3D ${MODULE_VERSION} module for Lengau Cluster
##

proc ModulesHelp { } {
    puts stderr "This module loads RLM3D ${MODULE_VERSION} (3D Ray Launching Method)."
    puts stderr "Compiled with Intel Parallel Studio XE 2020u1"
    puts stderr ""
    puts stderr "Usage:"
    puts stderr "  rlm3d                    # Run RLM3D"
    puts stderr "  rlm3d -h                 # Show help"
    puts stderr ""
    puts stderr "RLM3D Features:"
    puts stderr "  - 3D Ray Launching Method for electromagnetic propagation"
    puts stderr "  - High-frequency electromagnetic field calculations"
    puts stderr "  - Complex 3D geometry support"
    puts stderr "  - Parallel processing capabilities"
    puts stderr "  - Intel compiler optimization"
    puts stderr ""
    puts stderr "Model Components:"
    puts stderr "  - Ray launching algorithm"
    puts stderr "  - 3D geometry processing"
    puts stderr "  - Electromagnetic field calculations"
    puts stderr "  - Reflection and diffraction modeling"
    puts stderr "  - Parallel execution support"
}

module-whatis "Loads RLM3D ${MODULE_VERSION} - 3D Ray Launching Method"

# Load required modules
module purge
module load chpc/parallel_studio_xe/2020u1

# Set RLM3D environment
set rlm3d_root "${INSTALL_DIR}"
setenv RLM3D_ROOT \$rlm3d_root
setenv RLM3D_VERSION "${MODULE_VERSION}"
setenv RLM3D_COMPILER "intel-2020u1"

# Add to PATH
prepend-path PATH \${rlm3d_root}/bin

# Set library path for runtime
prepend-path LD_LIBRARY_PATH \${rlm3d_root}/lib

# Set include path for development
prepend-path CPATH \${rlm3d_root}/include

# Set OpenMP environment for parallel execution
setenv OMP_NUM_THREADS 1
setenv OMP_STACKSIZE 64M

# Print status message
puts stderr "RLM3D ${MODULE_VERSION} loaded successfully"
puts stderr "Installation: \${RLM3D_ROOT}"
puts stderr "Compiler: \${RLM3D_COMPILER}"
puts stderr "Executable: \$(which rlm3d 2>/dev/null || echo 'rlm3d not found in PATH')"
puts stderr ""
puts stderr "To run RLM3D:"
puts stderr "  rlm3d                    # Direct execution"
puts stderr "  rlm3d -h                 # Show help and options"
puts stderr ""
puts stderr "For parallel execution:"
puts stderr "  export OMP_NUM_THREADS=4    # Set OpenMP threads"
puts stderr "  rlm3d -np 8                 # Parallel execution (if supported)"
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
echo "module load rlm3d/${MODULE_VERSION}"
echo "rlm3d -h"
echo ""

echo "=== Module Creation Complete ==="
echo "Module file: ${MODULE_DIR}/${MODULE_VERSION}"
echo "Default version: ${MODULE_DIR}/.version"
echo ""
echo "To use RLM3D:"
echo "1. Load the module: module load rlm3d/${MODULE_VERSION}"
echo "2. Run RLM3D: rlm3d"
echo "3. For help: rlm3d -h"
echo ""
echo "Module creation completed successfully!"

























