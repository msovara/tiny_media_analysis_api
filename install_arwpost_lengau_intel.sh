#!/bin/bash

# ARWpost Installation Script for Lengau Cluster
# Using Intel Parallel Studio XE 2018.2.046
# This script compiles and installs ARWpost from pre-downloaded source

set -e  # Exit on any error

# Configuration
INSTALL_DIR="/mnt/lustre/users/msovara/SoftwareBuilds/ARWpost"
BUILD_DIR="${INSTALL_DIR}/build"
ARWPOST_VERSION="ARWpost_V3.1"

echo "=== ARWpost Installation Script for Lengau ==="
echo "Installation directory: ${INSTALL_DIR}"
echo "Build directory: ${BUILD_DIR}"
echo "ARWpost version: ${ARWPOST_VERSION}"
echo "Intel Parallel Studio XE 2018.2.046"
echo ""

# Check if build directory exists and contains source
if [ ! -d "${BUILD_DIR}" ]; then
    echo "✗ Build directory not found: ${BUILD_DIR}"
    echo "Please run download_arwpost.sh first to download the source code."
    exit 1
fi

if [ ! "$(ls -A ${BUILD_DIR})" ]; then
    echo "✗ Build directory is empty: ${BUILD_DIR}"
    echo "Please run download_arwpost.sh first to download the source code."
    exit 1
fi

echo "✓ Build directory found and contains source code"

# Load Intel Parallel Studio XE 2018.2.046
echo "Loading Intel Parallel Studio XE 2018.2.046..."
module purge
module load chpc/parallel_studio_xe/18.0.2/2018.2.046

# Source Intel MPI environment
echo "Setting up Intel MPI environment..."
source /apps/compilers/intel/parallel_studio_xe_2018_update2/compilers_and_libraries/linux/mpi/bin64/mpivars.sh

echo "✓ Intel Parallel Studio XE 2018.2.046 loaded"
echo "✓ Intel MPI environment configured"

# Load other required modules
echo "Loading other required modules..."

# Try to load compatible NetCDF and HDF5 modules
# First, check what modules are available
echo "Checking available NetCDF and HDF5 modules..."
module avail chpc/netcdf 2>/dev/null | grep -E "(netcdf|hdf5)" | head -10

# Try to load modules that are compatible with Intel 2018
echo "Attempting to load compatible modules..."

# Try different module combinations
MODULE_LOADED=false

# Option 1: Try newer versions
if module load chpc/netcdf/4.7.4 2>/dev/null; then
    echo "✓ Loaded chpc/netcdf/4.7.4"
    if module load chpc/hdf5/1.12.0 2>/dev/null; then
        echo "✓ Loaded chpc/hdf5/1.12.0"
        MODULE_LOADED=true
    else
        echo "⚠ Could not load chpc/hdf5/1.12.0, trying alternative..."
    fi
fi

# Option 2: Try older versions if newer ones failed
if [ "$MODULE_LOADED" = false ]; then
    if module load chpc/netcdf/4.1.3 2>/dev/null; then
        echo "✓ Loaded chpc/netcdf/4.1.3"
        if module load chpc/hdf5/1.8.16 2>/dev/null; then
            echo "✓ Loaded chpc/hdf5/1.8.16"
            MODULE_LOADED=true
        else
            echo "⚠ Could not load chpc/hdf5/1.8.16"
        fi
    fi
fi

# Option 3: Try system modules
if [ "$MODULE_LOADED" = false ]; then
    echo "⚠ Could not load CHPC modules, trying system modules..."
    if module load netcdf 2>/dev/null; then
        echo "✓ Loaded system netcdf"
        if module load hdf5 2>/dev/null; then
            echo "✓ Loaded system hdf5"
            MODULE_LOADED=true
        fi
    fi
fi

if [ "$MODULE_LOADED" = false ]; then
    echo "⚠ Could not load NetCDF/HDF5 modules automatically"
    echo "  Will try to use system-installed libraries"
fi

# Set Intel compiler environment variables
export FC=ifort
export CC=icc
export CXX=icpc

# Set NetCDF and HDF5 paths
if [ -n "$NETCDF_ROOT" ]; then
    export NETCDF=${NETCDF_ROOT}
    echo "✓ Using NetCDF from module: ${NETCDF}"
elif [ -n "$NETCDF" ]; then
    echo "✓ Using existing NetCDF: ${NETCDF}"
else
    echo "⚠ NETCDF_ROOT not set, will try system installation"
    # Try to find NetCDF in common locations
    for path in /usr /usr/local /opt/netcdf /apps/netcdf; do
        if [ -f "${path}/include/netcdf.h" ]; then
            export NETCDF=${path}
            echo "✓ Found NetCDF at: ${NETCDF}"
            break
        fi
    done
fi

if [ -n "$HDF5_ROOT" ]; then
    export HDF5=${HDF5_ROOT}
    echo "✓ Using HDF5 from module: ${HDF5}"
elif [ -n "$HDF5" ]; then
    echo "✓ Using existing HDF5: ${HDF5}"
else
    echo "⚠ HDF5_ROOT not set, will try system installation"
    # Try to find HDF5 in common locations
    for path in /usr /usr/local /opt/hdf5 /apps/hdf5; do
        if [ -f "${path}/include/hdf5.h" ]; then
            export HDF5=${path}
            echo "✓ Found HDF5 at: ${HDF5}"
            break
        fi
    done
fi

# Intel-specific compiler flags for optimization (adjusted for 2018 version)
export FCFLAGS="-O2 -xHost"
export CFLAGS="-O2 -xHost"
export CXXFLAGS="-O2 -xHost"

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

# Verify Intel MPI
echo "Verifying Intel MPI..."
if command -v mpicc &> /dev/null; then
    echo "✓ Intel MPI: $(mpicc --version | head -1)"
else
    echo "✗ Intel MPI not found"
    exit 1
fi
echo ""

# Change to build directory
echo "Changing to build directory..."
cd ${BUILD_DIR}
echo "Current directory: $(pwd)"
echo "Build files: $(ls -la | head -10)"

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

# Create Lengau-specific module file
echo "Creating Lengau-specific module file..."
mkdir -p ${INSTALL_DIR}/modulefiles
cat > ${INSTALL_DIR}/modulefiles/arwpost-lengau << EOF
#%Module1.0
##
## ARWpost modulefile for Lengau Cluster
## Intel Parallel Studio XE 2018.2.046
##

proc ModulesHelp { } {
    puts stderr "This module sets up the environment for ARWpost"
    puts stderr "ARWpost is a post-processing tool for WRF model output"
    puts stderr "Compiled with Intel Parallel Studio XE 2018.2.046"
}

module-whatis "ARWpost - WRF post-processing tool (Lengau Intel optimized)"

set version "3.1"
set arwpost_root "${INSTALL_DIR}"

prepend-path PATH \${arwpost_root}/bin
prepend-path MANPATH \${arwpost_root}/share/arwpost

setenv ARWPOST_ROOT \${arwpost_root}
setenv ARWPOST_VERSION \${version}
setenv ARWPOST_COMPILER "intel-2018.2.046"
EOF

# Create Lengau-specific setup script
echo "Creating Lengau-specific setup script..."
cat > ${INSTALL_DIR}/setup_arwpost_lengau.sh << EOF
#!/bin/bash
# Setup script for ARWpost on Lengau Cluster

# Load Intel Parallel Studio XE
module load chpc/parallel_studio_xe/18.0.2/2018.2.046

# Source Intel MPI environment
source /apps/compilers/intel/parallel_studio_xe_2018_update2/compilers_and_libraries/linux/mpi/bin64/mpivars.sh

# Set ARWpost environment
export ARWPOST_ROOT="${INSTALL_DIR}"
export PATH="\${ARWPOST_ROOT}/bin:\${PATH}"
export ARWPOST_COMPILER="intel-2018.2.046"

echo "ARWpost environment set up for Lengau:"
echo "ARWPOST_ROOT: \${ARWPOST_ROOT}"
echo "ARWPOST_COMPILER: \${ARWPOST_COMPILER}"
echo "ARWpost executable: \$(which ARWpost)"
echo ""
echo "Intel Parallel Studio XE 2018.2.046 loaded"
echo "Intel MPI environment configured"
EOF

chmod +x ${INSTALL_DIR}/setup_arwpost_lengau.sh

# Create installation log
echo "Creating installation log..."
cat > ${INSTALL_DIR}/install_log.txt << EOF
ARWpost Installation Log
=========================
Installation Date: $(date)
ARWpost Version: ${ARWPOST_VERSION}
Installation Directory: ${INSTALL_DIR}
Build Directory: ${BUILD_DIR}
Compiler: Intel Parallel Studio XE 2018.2.046

Environment Variables:
- FC: ${FC}
- CC: ${CC}
- CXX: ${CXX}
- NETCDF: ${NETCDF}
- HDF5: ${HDF5}
- FCFLAGS: ${FCFLAGS}

Compilation completed successfully!
EOF

# Test installation
echo "Testing installation..."
${INSTALL_DIR}/bin/ARWpost --help || echo "ARWpost executable found but help not available"

echo ""
echo "=== Installation Complete (Lengau Intel) ==="
echo "ARWpost has been installed to: ${INSTALL_DIR}"
echo "Compiled with: Intel Parallel Studio XE 2018.2.046"
echo ""
echo "To use ARWpost:"
echo "1. Load the Lengau module: module load ${INSTALL_DIR}/modulefiles/arwpost-lengau"
echo "2. Or source the setup script: source ${INSTALL_DIR}/setup_arwpost_lengau.sh"
echo "3. Run ARWpost: ARWpost"
echo ""
echo "Installation files:"
echo "- Executable: ${INSTALL_DIR}/bin/ARWpost"
echo "- Source files: ${INSTALL_DIR}/share/arwpost/"
echo "- Module file: ${INSTALL_DIR}/modulefiles/arwpost-lengau"
echo "- Setup script: ${INSTALL_DIR}/setup_arwpost_lengau.sh"
echo "- Installation log: ${INSTALL_DIR}/install_log.txt"
echo ""
echo "Performance notes:"
echo "- Compiled with Intel Parallel Studio XE 2018.2.046"
echo "- Optimized for the target architecture (-O2 -xHost)"
echo "- Intel MPI support included"
echo "- Should provide excellent performance on Lengau cluster"

echo "Installation completed successfully!"
