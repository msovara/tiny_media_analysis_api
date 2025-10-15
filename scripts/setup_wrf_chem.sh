#!/bin/bash

# WRF-Chem Setup Script for HPC Clusters
# This script sets up WRF-Chem environment and fixes common issues

set -e  # Exit on any error

# Default values
NODES=4
CORES=16
WALLTIME="24:00:00"
QUEUE="normal"
WRF_DIR=""
CHEM_DATA_DIR=""
WRF_EXEC_DIR=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

WRF-Chem Setup Script for HPC Clusters

OPTIONS:
    -d, --wrf-dir DIR          WRF run directory (required)
    -c, --chem-data DIR        Chemistry data directory (required)
    -e, --exec-dir DIR         WRF-Chem executables directory (required)
    -n, --nodes N              Number of nodes (default: 4)
    -p, --cores N              Cores per node (default: 16)
    -t, --walltime TIME        Walltime (default: 24:00:00)
    -q, --queue QUEUE          Queue name (default: normal)
    -h, --help                 Show this help message

EXAMPLES:
    $0 -d /path/to/wrf -c /path/to/chem -e /path/to/exec
    $0 --wrf-dir /home/user/wrf --chem-data /home/user/chem --exec-dir /home/user/exec --nodes 8 --cores 32

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--wrf-dir)
            WRF_DIR="$2"
            shift 2
            ;;
        -c|--chem-data)
            CHEM_DATA_DIR="$2"
            shift 2
            ;;
        -e|--exec-dir)
            WRF_EXEC_DIR="$2"
            shift 2
            ;;
        -n|--nodes)
            NODES="$2"
            shift 2
            ;;
        -p|--cores)
            CORES="$2"
            shift 2
            ;;
        -t|--walltime)
            WALLTIME="$2"
            shift 2
            ;;
        -q|--queue)
            QUEUE="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Validate required parameters
if [[ -z "$WRF_DIR" || -z "$CHEM_DATA_DIR" || -z "$WRF_EXEC_DIR" ]]; then
    print_error "Missing required parameters"
    show_usage
    exit 1
fi

print_status "Starting WRF-Chem setup..."
print_status "WRF Directory: $WRF_DIR"
print_status "Chemistry Data: $CHEM_DATA_DIR"
print_status "Executables: $WRF_EXEC_DIR"
print_status "Nodes: $NODES, Cores: $CORES, Walltime: $WALLTIME"

# Check if directories exist
if [[ ! -d "$WRF_DIR" ]]; then
    print_error "WRF directory does not exist: $WRF_DIR"
    exit 1
fi

if [[ ! -d "$CHEM_DATA_DIR" ]]; then
    print_error "Chemistry data directory does not exist: $CHEM_DATA_DIR"
    exit 1
fi

if [[ ! -d "$WRF_EXEC_DIR" ]]; then
    print_error "WRF executables directory does not exist: $WRF_EXEC_DIR"
    exit 1
fi

# Navigate to WRF directory
cd "$WRF_DIR"
print_status "Changed to WRF directory: $(pwd)"

# Create symbolic links to chemistry files
print_status "Creating symbolic links to chemistry files..."
ln -sf "$CHEM_DATA_DIR"/wrfchemi_d* . 2>/dev/null || print_warning "No wrfchemi files found"
ln -sf "$CHEM_DATA_DIR"/wrffirechemi_d* . 2>/dev/null || print_warning "No wrffirechemi files found"
ln -sf "$CHEM_DATA_DIR"/wrfbiochemi_d* . 2>/dev/null || print_warning "No wrfbiochemi files found"

# Create symbolic links to executables
print_status "Creating symbolic links to WRF-Chem executables..."
ln -sf "$WRF_EXEC_DIR"/real.exe .
ln -sf "$WRF_EXEC_DIR"/wrf.exe .

# Fix namelist.input if it exists
if [[ -f "namelist.input" ]]; then
    print_status "Fixing namelist.input..."
    
    # Backup original namelist
    cp namelist.input namelist.input.backup
    print_status "Backup created: namelist.input.backup"
    
    # Fix chem_in_opt
    sed -i 's/chem_in_opt.*=.*1.*,.*1.*,/chem_in_opt = 0, 0,/' namelist.input
    print_success "Fixed chem_in_opt in namelist.input"
else
    print_warning "namelist.input not found - you may need to create it manually"
fi

# Create PBS job script
print_status "Creating PBS job script..."
cat > wrf_chem_job.pbs << EOF
#!/bin/bash
#PBS -N wrf_chem_simulation
#PBS -q $QUEUE
#PBS -l nodes=$NODES:ppn=$CORES
#PBS -l mem=64GB
#PBS -l walltime=$WALLTIME
#PBS -o $WRF_DIR/wrf_chem.out
#PBS -e $WRF_DIR/wrf_chem.err
#PBS -j oe

# Load modules
module purge
module load chpc/parallel_studio_xe/16.0.1/2016.1.150
module load chpc/netcdf/4.4.3-F/intel/16.0.1
module load chpc/hdf5/1.8.16/intel/16.0.1

# Set environment
export OMP_NUM_THREADS=1
export I_MPI_PIN_DOMAIN=omp

# Change to working directory
cd $WRF_DIR

# Run real.exe
echo "Running real.exe..."
mpirun -np \$((PBS_NUM_NODES * PBS_NUM_PPN)) ./real.exe

# Run wrf.exe
echo "Running wrf.exe..."
mpirun -np \$((PBS_NUM_NODES * PBS_NUM_PPN)) ./wrf.exe

echo "WRF-Chem simulation completed!"
EOF

print_success "PBS job script created: wrf_chem_job.pbs"

# Create verification script
print_status "Creating verification script..."
cat > verify_setup.sh << 'EOF'
#!/bin/bash

echo "=== WRF-Chem Setup Verification ==="

# Check for required files
echo "Checking for required files..."
if [[ -f "namelist.input" ]]; then
    echo "✓ namelist.input found"
else
    echo "✗ namelist.input not found"
fi

if [[ -f "real.exe" ]]; then
    echo "✓ real.exe found"
else
    echo "✗ real.exe not found"
fi

if [[ -f "wrf.exe" ]]; then
    echo "✓ wrf.exe found"
else
    echo "✗ wrf.exe not found"
fi

# Check for chemistry files
CHEM_FILES=$(ls wrfchemi_d* 2>/dev/null | wc -l)
if [[ $CHEM_FILES -gt 0 ]]; then
    echo "✓ Found $CHEM_FILES chemistry emission files"
else
    echo "✗ No chemistry emission files found"
fi

# Check namelist configuration
if [[ -f "namelist.input" ]]; then
    if grep -q "chem_in_opt.*=.*0.*,.*0" namelist.input; then
        echo "✓ chem_in_opt correctly set to 0"
    else
        echo "✗ chem_in_opt not set to 0"
    fi
fi

echo "=== Verification Complete ==="
EOF

chmod +x verify_setup.sh
print_success "Verification script created: verify_setup.sh"

# Run verification
print_status "Running setup verification..."
./verify_setup.sh

print_success "WRF-Chem setup completed successfully!"
print_status "Next steps:"
print_status "1. Review the configuration: ./verify_setup.sh"
print_status "2. Submit the job: qsub wrf_chem_job.pbs"
print_status "3. Monitor the job: qstat -u \$USER"


























