#!/bin/bash
# DMI Extraction from HadISST Data on Lengau Cluster
# This script extracts DMI data from HadISST sea surface temperature data

echo "=========================================="
echo "DMI EXTRACTION FROM HADISST - LENGAU CLUSTER"
echo "=========================================="
echo "Date: $(date)"
echo "User: $(whoami)"
echo "Host: $(hostname)"
echo "Working Directory: $(pwd)"
echo "=========================================="

# Set up environment
module load python/3.8.5
module load gcc/9.3.0

# Create necessary directories
mkdir -p output/processed
mkdir -p output/plots
mkdir -p logs

# Set up logging
LOG_FILE="logs/dmi_extraction_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG_FILE")
exec 2>&1

echo "Log file: $LOG_FILE"
echo "Starting DMI extraction from HadISST data..."

# Check if HadISST file exists
if [ ! -f "HadISST_sst.nc" ]; then
    echo "✗ HadISST_sst.nc file not found in current directory"
    echo "Please ensure the file is in the current directory or update the path in the script"
    exit 1
fi

echo "✓ Found HadISST_sst.nc file"

# Run the DMI extraction
echo "Running DMI extraction..."
python3 extract_dmi_from_hadisst.py

# Check results
echo ""
echo "=========================================="
echo "DMI EXTRACTION RESULTS"
echo "=========================================="
echo "Output directory contents:"
ls -la output/processed/
echo ""
echo "Plots directory contents:"
ls -la output/plots/
echo ""
echo "Log file: $LOG_FILE"
echo "=========================================="

echo "DMI extraction workflow completed!"
















