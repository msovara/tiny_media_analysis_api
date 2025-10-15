#!/bin/bash

# Debug script to check NetCDF libraries and linking

echo "=== NetCDF Debug Script ==="

# Load modules
module purge
module load chpc/parallel_studio_xe/16.0.1/2016.1.150
module load chpc/zlib/1.2.8/intel/16.0.1
module load chpc/netcdf/4.1.3/intel-2016
module load chpc/hdf5/1.8.16/intel/16.0.1

echo "Modules loaded. Checking NetCDF installation..."

# Check NetCDF path
NETCDF_PATH="/apps/chpc/earth/netcdf-4.1.3-intel2016"
echo "NetCDF path: ${NETCDF_PATH}"

# Check what libraries exist
echo ""
echo "Checking NetCDF libraries in ${NETCDF_PATH}/lib/:"
ls -la ${NETCDF_PATH}/lib/ | grep -E "(netcdf|\.a|\.so)"

echo ""
echo "Checking NetCDF headers in ${NETCDF_PATH}/include/:"
ls -la ${NETCDF_PATH}/include/ | grep -E "(netcdf|\.h)"

echo ""
echo "Checking environment variables:"
echo "NETCDF: ${NETCDF}"
echo "NETCDF_ROOT: ${NETCDF_ROOT}"
echo "CPATH: ${CPATH}"
echo "LIBRARY_PATH: ${LIBRARY_PATH}"
echo "LD_LIBRARY_PATH: ${LD_LIBRARY_PATH}"

echo ""
echo "Testing NetCDF compilation..."

# Create a simple test program
cat > test_netcdf.f90 << 'EOF'
program test_netcdf
  implicit none
  
  print *, "NetCDF test program"
  print *, "Testing if NetCDF libraries can be linked"
  
end program test_netcdf
EOF

echo "Compiling test program..."
ifort -I${NETCDF_PATH}/include -L${NETCDF_PATH}/lib -lnetcdff -lnetcdf test_netcdf.f90 -o test_netcdf

if [ $? -eq 0 ]; then
    echo "✓ Test compilation successful"
    echo "Running test program..."
    ./test_netcdf
else
    echo "✗ Test compilation failed"
    echo "Trying alternative linking..."
    ifort -I${NETCDF_PATH}/include -L${NETCDF_PATH}/lib -lnetcdf -lnetcdff test_netcdf.f90 -o test_netcdf
    if [ $? -eq 0 ]; then
        echo "✓ Alternative linking successful"
        ./test_netcdf
    else
        echo "✗ Alternative linking also failed"
    fi
fi

echo ""
echo "Debug complete."
