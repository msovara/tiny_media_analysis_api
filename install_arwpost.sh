#!/bin/bash
# ARWpost Installation Script for Lengau Cluster
# This script installs the compiled ARWpost to the system

set -e  # Exit on any error

# Configuration
BUILD_DIR="/home/apps/chpc/earth/ARWpost-build"
INSTALL_DIR="/home/apps/chpc/earth/ARWpost-complete"

echo "=== ARWpost Installation Script ==="
echo "Build directory: ${BUILD_DIR}"
echo "Installation directory: ${INSTALL_DIR}"
echo ""

# Check if build exists
if [ ! -f "${BUILD_DIR}/ARWpost" ]; then
    echo "✗ ARWpost executable not found at ${BUILD_DIR}/ARWpost"
    echo "Please run build_arwpost.sh first"
    exit 1
fi

echo "✓ ARWpost executable found"

# Create installation directory
mkdir -p "${INSTALL_DIR}"
mkdir -p "${INSTALL_DIR}/bin"
mkdir -p "${INSTALL_DIR}/share/arwpost"
mkdir -p "${INSTALL_DIR}/examples"
mkdir -p "${INSTALL_DIR}/lib"

# Install ARWpost
echo "Installing ARWpost..."
cp "${BUILD_DIR}/ARWpost" "${INSTALL_DIR}/bin/"

# Copy source files
if [ -d "${BUILD_DIR}/src" ]; then
    cp -r "${BUILD_DIR}/src" "${INSTALL_DIR}/share/arwpost/"
fi

# Copy scripts
if [ -d "${BUILD_DIR}/scripts" ]; then
    cp -r "${BUILD_DIR}/scripts" "${INSTALL_DIR}/share/arwpost/"
fi

# Copy examples
if [ -f "${BUILD_DIR}/namelist.ARWpost" ]; then
    cp "${BUILD_DIR}/namelist.ARWpost" "${INSTALL_DIR}/examples/"
fi

if [ -f "${BUILD_DIR}/README" ]; then
    cp "${BUILD_DIR}/README" "${INSTALL_DIR}/share/arwpost/"
fi

# Create wrapper script
cat > "${INSTALL_DIR}/bin/run_arwpost" << 'EOF'
#!/bin/bash
# Wrapper script for complete ARWpost with correct library paths

# Set library paths
export LD_LIBRARY_PATH="/apps/chpc/earth/netcdf-4.1.3-intel2016/lib:${LD_LIBRARY_PATH}"

# Run ARWpost
exec "${0%/*}/ARWpost" "$@"
EOF
chmod +x "${INSTALL_DIR}/bin/run_arwpost"

# Create comprehensive module file
mkdir -p "${INSTALL_DIR}/modulefiles"
cat > "${INSTALL_DIR}/modulefiles/arwpost-complete" << EOF
#%Module1.0
proc ModulesHelp { } {
    puts stderr "ARWpost Complete Version - Full WRF post-processing tool"
    puts stderr "Compiled with Intel Parallel Studio XE 16.0.1"
    puts stderr "Includes all modules: interpolation, diagnostics, output, processing"
    puts stderr "Production-ready for WRF data processing"
}

module-whatis "ARWpost Complete Version - Full WRF post-processing tool"

set version "3.1-complete"
set arwpost_root "${INSTALL_DIR}"

# Load dependencies
module load chpc/parallel_studio_xe/16.0.1/2016.1.150
module load chpc/zlib/1.2.8/intel/16.0.1
module load chpc/hdf5/1.8.16/intel/16.0.1
module load chpc/netcdf/4.4.0-C/intel/16.0.1

# Set paths
prepend-path PATH \${arwpost_root}/bin
prepend-path MANPATH \${arwpost_root}/share/arwpost

# Set environment variables
setenv ARWPOST_ROOT \${arwpost_root}
setenv ARWPOST_VERSION \${version}
setenv ARWPOST_COMPILER "intel-16.0.1-complete"
setenv ARWPOST_TYPE "complete"

# Set library path
prepend-path LD_LIBRARY_PATH \${arwpost_root}/lib
EOF

# Create system module file
mkdir -p /apps/chpc/scripts/modules/earth/arwpost-complete
cp "${INSTALL_DIR}/modulefiles/arwpost-complete" /apps/chpc/scripts/modules/earth/arwpost-complete/3.1

# Create default version
echo "3.1" > /apps/chpc/scripts/modules/earth/arwpost-complete/.version

# Create symlink for easier access
ln -sf /apps/chpc/scripts/modules/earth/arwpost-complete/3.1 /apps/chpc/scripts/modules/earth/arwpost-complete/default

# Installation log
cat > "${INSTALL_DIR}/install_log.txt" << EOF
ARWpost Complete Installation Log
================================
Installation Date: $(date)
Installation Directory: ${INSTALL_DIR}
Build Directory: ${BUILD_DIR}
Compiler: Intel Parallel Studio XE 16.0.1
NetCDF: /apps/chpc/earth/netcdf-4.1.3-intel2016
HDF5: /apps/libs/hdf5/1.8.16
Compilation Method: Complete compilation with all modules

Modules installed:
- Core modules: constants, misc_definitions, module_debug, module_model_basics
- Secondary modules: gridinfo, input, module_arrays, module_basic_arrays, module_map_utils, module_date_pack
- Calculation modules: CAPE, cloud fraction, dBZ, height, pressure, RH, SLP, temperature, dew point, theta, kinetic energy, wind
- Complex modules: interpolation, diagnostics, output, process_domain

Installation completed successfully!
EOF

# Create usage examples
cat > "${INSTALL_DIR}/examples/usage_examples.txt" << EOF
ARWpost Usage Examples
=====================

1. Basic Usage:
   module load chpc/earth/arwpost-complete/3.1
   ARWpost

2. Using Wrapper Script:
   module load chpc/earth/arwpost-complete/3.1
   run_arwpost

3. Processing WRF Data:
   module load chpc/earth/arwpost-complete/3.1
   ARWpost < namelist.ARWpost

4. Check Installation:
   module load chpc/earth/arwpost-complete/3.1
   which ARWpost
   ARWpost --help

5. Environment Variables:
   echo \$ARWPOST_ROOT
   echo \$ARWPOST_VERSION
   echo \$ARWPOST_TYPE
EOF

echo ""
echo "=== ARWpost Installation Complete ==="
echo "ARWpost installed to: ${INSTALL_DIR}"
echo "Module file: /apps/chpc/scripts/modules/earth/arwpost-complete/3.1"
echo "Wrapper script: ${INSTALL_DIR}/bin/run_arwpost"
echo "Usage examples: ${INSTALL_DIR}/examples/usage_examples.txt"
echo ""
echo "To use ARWpost:"
echo "1. Load the module: module load chpc/earth/arwpost-complete/3.1"
echo "2. Run ARWpost: ARWpost"
echo "3. Or use wrapper: run_arwpost"
echo ""
echo "Next steps:"
echo "1. Run: ./test_arwpost.sh"
echo "2. Test with your WRF data"
echo ""
echo "ARWpost installation completed successfully!"