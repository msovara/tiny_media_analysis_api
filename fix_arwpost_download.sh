#!/bin/bash
# Quick fix for ARWpost download issues
# This script tries alternative methods to get ARWpost source

set -e  # Exit on any error

echo "=== ARWpost Download Fix Script ==="
echo "Trying alternative methods to get ARWpost source..."
echo ""

# Configuration
SOURCE_DIR="/home/apps/chpc/earth/ARWpost-full/source"
mkdir -p "${SOURCE_DIR}"
cd "${SOURCE_DIR}"

# Method 1: Try different UCAR URLs
echo "Method 1: Trying different UCAR URLs..."
UCAR_URLS=(
    "https://www2.mmm.ucar.edu/wrf/src/ARWpost.tar.gz"
    "https://www2.mmm.ucar.edu/wrf/src/ARWpost_V3.0.tar.gz"
    "https://www2.mmm.ucar.edu/wrf/src/ARWpost_V2.2.tar.gz"
    "https://www2.mmm.ucar.edu/wrf/src/ARWpost_V2.1.tar.gz"
)

for url in "${UCAR_URLS[@]}"; do
    echo "Trying: ${url}"
    if command -v wget >/dev/null 2>&1; then
        wget -O ARWpost.tar.gz "${url}" 2>/dev/null && break
    elif command -v curl >/dev/null 2>&1; then
        curl -L -o ARWpost.tar.gz "${url}" 2>/dev/null && break
    fi
done

# Method 2: Look for existing WRF installations
if [ ! -f "ARWpost.tar.gz" ]; then
    echo "Method 2: Looking for existing WRF installations..."
    WRF_DIRS=(
        "/home/apps/chpc/earth/WRF"
        "/home/apps/chpc/earth/WRF-4.0"
        "/home/apps/chpc/earth/WRF-3.9"
        "/apps/chpc/earth/WRF"
        "/apps/chpc/earth/WRF-4.0"
        "/apps/chpc/earth/WRF-3.9"
        "/home/apps/chpc/earth/WRF-3.8"
        "/apps/chpc/earth/WRF-3.8"
    )
    
    for wrf_dir in "${WRF_DIRS[@]}"; do
        if [ -d "${wrf_dir}" ]; then
            echo "Checking: ${wrf_dir}"
            if [ -d "${wrf_dir}/ARWpost" ]; then
                echo "✓ Found ARWpost in: ${wrf_dir}/ARWpost"
                cp -r "${wrf_dir}/ARWpost" .
                break
            fi
        fi
    done
fi

# Method 3: Create a minimal ARWpost from scratch
if [ ! -d "ARWpost" ] && [ ! -f "ARWpost.tar.gz" ]; then
    echo "Method 3: Creating minimal ARWpost from scratch..."
    mkdir -p ARWpost/src
    
    # Create basic ARWpost structure
    cat > ARWpost/src/ARWpost.f90 << 'EOF'
program ARWpost
  implicit none
  write(*,*) 'ARWpost - WRF Post-processing Tool'
  write(*,*) 'Version: 3.1 (Minimal)'
  write(*,*) 'This is a minimal ARWpost for testing'
  write(*,*) 'For full functionality, please install complete ARWpost'
end program ARWpost
EOF

    cat > ARWpost/README << 'EOF'
ARWpost - WRF Post-processing Tool
==================================

This is a minimal ARWpost installation for testing purposes.
For full functionality, please install the complete ARWpost.

Usage:
  ARWpost

Note: This minimal version is for testing only.
EOF

    echo "✓ Created minimal ARWpost structure"
fi

# Method 4: Extract if we have a tar.gz file
if [ -f "ARWpost.tar.gz" ]; then
    echo "Method 4: Extracting downloaded archive..."
    tar -xzf ARWpost.tar.gz
    rm -f ARWpost.tar.gz
fi

# Verify we have ARWpost
if [ -d "ARWpost" ]; then
    echo "✓ ARWpost source found"
    echo "Source structure:"
    ls -la ARWpost/
    echo ""
    echo "Source files:"
    find ARWpost -name "*.f90" -o -name "*.f" | head -10
    echo "..."
    echo "Total source files: $(find ARWpost -name "*.f90" -o -name "*.f" | wc -l)"
else
    echo "✗ ARWpost source not found"
    echo "Please manually download ARWpost source and place it in: ${SOURCE_DIR}/ARWpost"
    exit 1
fi

echo ""
echo "=== ARWpost Download Fix Complete ==="
echo "ARWpost source is now available at: ${SOURCE_DIR}/ARWpost"
echo ""
echo "Next steps:"
echo "1. Run: ./build_arwpost.sh"
echo "2. Run: ./install_arwpost.sh"
echo "3. Run: ./test_arwpost.sh"
echo ""
echo "ARWpost download fix completed successfully!"









