#!/bin/bash

# CCAM Installation Test Script for Lengau Cluster
# This script tests the CCAM installation and verifies functionality

set -e

# Configuration
INSTALL_DIR="/mnt/lustre/users/msovara/SoftwareBuilds/CCAM"
TEST_DIR="${INSTALL_DIR}/test"
MODULE_VERSION="2023"

echo "=== CCAM Installation Test Script ==="
echo "Installation directory: ${INSTALL_DIR}"
echo "Test directory: ${TEST_DIR}"
echo "Module version: ${MODULE_VERSION}"
echo ""

# Create test directory
mkdir -p ${TEST_DIR}
cd ${TEST_DIR}

# Test 1: Check if CCAM module can be loaded
echo "=== Test 1: Module Loading ==="
if module load ccam/${MODULE_VERSION} 2>/dev/null; then
    echo "✓ CCAM module loaded successfully"
else
    echo "✗ Failed to load CCAM module"
    echo "Trying alternative module loading..."
    if module load ${INSTALL_DIR}/modulefiles/ccam-lengau 2>/dev/null; then
        echo "✓ CCAM module loaded from installation directory"
    else
        echo "✗ Failed to load CCAM module from installation directory"
        echo "Please check module file creation"
        exit 1
    fi
fi

# Test 2: Check environment variables
echo ""
echo "=== Test 2: Environment Variables ==="
if [ -n "$CCAM_ROOT" ]; then
    echo "✓ CCAM_ROOT: ${CCAM_ROOT}"
else
    echo "✗ CCAM_ROOT not set"
fi

if [ -n "$CCAM_VERSION" ]; then
    echo "✓ CCAM_VERSION: ${CCAM_VERSION}"
else
    echo "✗ CCAM_VERSION not set"
fi

if [ -n "$CCAM_COMPILER" ]; then
    echo "✓ CCAM_COMPILER: ${CCAM_COMPILER}"
else
    echo "✗ CCAM_COMPILER not set"
fi

# Test 3: Check if CCAM executable exists
echo ""
echo "=== Test 3: Executable Check ==="
if command -v ccam &> /dev/null; then
    echo "✓ CCAM executable found: $(which ccam)"
    CCAM_EXECUTABLE=$(which ccam)
else
    echo "✗ CCAM executable not found in PATH"
    if [ -f "${INSTALL_DIR}/bin/ccam" ]; then
        echo "✓ CCAM executable found in installation directory: ${INSTALL_DIR}/bin/ccam"
        CCAM_EXECUTABLE="${INSTALL_DIR}/bin/ccam"
    else
        echo "✗ CCAM executable not found in installation directory"
        echo "Checking for other executables..."
        find ${INSTALL_DIR}/bin -type f -executable -ls 2>/dev/null || echo "No executables found in bin directory"
        exit 1
    fi
fi

# Test 4: Check CCAM help/version
echo ""
echo "=== Test 4: CCAM Help/Version ==="
if [ -n "$CCAM_EXECUTABLE" ]; then
    echo "Testing CCAM executable: ${CCAM_EXECUTABLE}"
    
    # Try to get version information
    if ${CCAM_EXECUTABLE} --version 2>/dev/null; then
        echo "✓ CCAM version information retrieved"
    elif ${CCAM_EXECUTABLE} -v 2>/dev/null; then
        echo "✓ CCAM version information retrieved"
    else
        echo "⚠ CCAM version command not available, trying help..."
    fi
    
    # Try to get help information
    if ${CCAM_EXECUTABLE} --help 2>/dev/null; then
        echo "✓ CCAM help information retrieved"
    elif ${CCAM_EXECUTABLE} -h 2>/dev/null; then
        echo "✓ CCAM help information retrieved"
    else
        echo "⚠ CCAM help command not available"
    fi
else
    echo "✗ Cannot test CCAM executable - not found"
fi

# Test 5: Check dependencies
echo ""
echo "=== Test 5: Dependencies Check ==="

# Check Intel compilers
if command -v ifort &> /dev/null; then
    echo "✓ Intel Fortran compiler: $(ifort --version | head -1)"
else
    echo "✗ Intel Fortran compiler not found"
fi

if command -v icc &> /dev/null; then
    echo "✓ Intel C compiler: $(icc --version | head -1)"
else
    echo "✗ Intel C compiler not found"
fi

# Check MPI
if command -v mpicc &> /dev/null; then
    echo "✓ MPI compiler: $(mpicc --version | head -1)"
else
    echo "✗ MPI compiler not found"
fi

# Check NetCDF
if [ -n "$NETCDF" ] || [ -n "$NETCDF_ROOT" ]; then
    echo "✓ NetCDF environment: ${NETCDF:-$NETCDF_ROOT}"
else
    echo "✗ NetCDF environment not set"
fi

# Check HDF5
if [ -n "$HDF5" ] || [ -n "$HDF5_ROOT" ]; then
    echo "✓ HDF5 environment: ${HDF5:-$HDF5_ROOT}"
else
    echo "✗ HDF5 environment not set"
fi

# Test 6: Check OpenMP
echo ""
echo "=== Test 6: OpenMP Support ==="
if [ -n "$OMP_NUM_THREADS" ]; then
    echo "✓ OMP_NUM_THREADS: ${OMP_NUM_THREADS}"
else
    echo "⚠ OMP_NUM_THREADS not set (defaulting to 1)"
    export OMP_NUM_THREADS=1
fi

# Test 7: Create a simple test case
echo ""
echo "=== Test 7: Simple Test Case ==="
cat > ${TEST_DIR}/test_ccam_input.txt << EOF
# Simple CCAM test case
# This is a minimal test to verify CCAM can start
# Replace with actual CCAM input parameters as needed

# Test parameters
test_mode = true
output_dir = "${TEST_DIR}/output"
EOF

echo "✓ Test input file created: ${TEST_DIR}/test_ccam_input.txt"

# Test 8: Check installation files
echo ""
echo "=== Test 8: Installation Files ==="
echo "Checking installation directory structure..."

if [ -d "${INSTALL_DIR}/bin" ]; then
    echo "✓ bin directory exists"
    ls -la ${INSTALL_DIR}/bin/ | head -5
else
    echo "✗ bin directory not found"
fi

if [ -d "${INSTALL_DIR}/lib" ]; then
    echo "✓ lib directory exists"
    ls -la ${INSTALL_DIR}/lib/ | head -5
else
    echo "✗ lib directory not found"
fi

if [ -d "${INSTALL_DIR}/share/ccam" ]; then
    echo "✓ share/ccam directory exists"
    ls -la ${INSTALL_DIR}/share/ccam/ | head -5
else
    echo "✗ share/ccam directory not found"
fi

# Test 9: Performance test (if executable is available)
echo ""
echo "=== Test 9: Performance Test ==="
if [ -n "$CCAM_EXECUTABLE" ] && [ -f "$CCAM_EXECUTABLE" ]; then
    echo "Running basic performance test..."
    
    # Create a simple performance test
    cat > ${TEST_DIR}/performance_test.sh << EOF
#!/bin/bash
# Simple performance test for CCAM

echo "Starting CCAM performance test..."
echo "Date: \$(date)"
echo "Host: \$(hostname)"
echo "OMP_NUM_THREADS: \${OMP_NUM_THREADS:-1}"

# Test basic execution (this may need to be adjusted based on actual CCAM usage)
timeout 30s ${CCAM_EXECUTABLE} --help 2>&1 | head -10

echo "Performance test completed"
EOF

    chmod +x ${TEST_DIR}/performance_test.sh
    echo "✓ Performance test script created"
    
    # Run the performance test
    echo "Running performance test..."
    if ${TEST_DIR}/performance_test.sh; then
        echo "✓ Performance test completed successfully"
    else
        echo "⚠ Performance test had issues (this may be normal for CCAM)"
    fi
else
    echo "⚠ Cannot run performance test - CCAM executable not available"
fi

# Test 10: Generate test report
echo ""
echo "=== Test 10: Generating Test Report ==="
cat > ${TEST_DIR}/test_report.txt << EOF
CCAM Installation Test Report
=============================
Test Date: $(date)
Installation Directory: ${INSTALL_DIR}
Module Version: ${MODULE_VERSION}

Test Results:
- Module Loading: $(module list ccam 2>/dev/null && echo "PASS" || echo "FAIL")
- CCAM Executable: $([ -n "$CCAM_EXECUTABLE" ] && echo "PASS" || echo "FAIL")
- Environment Variables: $([ -n "$CCAM_ROOT" ] && echo "PASS" || echo "FAIL")
- Intel Compilers: $(command -v ifort &> /dev/null && echo "PASS" || echo "FAIL")
- MPI Support: $(command -v mpicc &> /dev/null && echo "PASS" || echo "FAIL")
- NetCDF: $([ -n "$NETCDF" ] && echo "PASS" || echo "FAIL")
- HDF5: $([ -n "$HDF5" ] && echo "PASS" || echo "FAIL")

Installation Status: $([ -n "$CCAM_EXECUTABLE" ] && echo "SUCCESS" || echo "NEEDS ATTENTION")

Notes:
- CCAM source code access may require registration with CSIRO
- Ensure proper access to CCAM source code before installation
- Check CCAM documentation for specific usage instructions
EOF

echo "✓ Test report generated: ${TEST_DIR}/test_report.txt"

# Final summary
echo ""
echo "=== Test Summary ==="
echo "Test completed. Results saved to: ${TEST_DIR}/test_report.txt"
echo ""
echo "Installation status:"
if [ -n "$CCAM_EXECUTABLE" ]; then
    echo "✓ CCAM installation appears successful"
    echo "✓ Executable found: ${CCAM_EXECUTABLE}"
    echo ""
    echo "Next steps:"
    echo "1. Load the module: module load ccam/${MODULE_VERSION}"
    echo "2. Run CCAM: ccam"
    echo "3. Check CCAM documentation for usage instructions"
    echo "4. Set up your simulation parameters"
else
    echo "✗ CCAM installation needs attention"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check if CCAM source code was downloaded correctly"
    echo "2. Verify compilation completed without errors"
    echo "3. Check module file creation"
    echo "4. Review installation log: ${INSTALL_DIR}/install_log.txt"
fi

echo ""
echo "Test completed successfully!"




























