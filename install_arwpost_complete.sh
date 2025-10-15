#!/bin/bash

# ARWpost Complete Installation Script for Lengau Cluster
# This script orchestrates the complete download and installation process
# Can be run on a login node or compute node with internet access

set -e  # Exit on any error

# Configuration
INSTALL_DIR="/mnt/lustre/users/msovara/SoftwareBuilds/ARWpost"
DOWNLOAD_SCRIPT="download_arwpost.sh"
INSTALL_SCRIPT="install_arwpost_lengau_intel.sh"
VERIFY_SCRIPT="verify_arwpost.sh"

echo "=== ARWpost Complete Installation Script ==="
echo "Installation directory: ${INSTALL_DIR}"
echo ""

# Check if scripts exist
if [ ! -f "${DOWNLOAD_SCRIPT}" ]; then
    echo "✗ Download script not found: ${DOWNLOAD_SCRIPT}"
    exit 1
fi

if [ ! -f "${INSTALL_SCRIPT}" ]; then
    echo "✗ Install script not found: ${INSTALL_SCRIPT}"
    exit 1
fi

if [ ! -f "${VERIFY_SCRIPT}" ]; then
    echo "✗ Verify script not found: ${VERIFY_SCRIPT}"
    exit 1
fi

echo "✓ All required scripts found"

# Make scripts executable
echo "Making scripts executable..."
chmod +x ${DOWNLOAD_SCRIPT}
chmod +x ${INSTALL_SCRIPT}
chmod +x ${VERIFY_SCRIPT}
echo "✓ Scripts made executable"

# Step 1: Download source code
echo ""
echo "=== Step 1: Downloading ARWpost Source Code ==="
echo "This step can be run on any node with internet access..."
echo ""

./${DOWNLOAD_SCRIPT}

if [ $? -eq 0 ]; then
    echo "✓ Download completed successfully"
else
    echo "✗ Download failed!"
    exit 1
fi

# Step 2: Compile and install
echo ""
echo "=== Step 2: Compiling and Installing ARWpost ==="
echo "This step should be run on a compute node with Intel compilers..."
echo ""

# Check if we're on a compute node (optional check)
if [ -n "$SLURM_JOB_ID" ]; then
    echo "✓ Running on SLURM compute node (Job ID: $SLURM_JOB_ID)"
else
    echo "⚠ Not running on SLURM compute node"
    echo "  Make sure you have access to Intel compilers on this node"
fi

./${INSTALL_SCRIPT}

if [ $? -eq 0 ]; then
    echo "✓ Installation completed successfully"
else
    echo "✗ Installation failed!"
    exit 1
fi

# Step 3: Verify installation
echo ""
echo "=== Step 3: Verifying Installation ==="
echo ""

./${VERIFY_SCRIPT}

if [ $? -eq 0 ]; then
    echo "✓ Verification completed successfully"
else
    echo "✗ Verification failed!"
    exit 1
fi

echo ""
echo "=== Complete Installation Summary ==="
echo "ARWpost has been successfully installed on Lengau cluster!"
echo ""
echo "Installation location: ${INSTALL_DIR}"
echo ""
echo "Directory structure:"
echo "${INSTALL_DIR}/"
echo "├── bin/ARWpost                    # Executable"
echo "├── share/arwpost/                 # Source files"
echo "├── modulefiles/arwpost-lengau     # Module file"
echo "├── setup_arwpost_lengau.sh        # Setup script"
echo "├── install_log.txt                # Installation log"
echo "├── build_info.txt                 # Build information"
echo "├── source/                        # Downloaded source"
echo "└── build/                         # Build directory"
echo ""
echo "To use ARWpost:"
echo "1. Load the module: module load ${INSTALL_DIR}/modulefiles/arwpost-lengau"
echo "2. Or source the setup script: source ${INSTALL_DIR}/setup_arwpost_lengau.sh"
echo "3. Run ARWpost: ARWpost"
echo ""
echo "Installation completed successfully!"


