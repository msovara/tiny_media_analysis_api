#!/bin/bash

# ARWpost Dependency Checker for Lengau Cluster
# This script checks for all required dependencies

echo "=== ARWpost Dependency Checker ==="
echo "Checking prerequisites and dependencies..."
echo ""

# Check system information
echo "1. System Information:"
echo "   OS: $(uname -s)"
echo "   Architecture: $(uname -m)"
echo "   Available memory: $(free -h | grep Mem | awk '{print $2}')"
echo "   Available disk space: $(df -h /mnt/lustre/users/msovara/SoftwareBuilds/ARWpost | tail -1 | awk '{print $4}')"
echo ""

# Check write permissions
echo "2. Directory Permissions:"
if [ -w "/mnt/lustre/users/msovara/SoftwareBuilds/ARWpost" ]; then
    echo "   ✓ Write access to /mnt/lustre/users/msovara/SoftwareBuilds/ARWpost"
else
    echo "   ✗ No write access to /mnt/lustre/users/msovara/SoftwareBuilds/ARWpost"
    echo "   Creating directory..."
    mkdir -p /mnt/lustre/users/msovara/SoftwareBuilds/ARWpost
fi
echo ""

# Check available modules
echo "3. Available Modules:"
echo "   Loading module list..."
module avail 2>/dev/null | grep -E "(gcc|gfortran|netcdf|hdf5|mpi)" | head -20
echo ""

# Check compilers
echo "4. Compiler Availability:"
echo "   Checking GCC..."
if command -v gcc &> /dev/null; then
    echo "   ✓ GCC found: $(gcc --version | head -1)"
else
    echo "   ✗ GCC not found"
fi

echo "   Checking GFortran..."
if command -v gfortran &> /dev/null; then
    echo "   ✓ GFortran found: $(gfortran --version | head -1)"
else
    echo "   ✗ GFortran not found"
fi

echo "   Checking G++..."
if command -v g++ &> /dev/null; then
    echo "   ✓ G++ found: $(g++ --version | head -1)"
else
    echo "   ✗ G++ not found"
fi

echo "   Checking Intel C Compiler (icc)..."
if command -v icc &> /dev/null; then
    echo "   ✓ Intel C Compiler found: $(icc --version | head -1)"
else
    echo "   ✗ Intel C Compiler not found"
fi

echo "   Checking Intel Fortran Compiler (ifort)..."
if command -v ifort &> /dev/null; then
    echo "   ✓ Intel Fortran Compiler found: $(ifort --version | head -1)"
else
    echo "   ✗ Intel Fortran Compiler not found"
fi

echo "   Checking Intel C++ Compiler (icpc)..."
if command -v icpc &> /dev/null; then
    echo "   ✓ Intel C++ Compiler found: $(icpc --version | head -1)"
else
    echo "   ✗ Intel C++ Compiler not found"
fi
echo ""

# Check libraries
echo "5. Library Dependencies:"
echo "   Checking NetCDF..."
if pkg-config --exists netcdf; then
    echo "   ✓ NetCDF found: $(pkg-config --modversion netcdf)"
    echo "   NetCDF location: $(pkg-config --variable=prefix netcdf)"
elif [ -n "$NETCDF_ROOT" ]; then
    echo "   ✓ NetCDF found via environment: $NETCDF_ROOT"
else
    echo "   ✗ NetCDF not found"
fi

echo "   Checking HDF5..."
if pkg-config --exists hdf5; then
    echo "   ✓ HDF5 found: $(pkg-config --modversion hdf5)"
    echo "   HDF5 location: $(pkg-config --variable=prefix hdf5)"
elif [ -n "$HDF5_ROOT" ]; then
    echo "   ✓ HDF5 found via environment: $HDF5_ROOT"
else
    echo "   ✗ HDF5 not found"
fi

echo "   Checking zlib..."
if pkg-config --exists zlib; then
    echo "   ✓ zlib found: $(pkg-config --modversion zlib)"
else
    echo "   ✗ zlib not found (usually included with system)"
fi
echo ""

# Check build tools
echo "6. Build Tools:"
echo "   Checking make..."
if command -v make &> /dev/null; then
    echo "   ✓ Make found: $(make --version | head -1)"
else
    echo "   ✗ Make not found"
fi

echo "   Checking wget..."
if command -v wget &> /dev/null; then
    echo "   ✓ wget found: $(wget --version | head -1)"
else
    echo "   ✗ wget not found"
fi

echo "   Checking tar..."
if command -v tar &> /dev/null; then
    echo "   ✓ tar found"
else
    echo "   ✗ tar not found"
fi
echo ""

# Check MPI (optional)
echo "7. MPI (Optional):"
if command -v mpicc &> /dev/null; then
    echo "   ✓ MPI found: $(mpicc --version | head -1)"
elif [ -n "$MPI_ROOT" ]; then
    echo "   ✓ MPI found via environment: $MPI_ROOT"
else
    echo "   - MPI not found (optional for basic installation)"
fi
echo ""

# Summary
echo "=== Dependency Summary ==="
echo "Required dependencies:"
echo "  - Compilers (gcc, gfortran, g++)"
echo "  - NetCDF library"
echo "  - HDF5 library"
echo "  - Build tools (make, wget, tar)"
echo ""
echo "Optional dependencies:"
echo "  - MPI (for parallel processing)"
echo "  - OpenMP (for shared memory parallelism)"
echo ""

# Recommendations
echo "=== Recommendations ==="
echo "If any required dependencies are missing:"
echo "1. Load appropriate modules:"
echo "   module load chpc/compiler/gcc-9.3.0"
echo "   module load chpc/netcdf/4.7.4"
echo "   module load chpc/hdf5/1.12.0"
echo ""
echo "2. Or contact CHPC support for missing libraries"
echo "3. Check module avail for exact module names on your system"
echo ""

echo "Dependency check completed!"
