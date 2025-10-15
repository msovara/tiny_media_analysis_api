#!/bin/bash
# ARWpost Complete Workflow for Lengau Cluster
# This script orchestrates the download on DTN and build on compute node

echo "=== ARWpost Complete Workflow ==="
echo "This workflow will:"
echo "1. Download ARWpost source on DTN node (has internet)"
echo "2. Build ARWpost on compute node (has Intel compiler)"
echo ""

# Step 1: Download on DTN
echo "Step 1: Downloading ARWpost source on DTN node..."
echo "Run this command on DTN node:"
echo "ssh msovara@dtn.chpc.ac.za"
echo "chmod +x download_on_dtn.sh"
echo "./download_on_dtn.sh"
echo ""

# Step 2: Transfer to compute node
echo "Step 2: Transfer to compute node..."
echo "Run this command from DTN:"
echo "scp -r /home/msovara/lustre/SoftwareBuilds/ARWpost-download msovara@login2.chpc.ac.za:~/"
echo ""

# Step 3: Build on compute node
echo "Step 3: Building ARWpost on compute node..."
echo "Run these commands on compute node:"
echo "ssh msovara@login2.chpc.ac.za"
echo "cd ~/ARWpost-download"
echo "chmod +x build_on_compute.sh"
echo "./build_on_compute.sh"
echo ""

# Step 4: Test
echo "Step 4: Testing ARWpost..."
echo "Run these commands to test:"
echo "module load chpc/earth/arwpost-full/3.1"
echo "ARWpost"
echo ""

echo "=== Workflow Complete ==="
echo "Follow the steps above to build the full ARWpost!"









