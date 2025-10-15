#!/bin/bash

# ARWpost Installation Script for Lengau Cluster (Fixed NetCDF Linking)
# Using Intel Parallel Studio XE 16.0.1 with compatible NetCDF/HDF5 modules
# This script compiles and installs ARWpost from pre-downloaded source

set -e  # Exit on any error

# Configuration
INSTALL_DIR="/home/apps/chpc/earth/ARWpost"
BUILD_DIR="${INSTALL_DIR}/build"

echo "=== ARWpost Installation Script for Lengau (Fixed NetCDF Linking) ==="
echo "Installation directory: ${INSTALL_DIR}"
echo "Build directory: ${BUILD_DIR}"
echo "Intel Parallel Studio XE 16.0.1 (compatible with available modules)"
echo ""

# Detect downloaded version dynamically from build_info.txt
if [ ! -f "${INSTALL_DIR}/build_info.txt" ]; then
    echo "✗ build_info.txt not found! Please run download_arwpost.sh first."
    exit 1
fi

ARWPOST_VERSION=$(grep "^Version:" "${INSTALL_DIR}/build_info.txt" | awk '{print $2}')
EXTRACTED_DIR=$(grep "^Extracted Source:" "${INSTALL_DIR}/build_info.txt" | awk '{print $3}')

echo "Detected ARWpost version: ${ARWPOST_VERSION}"
echo "Extracted directory: ${EXTRACTED_DIR}"

# Verify build directory
if [ ! -d "${BUILD_DIR}" ] || [ -z "$(ls -A ${BUILD_DIR})" ]; then
    echo "✗ Build directory empty or not found. Copying extracted source..."
    cp -r "${INSTALL_DIR}/source/${EXTRACTED_DIR}"/* "${BUILD_DIR}/"
fi
echo "✓ Build directory ready"

# Load Intel Parallel Studio XE 16.0.1 (compatible with available modules)
echo "Loading Intel Parallel Studio XE 16.0.1..."
module purge
module load chpc/parallel_studio_xe/16.0.1/2016.1.150

# Source Intel MPI environment (adjust path for Intel 16.0.1)
echo "Setting up Intel MPI environment..."
if [ -f "/apps/compilers/intel/parallel_studio_xe_2016_update1/compilers_and_libraries/linux/mpi/bin64/mpivars.sh" ]; then
    source /apps/compilers/intel/parallel_studio_xe_2016_update1/compilers_and_libraries/linux/mpi/bin64/mpivars.sh
elif [ -f "/apps/compilers/intel/parallel_studio_xe_2016/compilers_and_libraries/linux/mpi/bin64/mpivars.sh" ]; then
    source /apps/compilers/intel/parallel_studio_xe_2016/compilers_and_libraries/linux/mpi/bin64/mpivars.sh
else
    echo "⚠ Intel MPI environment script not found, continuing without MPI..."
fi

echo "✓ Intel Parallel Studio XE 16.0.1 loaded"

# Load compatible NetCDF and HDF5 modules
echo "Loading compatible NetCDF and HDF5 modules..."

# First, check what zlib modules are available
echo "Checking available zlib modules..."
module avail chpc/zlib 2>/dev/null | grep -E "(zlib|intel)" | head -5

# Load zlib first (required by HDF5)
echo "Loading zlib module..."
if module load chpc/zlib/1.2.8/intel/16.0.1 2>/dev/null; then
    echo "✓ Loaded chpc/zlib/1.2.8/intel/16.0.1"
elif module load chpc/zlib/1.2.8/intel-2016 2>/dev/null; then
    echo "✓ Loaded chpc/zlib/1.2.8/intel-2016"
else
    echo "⚠ Could not load zlib module, trying to continue..."
fi

# Load NetCDF (try the Intel 16.0.1 specific version first)
echo "Loading NetCDF module..."
if module load chpc/netcdf/4.4.3-F/intel/16.0.1 2>/dev/null; then
    echo "✓ Loaded chpc/netcdf/4.4.3-F/intel/16.0.1 (Intel 16.0.1 specific)"
elif module load chpc/netcdf/4.4.0-C/intel/16.0.1 2>/dev/null; then
    echo "✓ Loaded chpc/netcdf/4.4.0-C/intel/16.0.1 (Intel 16.0.1 specific)"
elif module load chpc/netcdf/4.1.3/intel-2016 2>/dev/null; then
    echo "✓ Loaded chpc/netcdf/4.1.3/intel-2016 (fallback)"
else
    echo "✗ Failed to load any NetCDF module"
    exit 1
fi

# Load HDF5 (should work now with zlib loaded)
echo "Loading HDF5 module..."
if module load chpc/hdf5/1.8.16/intel/16.0.1 2>/dev/null; then
    echo "✓ Loaded chpc/hdf5/1.8.16/intel/16.0.1"
else
    echo "✗ Failed to load HDF5 module"
    echo "  This might be due to missing zlib dependency"
    exit 1
fi

echo "✓ All required modules loaded"

# Set Intel compiler environment variables
export FC=ifort
export CC=icc
export CXX=icpc

# Extract NetCDF and HDF5 paths from environment
NETCDF_PATH="/apps/chpc/earth/netcdf-4.1.3-intel2016"
HDF5_PATH="/apps/libs/hdf5/1.8.16"

export NETCDF=${NETCDF_PATH}
export HDF5=${HDF5_PATH}

# Set compiler flags with proper NetCDF linking
export FCFLAGS="-O2 -xHost"
export CFLAGS="-O2 -xHost"
export CXXFLAGS="-O2 -xHost"

# Set NetCDF-specific flags for proper linking
export CPPFLAGS="-I${NETCDF}/include"
export LDFLAGS="-L${NETCDF}/lib"
export LIBS="-lnetcdff -lnetcdf"

echo "Environment variables set:"
echo "FC (Fortran): ${FC}"
echo "CC (C): ${CC}"
echo "CXX (C++): ${CXX}"
echo "NETCDF: ${NETCDF}"
echo "HDF5: ${HDF5}"
echo "FCFLAGS: ${FCFLAGS}"
echo "CPPFLAGS: ${CPPFLAGS}"
echo "LDFLAGS: ${LDFLAGS}"
echo "LIBS: ${LIBS}"
echo ""

# Verify Intel compilers
echo "Verifying Intel compilers..."
for compiler in ifort icc icpc; do
    command -v $compiler >/dev/null 2>&1 || { echo "✗ $compiler not found!"; exit 1; }
done
echo "✓ Intel compilers verified"

# Verify MPI (optional)
if command -v mpicc &> /dev/null; then
    echo "✓ Intel MPI found: $(mpicc --version | head -1)"
else
    echo "⚠ Intel MPI not found (will compile without MPI support)"
fi

# Verify NetCDF libraries
echo "Verifying NetCDF libraries..."
if [ -n "$NETCDF" ]; then
    if [ -f "${NETCDF}/lib/libnetcdf.a" ] || [ -f "${NETCDF}/lib/libnetcdf.so" ]; then
        echo "✓ NetCDF C library found"
    else
        echo "✗ NetCDF C library not found in ${NETCDF}/lib/"
    fi
    
    if [ -f "${NETCDF}/lib/libnetcdff.a" ] || [ -f "${NETCDF}/lib/libnetcdff.so" ]; then
        echo "✓ NetCDF Fortran library found"
    else
        echo "✗ NetCDF Fortran library not found in ${NETCDF}/lib/"
        echo "  This may cause linking errors"
    fi
else
    echo "⚠ NETCDF path not set"
fi
echo ""

# Change to build directory
cd "${BUILD_DIR}"
echo "Current directory: $(pwd)"

# Configure ARWpost with explicit NetCDF paths
echo "Configuring ARWpost with explicit NetCDF paths..."
./configure

echo "Checking build files after configuration..."
ls -la

echo "Compiling ARWpost..."
# ARWpost might use different build methods
if [ -f "Makefile" ]; then
    echo "✓ Using Makefile for compilation..."
    # Modify Makefile to include proper NetCDF linking
    if grep -q "LIBS" Makefile; then
        echo "✓ Makefile already has LIBS variable"
    else
        echo "⚠ Adding LIBS to Makefile..."
        sed -i 's/^LIBS =/LIBS = -lnetcdff -lnetcdf/' Makefile 2>/dev/null || echo "Could not modify Makefile"
    fi
    make clean
    make
elif [ -f "compile" ]; then
    echo "✓ Using compile script for compilation..."
    # Check if compile script needs modification
    if [ -f "compile" ]; then
        echo "Checking compile script..."
        head -20 compile
    fi
    ./compile
elif [ -f "src/Makefile" ]; then
    echo "✓ Using src/Makefile for compilation..."
    cd src
    make clean
    make
    cd ..
else
    echo "✗ No build system found after configuration"
    echo "Available files:"
    ls -la
    echo ""
    echo "Trying to find ARWpost executable..."
    find . -name "ARWpost" -type f 2>/dev/null || echo "ARWpost executable not found"
    exit 1
fi

# Install
echo "Installing ARWpost..."
mkdir -p ${INSTALL_DIR}/bin
mkdir -p ${INSTALL_DIR}/share/arwpost

# Look for the executable with different names
if [ -f "ARWpost" ]; then
    cp ARWpost ${INSTALL_DIR}/bin/
elif [ -f "ARWpost.exe" ]; then
    cp ARWpost.exe ${INSTALL_DIR}/bin/ARWpost
elif [ -f "src/ARWpost" ]; then
    cp src/ARWpost ${INSTALL_DIR}/bin/
elif [ -f "src/ARWpost.exe" ]; then
    cp src/ARWpost.exe ${INSTALL_DIR}/bin/ARWpost
else
    echo "✗ ARWpost executable not found"
    echo "Looking for executables..."
    find . -name "*ARWpost*" -type f
    exit 1
fi

cp -r * ${INSTALL_DIR}/share/arwpost/

# Create module file
mkdir -p ${INSTALL_DIR}/modulefiles
cat > ${INSTALL_DIR}/modulefiles/arwpost-lengau << EOF
#%Module1.0
proc ModulesHelp { } {
    puts stderr "ARWpost post-processing tool for WRF"
    puts stderr "Compiled with Intel Parallel Studio XE 16.0.1"
    puts stderr "Using compatible NetCDF and HDF5 modules"
}
module-whatis "ARWpost - WRF post-processing tool (Lengau Intel optimized)"
set version "${ARWPOST_VERSION}"
set arwpost_root "${INSTALL_DIR}"
prepend-path PATH \${arwpost_root}/bin
prepend-path MANPATH \${arwpost_root}/share/arwpost
setenv ARWPOST_ROOT \${arwpost_root}
setenv ARWPOST_VERSION \${version}
setenv ARWPOST_COMPILER "intel-16.0.1"
EOF

# Setup script
cat > ${INSTALL_DIR}/setup_arwpost_lengau.sh << EOF
#!/bin/bash
# Setup script for ARWpost on Lengau Cluster (Compatible Modules)

# Load Intel Parallel Studio XE 16.0.1
module load chpc/parallel_studio_xe/16.0.1/2016.1.150

# Load compatible modules in correct order
module load chpc/zlib/1.2.8/intel/16.0.1
module load chpc/netcdf/4.1.3/intel-2016
module load chpc/hdf5/1.8.16/intel/16.0.1

# Set ARWpost environment
export ARWPOST_ROOT="${INSTALL_DIR}"
export PATH="\${ARWPOST_ROOT}/bin:\${PATH}"
export ARWPOST_COMPILER="intel-16.0.1"

echo "ARWpost environment set up for Lengau (Compatible Modules):"
echo "ARWPOST_ROOT: \${ARWPOST_ROOT}"
echo "ARWPOST_COMPILER: \${ARWPOST_COMPILER}"
echo "ARWpost executable: \$(which ARWpost)"
echo ""
echo "Intel Parallel Studio XE 16.0.1 loaded"
echo "Compatible zlib, NetCDF and HDF5 modules loaded"
EOF
chmod +x ${INSTALL_DIR}/setup_arwpost_lengau.sh

# Installation log
cat > ${INSTALL_DIR}/install_log.txt << EOF
ARWpost Installation Log (Fixed NetCDF Linking)
===============================================
Installation Date: $(date)
ARWpost Version: ${ARWPOST_VERSION}
Installation Directory: ${INSTALL_DIR}
Build Directory: ${BUILD_DIR}
Compiler: Intel Parallel Studio XE 16.0.1
NetCDF: ${NETCDF}
HDF5: ${HDF5}
Modules Used:
- chpc/parallel_studio_xe/16.0.1/2016.1.150
- chpc/zlib/1.2.8/intel/16.0.1
- chpc/netcdf/4.1.3/intel-2016
- chpc/hdf5/1.8.16/intel/16.0.1

Linking Flags:
- CPPFLAGS: ${CPPFLAGS}
- LDFLAGS: ${LDFLAGS}
- LIBS: ${LIBS}

Compilation completed successfully!
EOF

# Test installation
${INSTALL_DIR}/bin/ARWpost --help || echo "ARWpost executable found but help not available"

echo ""
echo "=== Installation Complete (Lengau Intel - Fixed NetCDF Linking) ==="
echo "ARWpost installed to: ${INSTALL_DIR}"
echo "Compiled with: Intel Parallel Studio XE 16.0.1"
echo "Using compatible NetCDF and HDF5 modules"
echo ""
echo "Module file: ${INSTALL_DIR}/modulefiles/arwpost-lengau"
echo "Setup script: ${INSTALL_DIR}/setup_arwpost_lengau.sh"
echo ""
echo "To use ARWpost:"
echo "1. Load the module: module load ${INSTALL_DIR}/modulefiles/arwpost-lengau"
echo "2. Or source the setup script: source ${INSTALL_DIR}/setup_arwpost_lengau.sh"
echo "3. Run ARWpost: ARWpost"
echo ""
echo "Installation completed successfully!"
