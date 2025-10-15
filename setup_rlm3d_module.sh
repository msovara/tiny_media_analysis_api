#!/bin/bash

# Setup RLM3D Module File for Lengau Cluster
# This script sets up the RLM3D module file in the correct location

set -e

# Configuration
MODULE_DIR="/apps/chpc/scripts/modules/earth/rlm3d"
INSTALL_DIR="/mnt/lustre/users/msovara/SoftwareBuilds/RLM3D"
MODULE_VERSION="3.3.2"
EXECUTABLE_NAME="RLM3D_v3.3.2"

echo "=== Setting up RLM3D Module for Lengau Cluster ==="
echo "Module directory: ${MODULE_DIR}"
echo "Installation directory: ${INSTALL_DIR}"
echo "Module version: ${MODULE_VERSION}"
echo "Executable: ${EXECUTABLE_NAME}"
echo ""

# Check if we're on the cluster
if [ ! -d "/apps/chpc" ]; then
    echo "⚠️  This script should be run on the Lengau cluster"
    echo "Please run this script on the cluster where /apps/chpc exists"
    exit 1
fi

# Create installation directory structure
echo "Creating RLM3D installation directory..."
mkdir -p "${INSTALL_DIR}/bin"
mkdir -p "${INSTALL_DIR}/lib"
mkdir -p "${INSTALL_DIR}/include"

# Check if RLM3D executable exists in current directory
if [ -f "./${EXECUTABLE_NAME}" ]; then
    echo "✓ Found RLM3D executable: ./${EXECUTABLE_NAME}"
    echo "Copying executable to installation directory..."
    cp "./${EXECUTABLE_NAME}" "${INSTALL_DIR}/bin/"
    chmod +x "${INSTALL_DIR}/bin/${EXECUTABLE_NAME}"
    echo "✓ Executable copied and made executable"
else
    echo "⚠️  RLM3D executable not found in current directory"
    echo "Please ensure ${EXECUTABLE_NAME} is in the current directory"
    echo "Continuing with module setup..."
fi

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
    puts stderr "  RLM3D_v3.3.2              # Run RLM3D"
    puts stderr "  RLM3D_v3.3.2 -h           # Show help"
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
puts stderr "Installation: \\\$RLM3D_ROOT"
puts stderr "Compiler: \\\$RLM3D_COMPILER"
puts stderr "Executable: \$(which RLM3D_v3.3.2 2>/dev/null || echo 'RLM3D_v3.3.2 not found in PATH')"
puts stderr ""
puts stderr "To run RLM3D:"
puts stderr "  RLM3D_v3.3.2              # Direct execution"
puts stderr "  RLM3D_v3.3.2 -h           # Show help and options"
puts stderr ""
puts stderr "For parallel execution:"
puts stderr "  export OMP_NUM_THREADS=4    # Set OpenMP threads"
puts stderr "  RLM3D_v3.3.2 -np 8         # Parallel execution (if supported)"
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
echo "RLM3D_v3.3.2 -h"
echo ""

echo "=== Module Setup Complete ==="
echo "Module file: ${MODULE_DIR}/${MODULE_VERSION}"
echo "Default version: ${MODULE_DIR}/.version"
echo "Installation: ${INSTALL_DIR}"
echo ""
echo "To use RLM3D:"
echo "1. Load the module: module load rlm3d/${MODULE_VERSION}"
echo "2. Run RLM3D: RLM3D_v3.3.2"
echo "3. For help: RLM3D_v3.3.2 -h"
echo ""
echo "Module setup completed successfully!"
