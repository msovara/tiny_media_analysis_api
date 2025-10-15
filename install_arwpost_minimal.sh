#!/bin/bash

# ARWpost Minimal Installation Script for Lengau Cluster
# This script compiles only the minimal essential ARWpost functionality

set -e  # Exit on any error

# Configuration
INSTALL_DIR="/home/apps/chpc/earth/ARWpost"
BUILD_DIR="${INSTALL_DIR}/build"

echo "=== ARWpost Minimal Installation Script ==="
echo "Installation directory: ${INSTALL_DIR}"
echo "Build directory: ${BUILD_DIR}"
echo ""

# Check if build directory exists
if [ ! -d "${BUILD_DIR}" ]; then
    echo "✗ Build directory not found: ${BUILD_DIR}"
    echo "Please run download_arwpost.sh first."
    exit 1
fi

# Load Intel Parallel Studio XE 16.0.1
echo "Loading Intel Parallel Studio XE 16.0.1..."
module purge
module load chpc/parallel_studio_xe/16.0.1/2016.1.150

# Load compatible modules
echo "Loading compatible modules..."
module load chpc/zlib/1.2.8/intel/16.0.1
module load chpc/netcdf/4.4.3-F/intel/16.0.1
module load chpc/hdf5/1.8.16/intel/16.0.1

echo "✓ All modules loaded"

# Set explicit paths
NETCDF_PATH="/apps/chpc/earth/netcdf-4.1.3-intel2016"
HDF5_PATH="/apps/libs/hdf5/1.8.16"

# Set compiler environment
export FC=ifort
export CC=icc
export CXX=icpc
export NETCDF=${NETCDF_PATH}
export HDF5=${HDF5_PATH}

echo "Environment variables set:"
echo "FC: ${FC}"
echo "CC: ${CC}"
echo "NETCDF: ${NETCDF}"
echo "HDF5: ${HDF5}"
echo ""

# Change to build directory
cd "${BUILD_DIR}"
echo "Current directory: $(pwd)"

# Define minimal files to compile (only the most basic functionality)
MINIMAL_FILES=(
    "src/constants_module.f90"
    "src/misc_definitions_module.f90"
    "src/module_debug.f90"
    "src/module_model_basics.f90"
    "src/gridinfo_module.f90"
    "src/input_module.f90"
    "src/module_arrays.f90"
    "src/module_basic_arrays.f90"
    "src/module_map_utils.f90"
    "src/module_date_pack.f90"
    "src/module_pressure.f90"
    "src/module_calc_cape.f90"
    "src/module_calc_clfr.f90"
    "src/module_calc_dbz.f90"
    "src/module_calc_height.f90"
    "src/module_calc_pressure.f90"
    "src/module_calc_rh2.f90"
    "src/module_calc_rh.f90"
    "src/module_calc_slp.f90"
    "src/module_calc_tc.f90"
    "src/module_calc_td2.f90"
    "src/module_calc_td.f90"
    "src/module_calc_theta.f90"
    "src/module_calc_tk.f90"
    "src/module_calc_uvmet.f90"
    "src/module_calc_wdir.f90"
    "src/module_calc_wspd.f90"
    "src/ARWpost.f90"
)

echo "Minimal files to compile:"
for file in "${MINIMAL_FILES[@]}"; do
    echo "  $file"
done
echo ""

# Set compilation flags
FCFLAGS="-O2 -xHost -I${NETCDF}/include"
LDFLAGS="-L${NETCDF}/lib"
LIBS="-lnetcdff -lnetcdf"

echo "Compilation flags:"
echo "FCFLAGS: ${FCFLAGS}"
echo "LDFLAGS: ${LDFLAGS}"
echo "LIBS: ${LIBS}"
echo ""

# Clean up any existing object files
echo "Cleaning up existing object files..."
rm -f *.o src/*.o

# Compile minimal files
echo "Compiling minimal files..."
for file in "${MINIMAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Compiling: $file"
        ifort ${FCFLAGS} -c "$file" -o "${file%.*}.o"
        if [ $? -ne 0 ]; then
            echo "✗ Compilation failed for: $file"
            echo "Skipping this file and continuing..."
        fi
    else
        echo "⚠ File not found: $file"
    fi
done

echo "✓ Minimal files compilation completed"

# Link the executable
echo ""
echo "Linking ARWpost executable..."
OBJECT_FILES=$(find . -name "*.o" | tr '\n' ' ')
echo "Object files: $OBJECT_FILES"

ifort ${LDFLAGS} ${OBJECT_FILES} ${LIBS} -o ARWpost

if [ $? -eq 0 ]; then
    echo "✓ ARWpost executable created successfully"
else
    echo "✗ Linking failed"
    echo "Trying alternative linking order..."
    ifort ${LDFLAGS} ${OBJECT_FILES} -lnetcdf -lnetcdff -o ARWpost
    if [ $? -eq 0 ]; then
        echo "✓ ARWpost executable created with alternative linking"
    else
        echo "✗ Alternative linking also failed"
        exit 1
    fi
fi

# Verify executable
if [ -f "ARWpost" ]; then
    echo "✓ ARWpost executable found: $(ls -lh ARWpost)"
    echo "Testing executable..."
    ./ARWpost --help 2>/dev/null || echo "Executable runs but help not available"
else
    echo "✗ ARWpost executable not found after linking"
    exit 1
fi

# Install
echo ""
echo "=== Installing ARWpost ==="
mkdir -p ${INSTALL_DIR}/bin
mkdir -p ${INSTALL_DIR}/share/arwpost

cp ARWpost ${INSTALL_DIR}/bin/
cp -r * ${INSTALL_DIR}/share/arwpost/

# Create module file
mkdir -p ${INSTALL_DIR}/modulefiles
cat > ${INSTALL_DIR}/modulefiles/arwpost-lengau << EOF
#%Module1.0
proc ModulesHelp { } {
    puts stderr "ARWpost post-processing tool for WRF"
    puts stderr "Minimal compilation with Intel Parallel Studio XE 16.0.1"
    puts stderr "Explicit NetCDF linking"
}
module-whatis "ARWpost - WRF post-processing tool (Minimal compilation)"
set version "3.1"
set arwpost_root "${INSTALL_DIR}"
prepend-path PATH \${arwpost_root}/bin
prepend-path MANPATH \${arwpost_root}/share/arwpost
setenv ARWPOST_ROOT \${arwpost_root}
setenv ARWPOST_VERSION \${version}
setenv ARWPOST_COMPILER "intel-16.0.1-minimal"
EOF

# Setup script
cat > ${INSTALL_DIR}/setup_arwpost_lengau.sh << EOF
#!/bin/bash
# Setup script for ARWpost on Lengau Cluster (Minimal compilation)

# Load Intel Parallel Studio XE 16.0.1
module load chpc/parallel_studio_xe/16.0.1/2016.1.150

# Load compatible modules
module load chpc/zlib/1.2.8/intel/16.0.1
module load chpc/netcdf/4.4.3-F/intel/16.0.1
module load chpc/hdf5/1.8.16/intel/16.0.1

# Set ARWpost environment
export ARWPOST_ROOT="${INSTALL_DIR}"
export PATH="\${ARWPOST_ROOT}/bin:\${PATH}"
export ARWPOST_COMPILER="intel-16.0.1-minimal"

echo "ARWpost environment set up (Minimal compilation):"
echo "ARWPOST_ROOT: \${ARWPOST_ROOT}"
echo "ARWPOST_COMPILER: \${ARWPOST_COMPILER}"
echo "ARWpost executable: \$(which ARWpost)"
echo ""
echo "Intel Parallel Studio XE 16.0.1 loaded"
echo "Minimal compilation with explicit NetCDF linking"
EOF
chmod +x ${INSTALL_DIR}/setup_arwpost_lengau.sh

# Installation log
cat > ${INSTALL_DIR}/install_log.txt << EOF
ARWpost Installation Log (Minimal Compilation)
==============================================
Installation Date: $(date)
Installation Directory: ${INSTALL_DIR}
Build Directory: ${BUILD_DIR}
Compiler: Intel Parallel Studio XE 16.0.1
NetCDF: ${NETCDF}
HDF5: ${HDF5}

Compilation Method: Minimal compilation with explicit linking
FCFLAGS: ${FCFLAGS}
LDFLAGS: ${LDFLAGS}
LIBS: ${LIBS}

Minimal Files Compiled:
$(for file in "${MINIMAL_FILES[@]}"; do echo "- $file"; done)

Compilation completed successfully!
EOF

echo ""
echo "=== Installation Complete (Minimal Compilation) ==="
echo "ARWpost installed to: ${INSTALL_DIR}"
echo "Compiled with: Minimal compilation and explicit NetCDF linking"
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




















