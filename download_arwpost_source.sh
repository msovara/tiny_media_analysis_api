#!/bin/bash
# ARWpost Source Download Script for Lengau Cluster
# This script downloads the complete ARWpost source code

set -e  # Exit on any error

# Configuration
SOURCE_DIR="/home/apps/chpc/earth/ARWpost-full/source"
ARWPOST_VERSION="3.1"

# Multiple download URLs to try
ARWPOST_URLS=(
    "https://www2.mmm.ucar.edu/wrf/src/ARWpost_V${ARWPOST_VERSION}.tar.gz"
    "https://www2.mmm.ucar.edu/wrf/src/ARWpost.tar.gz"
    "https://github.com/NCAR/ARWpost/archive/v${ARWPOST_VERSION}.tar.gz"
    "https://github.com/NCAR/ARWpost/archive/main.tar.gz"
    "https://www2.mmm.ucar.edu/wrf/src/ARWpost_V3.0.tar.gz"
    "https://www2.mmm.ucar.edu/wrf/src/ARWpost_V2.2.tar.gz"
)

echo "=== ARWpost Source Download Script ==="
echo "Source directory: ${SOURCE_DIR}"
echo "ARWpost version: ${ARWPOST_VERSION}"
echo "Download URL: ${ARWPOST_URL}"
echo ""

# Create source directory
mkdir -p "${SOURCE_DIR}"
cd "${SOURCE_DIR}"

# Check if source already exists
if [ -d "ARWpost" ]; then
    echo "✓ ARWpost source already exists at ${SOURCE_DIR}/ARWpost"
    echo "To re-download, remove the existing directory first:"
    echo "rm -rf ${SOURCE_DIR}/ARWpost"
    exit 0
fi

# Check for download tools
echo "Checking for download tools..."
if command -v wget >/dev/null 2>&1; then
    DOWNLOAD_TOOL="wget"
    DOWNLOAD_CMD="wget -O ARWpost.tar.gz"
elif command -v curl >/dev/null 2>&1; then
    DOWNLOAD_TOOL="curl"
    DOWNLOAD_CMD="curl -L -o ARWpost.tar.gz"
else
    echo "✗ Neither wget nor curl available"
    echo "Please install wget or curl to download ARWpost source"
    exit 1
fi

echo "✓ Using ${DOWNLOAD_TOOL} for download"

# Download ARWpost source
echo "Downloading ARWpost source..."
echo "Trying multiple download URLs..."

DOWNLOAD_SUCCESS=false
for url in "${ARWPOST_URLS[@]}"; do
    echo "Trying URL: ${url}"
    ${DOWNLOAD_CMD} "${url}"
    
    if [ $? -eq 0 ] && [ -f "ARWpost.tar.gz" ]; then
        echo "✓ Download completed successfully from: ${url}"
        DOWNLOAD_SUCCESS=true
        break
    else
        echo "⚠ Download failed from: ${url}"
        rm -f ARWpost.tar.gz 2>/dev/null || true
    fi
done

if [ "$DOWNLOAD_SUCCESS" = false ]; then
    echo "✗ All download attempts failed"
    echo "Trying to find ARWpost in existing WRF installations..."
    
    # Look for existing ARWpost in WRF installations
    WRF_DIRS=(
        "/home/apps/chpc/earth/WRF"
        "/home/apps/chpc/earth/WRF-4.0"
        "/home/apps/chpc/earth/WRF-3.9"
        "/apps/chpc/earth/WRF"
        "/apps/chpc/earth/WRF-4.0"
        "/apps/chpc/earth/WRF-3.9"
    )
    
    for wrf_dir in "${WRF_DIRS[@]}"; do
        if [ -d "${wrf_dir}" ]; then
            echo "Checking WRF directory: ${wrf_dir}"
            if [ -d "${wrf_dir}/ARWpost" ]; then
                echo "✓ Found existing ARWpost in: ${wrf_dir}/ARWpost"
                cp -r "${wrf_dir}/ARWpost" .
                DOWNLOAD_SUCCESS=true
                break
            fi
        fi
    done
    
    if [ "$DOWNLOAD_SUCCESS" = false ]; then
        echo "✗ No ARWpost source found"
        echo "Please manually download ARWpost source and place it in: ${SOURCE_DIR}/ARWpost"
        exit 1
    fi
fi

# Verify download
if [ -f "ARWpost.tar.gz" ]; then
    echo "✓ ARWpost.tar.gz downloaded successfully"
    ls -lh ARWpost.tar.gz
else
    echo "✗ ARWpost.tar.gz not found"
    exit 1
fi

# Extract source
echo "Extracting ARWpost source..."
if [ -f "ARWpost.tar.gz" ]; then
    tar -xzf ARWpost.tar.gz
    if [ $? -eq 0 ]; then
        echo "✓ Extraction completed successfully"
    else
        echo "✗ Extraction failed"
        exit 1
    fi
else
    echo "✓ Using existing ARWpost source (no extraction needed)"
fi

# Verify extraction
if [ -d "ARWpost" ]; then
    echo "✓ ARWpost directory created"
    echo "Source structure:"
    ls -la ARWpost/
    echo ""
    echo "Source files:"
    find ARWpost -name "*.f90" -o -name "*.f" | head -10
    echo "..."
    echo "Total source files: $(find ARWpost -name "*.f90" -o -name "*.f" | wc -l)"
else
    echo "✗ ARWpost directory not found after extraction"
    exit 1
fi

# Clean up
echo "Cleaning up download file..."
rm -f ARWpost.tar.gz

# Create source info file
cat > "${SOURCE_DIR}/source_info.txt" << EOF
ARWpost Source Information
=========================
Download Date: $(date)
Source Directory: ${SOURCE_DIR}
ARWpost Version: ${ARWPOST_VERSION}
Download URL: ${ARWPOST_URL}
Download Tool: ${DOWNLOAD_TOOL}

Source Structure:
$(find ARWpost -type f -name "*.f90" -o -name "*.f" | sort)

Total Files: $(find ARWpost -type f -name "*.f90" -o -name "*.f" | wc -l)
Total Size: $(du -sh ARWpost | cut -f1)

Next Steps:
1. Run build_arwpost.sh to compile ARWpost
2. Run install_arwpost.sh to install ARWpost
3. Run test_arwpost.sh to test ARWpost
EOF

echo ""
echo "=== ARWpost Source Download Complete ==="
echo "Source downloaded to: ${SOURCE_DIR}/ARWpost"
echo "Source info saved to: ${SOURCE_DIR}/source_info.txt"
echo ""
echo "Next steps:"
echo "1. Run: ./build_arwpost.sh"
echo "2. Run: ./install_arwpost.sh"
echo "3. Run: ./test_arwpost.sh"
echo ""
echo "ARWpost source download completed successfully!"
