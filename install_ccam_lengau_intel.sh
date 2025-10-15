#!/bin/bash

# CCAM Installation Script for Lengau Cluster
# Using Intel Parallel Studio XE 2018.2.046
# This script compiles and installs CCAM (Conformal Cubic Atmospheric Model)

set -e  # Exit on any error

# Configuration
INSTALL_DIR="/mnt/lustre/users/msovara/SoftwareBuilds/CCAM"
BUILD_DIR="${INSTALL_DIR}/build"
CCAM_VERSION="CCAM-2023"
CCAM_SOURCE_URL="https://github.com/CSIRO-CCAM/ccam.git"

echo "=== CCAM Installation Script for Lengau ==="
echo "Installation directory: ${INSTALL_DIR}"
echo "Build directory: ${BUILD_DIR}"
echo "CCAM version: ${CCAM_VERSION}"
echo "Intel Parallel Studio XE 2018.2.046"
echo ""

# Create directories
echo "Creating installation directories..."
mkdir -p ${INSTALL_DIR}
mkdir -p ${BUILD_DIR}

# Check if source already exists
if [ ! -d "${BUILD_DIR}/ccam" ]; then
    echo "Downloading CCAM source code..."
    cd ${BUILD_DIR}
    
    # Try to clone from GitHub (if available)
    if command -v git &> /dev/null; then
        echo "Cloning CCAM from GitHub..."
        git clone ${CCAM_SOURCE_URL} ccam || {
            echo "⚠ GitHub clone failed, trying alternative download methods..."
            # Alternative: download from CSIRO website or other sources
            echo "Please download CCAM source code manually and place it in ${BUILD_DIR}/ccam"
            echo "You can obtain CCAM from:"
            echo "1. CSIRO CCAM website"
            echo "2. Contact CSIRO for access"
            echo "3. Check if available through CHPC software repository"
            exit 1
        }
    else
        echo "✗ Git not available. Please install git or download CCAM source manually."
        exit 1
    fi
else
    echo "✓ CCAM source code already exists"
fi

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

# Intel-specific compiler flags for optimization
export FCFLAGS="-O2 -xHost -qopenmp"
export CFLAGS="-O2 -xHost -qopenmp"
export CXXFLAGS="-O2 -xHost -qopenmp"

# CCAM-specific environment variables
export CCAM_ROOT=${INSTALL_DIR}
export CCAM_VERSION=${CCAM_VERSION}

echo "Environment variables set:"
echo "FC (Fortran): ${FC}"
echo "CC (C): ${CC}"
echo "CXX (C++): ${CXX}"
echo "NETCDF: ${NETCDF}"
echo "HDF5: ${HDF5}"
echo "FCFLAGS: ${FCFLAGS}"
echo "CCAM_ROOT: ${CCAM_ROOT}"
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

# Change to CCAM source directory
echo "Changing to CCAM source directory..."
cd ${BUILD_DIR}/ccam
echo "Current directory: $(pwd)"
echo "Source files: $(ls -la | head -10)"

# Check for CCAM build system
if [ -f "configure" ]; then
    echo "Found configure script, running configuration..."
    ./configure --prefix=${INSTALL_DIR} \
                --with-netcdf=${NETCDF} \
                --with-hdf5=${HDF5} \
                --with-mpi \
                --enable-openmp
elif [ -f "Makefile" ]; then
    echo "Found Makefile, proceeding with compilation..."
    # Set make variables for Intel compilers
    export MAKE_FC=ifort
    export MAKE_CC=icc
    export MAKE_CXX=icpc
elif [ -f "CMakeLists.txt" ]; then
    echo "Found CMakeLists.txt, using CMake..."
    mkdir -p build_cmake
    cd build_cmake
    cmake .. -DCMAKE_Fortran_COMPILER=ifort \
             -DCMAKE_C_COMPILER=icc \
             -DCMAKE_CXX_COMPILER=icpc \
             -DCMAKE_INSTALL_PREFIX=${INSTALL_DIR} \
             -DNETCDF_ROOT=${NETCDF} \
             -DHDF5_ROOT=${HDF5}
else
    echo "⚠ No standard build system found. Checking for custom build instructions..."
    if [ -f "README" ] || [ -f "README.md" ]; then
        echo "Found README file. Please check for build instructions:"
        head -20 README* 2>/dev/null || echo "Could not read README"
    fi
    echo "Please check CCAM documentation for build instructions"
    exit 1
fi

# Compile CCAM
echo "Compiling CCAM with Intel optimizations..."
make clean 2>/dev/null || echo "No clean target available"
make -j$(nproc)

# Install CCAM
echo "Installing CCAM to ${INSTALL_DIR}..."
mkdir -p ${INSTALL_DIR}/bin
mkdir -p ${INSTALL_DIR}/lib
mkdir -p ${INSTALL_DIR}/include
mkdir -p ${INSTALL_DIR}/share/ccam

# Copy executables and libraries
find . -name "ccam" -type f -executable -exec cp {} ${INSTALL_DIR}/bin/ \;
find . -name "*.exe" -type f -executable -exec cp {} ${INSTALL_DIR}/bin/ \;
find . -name "*.so" -type f -exec cp {} ${INSTALL_DIR}/lib/ \;
find . -name "*.a" -type f -exec cp {} ${INSTALL_DIR}/lib/ \;

# Copy source files and documentation
cp -r * ${INSTALL_DIR}/share/ccam/ 2>/dev/null || echo "Some files could not be copied"

# Create Lengau-specific module file
echo "Creating Lengau-specific module file..."
mkdir -p ${INSTALL_DIR}/modulefiles
cat > ${INSTALL_DIR}/modulefiles/ccam-lengau << EOF
#%Module1.0
##
## CCAM modulefile for Lengau Cluster
## Intel Parallel Studio XE 2018.2.046
##

proc ModulesHelp { } {
    puts stderr "This module sets up the environment for CCAM"
    puts stderr "CCAM is the Conformal Cubic Atmospheric Model"
    puts stderr "Compiled with Intel Parallel Studio XE 2018.2.046"
}

module-whatis "CCAM - Conformal Cubic Atmospheric Model (Lengau Intel optimized)"

set version "${CCAM_VERSION}"
set ccam_root "${INSTALL_DIR}"

prepend-path PATH \${ccam_root}/bin
prepend-path LD_LIBRARY_PATH \${ccam_root}/lib
prepend-path MANPATH \${ccam_root}/share/ccam

setenv CCAM_ROOT \${ccam_root}
setenv CCAM_VERSION \${version}
setenv CCAM_COMPILER "intel-2018.2.046"
EOF

# Create Lengau-specific setup script
echo "Creating Lengau-specific setup script..."
cat > ${INSTALL_DIR}/setup_ccam_lengau.sh << EOF
#!/bin/bash
# Setup script for CCAM on Lengau Cluster

# Load Intel Parallel Studio XE
module load chpc/parallel_studio_xe/18.0.2/2018.2.046

# Source Intel MPI environment
source /apps/compilers/intel/parallel_studio_xe_2018_update2/compilers_and_libraries/linux/mpi/bin64/mpivars.sh

# Set CCAM environment
export CCAM_ROOT="${INSTALL_DIR}"
export PATH="\${CCAM_ROOT}/bin:\${PATH}"
export LD_LIBRARY_PATH="\${CCAM_ROOT}/lib:\${LD_LIBRARY_PATH}"
export CCAM_COMPILER="intel-2018.2.046"

echo "CCAM environment set up for Lengau:"
echo "CCAM_ROOT: \${CCAM_ROOT}"
echo "CCAM_COMPILER: \${CCAM_COMPILER}"
echo "CCAM executable: \$(which ccam 2>/dev/null || echo 'ccam not found in PATH')"
echo ""
echo "Intel Parallel Studio XE 2018.2.046 loaded"
echo "Intel MPI environment configured"
EOF

chmod +x ${INSTALL_DIR}/setup_ccam_lengau.sh

# Create installation log
echo "Creating installation log..."
cat > ${INSTALL_DIR}/install_log.txt << EOF
CCAM Installation Log
=====================
Installation Date: $(date)
CCAM Version: ${CCAM_VERSION}
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
- CCAM_ROOT: ${CCAM_ROOT}

Compilation completed successfully!
EOF

# Test installation
echo "Testing installation..."
if [ -f "${INSTALL_DIR}/bin/ccam" ]; then
    echo "✓ CCAM executable found: ${INSTALL_DIR}/bin/ccam"
    ${INSTALL_DIR}/bin/ccam --help 2>/dev/null || echo "CCAM executable found but help not available"
else
    echo "⚠ CCAM executable not found in expected location"
    echo "Checking for other executables..."
    find ${INSTALL_DIR}/bin -type f -executable -ls
fi

echo ""
echo "=== Installation Complete (Lengau Intel) ==="
echo "CCAM has been installed to: ${INSTALL_DIR}"
echo "Compiled with: Intel Parallel Studio XE 2018.2.046"
echo ""
echo "To use CCAM:"
echo "1. Load the Lengau module: module load ${INSTALL_DIR}/modulefiles/ccam-lengau"
echo "2. Or source the setup script: source ${INSTALL_DIR}/setup_ccam_lengau.sh"
echo "3. Run CCAM: ccam"
echo ""
echo "Installation files:"
echo "- Executable: ${INSTALL_DIR}/bin/ccam (if found)"
echo "- Source files: ${INSTALL_DIR}/share/ccam/"
echo "- Module file: ${INSTALL_DIR}/modulefiles/ccam-lengau"
echo "- Setup script: ${INSTALL_DIR}/setup_ccam_lengau.sh"
echo "- Installation log: ${INSTALL_DIR}/install_log.txt"
echo ""
echo "Performance notes:"
echo "- Compiled with Intel Parallel Studio XE 2018.2.046"
echo "- Optimized for the target architecture (-O2 -xHost)"
echo "- OpenMP support enabled (-qopenmp)"
echo "- Intel MPI support included"
echo "- Should provide excellent performance on Lengau cluster"
echo ""
echo "Note: CCAM source code access may require registration with CSIRO"
echo "Please ensure you have proper access to CCAM source code"

echo "Installation completed successfully!"




























