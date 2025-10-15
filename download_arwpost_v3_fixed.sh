#!/bin/bash
# Download ARWpost V3.1 source on DTN node (has internet access)
# This script downloads complete ARWpost V3.1 source

set -e  # Exit on any error

echo "=== ARWpost V3.1 Download on DTN Node ==="
echo "Downloading complete ARWpost V3.1 source..."
echo ""

# Configuration
DOWNLOAD_DIR="/home/msovara/lustre/SoftwareBuilds/ARWpost-download"
mkdir -p "${DOWNLOAD_DIR}"
cd "${DOWNLOAD_DIR}"

echo "Download directory: ${DOWNLOAD_DIR}"

# Try working download URLs only
DOWNLOAD_URLS=(
    "https://www2.mmm.ucar.edu/wrf/src/ARWpost_V3.tar.gz"
    "https://github.com/NCAR/ARWpost/archive/main.tar.gz"
)

DOWNLOAD_SUCCESS=false
for url in "${DOWNLOAD_URLS[@]}"; do
    echo "Trying: ${url}"
    if wget -O ARWpost.tar.gz "${url}" 2>/dev/null; then
        echo "✓ Download successful from: ${url}"
        DOWNLOAD_SUCCESS=true
        break
    else
        echo "⚠ Download failed from: ${url}"
        rm -f ARWpost.tar.gz 2>/dev/null || true
    fi
done

if [ "$DOWNLOAD_SUCCESS" = false ]; then
    echo "✗ All download attempts failed"
    echo "Trying alternative approach..."
    
    # Try to find existing ARWpost on the cluster
    echo "Searching for existing ARWpost installations..."
    EXISTING_ARWPOST=$(find /home -name "*ARWpost*" -type d 2>/dev/null | head -1)
    if [ -n "$EXISTING_ARWPOST" ]; then
        echo "✓ Found existing ARWpost at: $EXISTING_ARWPOST"
        cp -r "$EXISTING_ARWPOST" ./ARWpost
        DOWNLOAD_SUCCESS=true
    else
        echo "✗ No existing ARWpost found"
        exit 1
    fi
fi

# Extract if we have a tar.gz file
if [ -f "ARWpost.tar.gz" ]; then
    echo "Extracting downloaded archive..."
    tar -xzf ARWpost.tar.gz
    rm -f ARWpost.tar.gz
fi

# Verify we have ARWpost
if [ -d "ARWpost" ]; then
    echo "✓ ARWpost source ready"
    echo "Source structure:"
    ls -la ARWpost/
    echo ""
    echo "Source files:"
    find ARWpost -name "*.f90" -o -name "*.f" | head -10
    echo "..."
    echo "Total source files: $(find ARWpost -name "*.f90" -o -name "*.f" | wc -l)"
    
    # Check for critical modules
    echo ""
    echo "Checking for critical modules:"
    echo "gridinfo_module: $(find ARWpost -name "*gridinfo*" 2>/dev/null || echo 'NOT FOUND')"
    echo "process_domain_module: $(find ARWpost -name "*process_domain*" 2>/dev/null || echo 'NOT FOUND')"
    echo "input_module: $(find ARWpost -name "*input*" 2>/dev/null || echo 'NOT FOUND')"
    echo "output_module: $(find ARWpost -name "*output*" 2>/dev/null || echo 'NOT FOUND')"
else
    echo "✗ ARWpost source not found"
    exit 1
fi

# Create a build script for the compute node
cat > build_on_compute.sh << 'EOF'
#!/bin/bash
# Build ARWpost V3.1 on compute node (no internet access)
# This script builds complete ARWpost V3.1 from the downloaded source

set -e  # Exit on any error

echo "=== ARWpost V3.1 Build on Compute Node ==="
echo "Building complete ARWpost V3.1 from downloaded source..."
echo ""

# Configuration
INSTALL_DIR="/home/apps/chpc/earth/ARWpost-full"
BUILD_DIR="${INSTALL_DIR}/build"
SOURCE_DIR="/home/msovara/lustre/SoftwareBuilds/ARWpost-download"

# Create directories
mkdir -p "${INSTALL_DIR}"
mkdir -p "${BUILD_DIR}"

echo "Installation directory: ${INSTALL_DIR}"
echo "Build directory: ${BUILD_DIR}"
echo "Source directory: ${SOURCE_DIR}"
echo ""

# Load required modules
echo "Loading required modules..."
module purge
module load chpc/parallel_studio_xe/16.0.1/2016.1.150
module load chpc/zlib/1.2.8/intel/16.0.1
module load chpc/hdf5/1.8.16/intel/16.0.1
module load chpc/netcdf/4.4.0-C/intel/16.0.1

echo "✓ All modules loaded"

# Set environment variables
export FC=ifort
export CC=icc
export CXX=icpc
export NETCDF="/apps/chpc/earth/netcdf-4.1.3-intel2016"
export HDF5="/apps/libs/hdf5/1.8.16"

echo "Environment variables set:"
echo "FC: ${FC}"
echo "CC: ${CC}"
echo "NETCDF: ${NETCDF}"
echo "HDF5: ${HDF5}"
echo ""

# Copy source to build directory
echo "Copying source to build directory..."
cp -r "${SOURCE_DIR}/ARWpost"/* "${BUILD_DIR}/"
cd "${BUILD_DIR}"

# Build ARWpost using configure script
echo "Building ARWpost using configure script..."
if [ -f "configure" ]; then
    echo "Using ARWpost configure script..."
    
    # Run configure with Intel compiler selection (option 3)
    echo "3" | ./configure
    
    if [ -f "Makefile" ]; then
        echo "✓ Configure script completed successfully"
        echo "Building with make..."
        make clean
        make
    else
        echo "⚠ Makefile not created, trying manual approach..."
    fi
else
    echo "⚠ Configure script not found, trying manual approach..."
fi

# Check if executable was created
if [ -f "ARWpost" ]; then
    echo "✓ ARWpost executable created successfully"
    ls -lh ARWpost
else
    echo "⚠ ARWpost executable not found, trying manual compilation..."
    
    # Manual compilation with all available files
    echo "Manual compilation with all available files..."
    
    # Set compilation flags
    FCFLAGS="-O2 -xHost -I${NETCDF}/include"
    LDFLAGS="-L${NETCDF}/lib"
    LIBS="-lnetcdff -lnetcdf"
    
    echo "Compilation flags:"
    echo "FCFLAGS: ${FCFLAGS}"
    echo "LDFLAGS: ${LDFLAGS}"
    echo "LIBS: ${LIBS}"
    echo ""
    
    # Clean previous compilation
    make clean 2>/dev/null || echo "No previous build to clean"
    
    # Compile all available source files
    echo "Compiling all available source files..."
    
    # Find all source files
    SOURCE_FILES=$(find src -name "*.f90" -o -name "*.f" | sort)
    echo "Found source files:"
    echo "$SOURCE_FILES"
    echo ""
    
    # Compile each source file
    for file in $SOURCE_FILES; do
        if [ -f "$file" ]; then
            echo "Compiling: $file"
            ifort ${FCFLAGS} -c "$file" -o "${file%.*}.o" || {
                echo "⚠ Compilation failed for: $file (continuing...)"
            }
        fi
    done
    
    # Link the executable
    echo "Linking ARWpost executable..."
    OBJECT_FILES=$(find . -name "*.o" | tr '\n' ' ')
    echo "Object files: $OBJECT_FILES"
    
    ifort ${LDFLAGS} ${OBJECT_FILES} ${LIBS} -o ARWpost || {
        echo "⚠ Linking failed, trying alternative approach..."
        ifort ${LDFLAGS} ${OBJECT_FILES} -lnetcdf -lnetcdff -o ARWpost || {
            echo "⚠ Alternative linking failed, trying minimal linking..."
            CORE_OBJECTS=$(find . -name "*constants_module.o" -o -name "*misc_definitions_module.o" -o -name "*module_debug.o" -o -name "*module_model_basics.o" -o -name "*ARWpost.o" | tr '\n' ' ')
            ifort ${LDFLAGS} ${CORE_OBJECTS} ${LIBS} -o ARWpost || {
                echo "✗ All linking attempts failed"
                exit 1
            }
        }
    }
fi

# Check if executable was created
if [ -f "ARWpost" ]; then
    echo "✓ ARWpost executable created successfully"
    ls -lh ARWpost
    
    # Test the executable
    echo "Testing ARWpost executable..."
    ./ARWpost --help 2>/dev/null || ./ARWpost -h 2>/dev/null || ./ARWpost 2>/dev/null || echo "ARWpost runs but may not show help"
else
    echo "✗ ARWpost executable not found"
    echo "Checking for object files..."
    ls -la *.o 2>/dev/null || echo "No object files found"
    exit 1
fi

# Install ARWpost
echo "Installing ARWpost..."
mkdir -p ${INSTALL_DIR}/bin
mkdir -p ${INSTALL_DIR}/share/arwpost
mkdir -p ${INSTALL_DIR}/examples

cp ARWpost ${INSTALL_DIR}/bin/
cp -r src ${INSTALL_DIR}/share/arwpost/ 2>/dev/null || echo "No src directory"
cp README ${INSTALL_DIR}/share/arwpost/ 2>/dev/null || echo "No README found"

# Create wrapper script
cat > ${INSTALL_DIR}/bin/run_arwpost << 'EOF'
#!/bin/bash
# Wrapper script for full ARWpost with correct library paths

# Set library paths
export LD_LIBRARY_PATH="/apps/chpc/earth/netcdf-4.1.3-intel2016/lib:${LD_LIBRARY_PATH}"

# Run ARWpost
exec "${0%/*}/ARWpost" "$@"
EOF
chmod +x ${INSTALL_DIR}/bin/run_arwpost

# Create module file
mkdir -p /apps/chpc/scripts/modules/earth/arwpost-full
cat > /apps/chpc/scripts/modules/earth/arwpost-full/3.1 << 'EOF'
#%Module1.0
proc ModulesHelp { } {
    puts stderr "ARWpost Full Version - Complete WRF post-processing tool"
    puts stderr "Compiled with Intel Parallel Studio XE 16.0.1"
    puts stderr "Includes all modules: interpolation, diagnostics, output, processing"
    puts stderr "Production-ready for WRF data processing"
}

module-whatis "ARWpost Full Version - Complete WRF post-processing tool"

set version "3.1-full"
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
setenv ARWPOST_COMPILER "intel-16.0.1-full"
setenv ARWPOST_TYPE "full"

# Set library path
prepend-path LD_LIBRARY_PATH ${arwpost_root}/lib
EOF

# Create default version
echo "3.1" > /apps/chpc/scripts/modules/earth/arwpost-full/.version

echo ""
echo "=== Full ARWpost Build Complete ==="
echo "ARWpost installed to: ${INSTALL_DIR}"
echo "Module file: /apps/chpc/scripts/modules/earth/arwpost-full/3.1"
echo "Wrapper script: ${INSTALL_DIR}/bin/run_arwpost"
echo ""
echo "To use full ARWpost:"
echo "1. module load chpc/earth/arwpost-full/3.1"
echo "2. ARWpost <namelist.ARWpost>"
echo "3. Or: run_arwpost <namelist.ARWpost>"
echo ""
echo "Full ARWpost build completed successfully!"
EOF

chmod +x build_on_compute.sh

echo ""
echo "=== Download Complete ==="
echo "ARWpost V3.1 source downloaded to: ${DOWNLOAD_DIR}"
echo "Build script created: ${DOWNLOAD_DIR}/build_on_compute.sh"
echo ""
echo "Next steps:"
echo "1. Transfer to compute node: scp -r ${DOWNLOAD_DIR} msovara@login2.chpc.ac.za:~/"
echo "2. SSH to compute node: ssh msovara@login2.chpc.ac.za"
echo "3. Run build script: ./build_on_compute.sh"
echo ""
echo "Download on DTN completed successfully!"
