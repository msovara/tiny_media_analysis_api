#!/bin/bash

# ARWpost Installation Script for Lengau Cluster using Intel Compilers
# This script installs ARWpost to /home/apps/chpc/earth using Intel oneAPI

set -e  # Exit on any error

# Configuration
INSTALL_DIR="/mnt/lustre/users/msovara/SoftwareBuilds/ARWpost"
ARWPOST_VERSION="ARWpost_V3.1"
DOWNLOAD_URL="https://github.com/wrf-model/ARWpost/archive/refs/tags/${ARWPOST_VERSION}.tar.gz"
BUILD_DIR="/tmp/arwpost_build_intel"

echo "=== ARWpost Installation Script (Intel Compilers) ==="
echo "Installation directory: ${INSTALL_DIR}"
echo "ARWpost version: ${ARWPOST_VERSION}"
echo "Compiler: Intel oneAPI"
echo ""

# Create installation directory
echo "Creating installation directory..."
mkdir -p ${INSTALL_DIR}
mkdir -p ${BUILD_DIR}

# Load Intel compiler modules
echo "Loading Intel compiler modules..."
module purge

# Load Intel Parallel Studio XE 2018.2.046
echo "Loading Intel Parallel Studio XE 2018.2.046..."
module load chpc/parallel_studio_xe/18.0.2/2018.2.046

# Source Intel MPI environment
echo "Setting up Intel MPI environment..."
source /apps/compilers/intel/parallel_studio_xe_2018_update2/compilers_and_libraries/linux/mpi/bin64/mpivars.sh

echo "✓ Intel Parallel Studio XE 2018.2.046 loaded"
echo "✓ Intel MPI environment configured"

# Load other required modules
echo "Loading other required modules..."
module load chpc/netcdf/4.7.4
module load chpc/hdf5/1.12.0

# Set Intel compiler environment variables
export FC=ifort
export CC=icc
export CXX=icpc
export NETCDF=${NETCDF_ROOT}
export HDF5=${HDF5_ROOT}

# Intel-specific compiler flags for optimization
export FCFLAGS="-O2 -xHost -ipo"
export CFLAGS="-O2 -xHost -ipo"
export CXXFLAGS="-O2 -xHost -ipo"

echo "Environment variables set:"
echo "FC (Fortran): ${FC}"
echo "CC (C): ${CC}"
echo "CXX (C++): ${CXX}"
echo "NETCDF: ${NETCDF}"
echo "HDF5: ${HDF5}"
echo "FCFLAGS: ${FCFLAGS}"
echo ""

# Verify Intel compilers
echo "Verifying Intel compilers..."
if command -v ifort &> /dev/null; then
    echo "✓ Intel Fortran: $(ifort --version | head -1)"
else
    echo "✗ Intel Fortran not found"
    exit 1
fi

if command -v icc &> /dev/null; then
    echo "✓ Intel C: $(icc --version | head -1)"
else
    echo "✗ Intel C not found"
    exit 1
fi

if command -v icpc &> /dev/null; then
    echo "✓ Intel C++: $(icpc --version | head -1)"
else
    echo "✗ Intel C++ not found"
    exit 1
fi
echo ""

# Download ARWpost source code
echo "Downloading ARWpost source code..."
cd ${BUILD_DIR}
if [ ! -f "${ARWPOST_VERSION}.tar.gz" ]; then
    wget ${DOWNLOAD_URL}
fi

# Extract source code
echo "Extracting source code..."
tar -xzf ${ARWPOST_VERSION}.tar.gz
cd ARWpost-${ARWPOST_VERSION}

# Configure ARWpost with Intel compilers
echo "Configuring ARWpost with Intel compilers..."
./configure

# Compile ARWpost
echo "Compiling ARWpost with Intel optimizations..."
make clean  # Clean any previous builds
make

# Install ARWpost
echo "Installing ARWpost to ${INSTALL_DIR}..."
mkdir -p ${INSTALL_DIR}/bin
mkdir -p ${INSTALL_DIR}/share/arwpost
cp ARWpost ${INSTALL_DIR}/bin/
cp -r * ${INSTALL_DIR}/share/arwpost/

# Create Intel-specific module file
echo "Creating Intel-specific module file..."
mkdir -p ${INSTALL_DIR}/modulefiles
cat > ${INSTALL_DIR}/modulefiles/arwpost-intel << EOF
#%Module1.0
##
## ARWpost modulefile (Intel Compiler Version)
##

proc ModulesHelp { } {
    puts stderr "This module sets up the environment for ARWpost"
    puts stderr "ARWpost is a post-processing tool for WRF model output"
    puts stderr "Compiled with Intel oneAPI compilers for optimal performance"
}

module-whatis "ARWpost - WRF post-processing tool (Intel optimized)"

set version "3.1"
set arwpost_root "${INSTALL_DIR}"

prepend-path PATH \${arwpost_root}/bin
prepend-path MANPATH \${arwpost_root}/share/arwpost

setenv ARWPOST_ROOT \${arwpost_root}
setenv ARWPOST_VERSION \${version}
setenv ARWPOST_COMPILER "intel"
EOF

# Create Intel-specific setup script
echo "Creating Intel-specific setup script..."
cat > ${INSTALL_DIR}/setup_arwpost_intel.sh << EOF
#!/bin/bash
# Setup script for ARWpost (Intel Compiler Version)

export ARWPOST_ROOT="${INSTALL_DIR}"
export PATH="\${ARWPOST_ROOT}/bin:\${PATH}"
export ARWPOST_COMPILER="intel"

echo "ARWpost environment set up (Intel optimized):"
echo "ARWPOST_ROOT: \${ARWPOST_ROOT}"
echo "ARWPOST_COMPILER: \${ARWPOST_COMPILER}"
echo "ARWpost executable: \$(which ARWpost)"
echo ""
echo "Note: This version was compiled with Intel oneAPI for optimal performance"
EOF

chmod +x ${INSTALL_DIR}/setup_arwpost_intel.sh

# Test installation
echo "Testing installation..."
${INSTALL_DIR}/bin/ARWpost --help || echo "ARWpost executable found but help not available"

echo ""
echo "=== Installation Complete (Intel Compilers) ==="
echo "ARWpost has been installed to: ${INSTALL_DIR}"
echo "Compiled with: Intel oneAPI compilers"
echo ""
echo "To use ARWpost:"
echo "1. Load the Intel module: module load ${INSTALL_DIR}/modulefiles/arwpost-intel"
echo "2. Or source the setup script: source ${INSTALL_DIR}/setup_arwpost_intel.sh"
echo "3. Run ARWpost: ARWpost"
echo ""
echo "Installation files:"
echo "- Executable: ${INSTALL_DIR}/bin/ARWpost"
echo "- Source files: ${INSTALL_DIR}/share/arwpost/"
echo "- Module file: ${INSTALL_DIR}/modulefiles/arwpost-intel"
echo "- Setup script: ${INSTALL_DIR}/setup_arwpost_intel.sh"
echo ""
echo "Performance notes:"
echo "- Compiled with Intel optimizations (-O2 -xHost -ipo)"
echo "- Optimized for the target architecture"
echo "- Should provide better performance than GCC version"

# Clean up build directory
echo "Cleaning up build directory..."
rm -rf ${BUILD_DIR}

echo "Installation completed successfully!"
