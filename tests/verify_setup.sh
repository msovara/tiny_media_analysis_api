#!/bin/bash

# WRF-Chem Setup Verification Script
# This script verifies that WRF-Chem is properly configured and ready to run

set -e  # Exit on any error

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

WRF-Chem Setup Verification Script

OPTIONS:
    --check-files              Check for required files only
    --check-executables        Check for WRF-Chem executables only
    --check-chemistry          Check for chemistry files only
    --check-namelist           Check namelist.input configuration only
    --check-modules            Check loaded modules only
    --verbose                  Verbose output
    -h, --help                 Show this help message

EXAMPLES:
    $0                                    # Run all checks
    $0 --check-files --check-executables # Check files and executables only
    $0 --verbose                          # Run all checks with verbose output

EOF
}

# Default values
CHECK_FILES=true
CHECK_EXECUTABLES=true
CHECK_CHEMISTRY=true
CHECK_NAMELIST=true
CHECK_MODULES=true
VERBOSE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --check-files)
            CHECK_FILES=true
            CHECK_EXECUTABLES=false
            CHECK_CHEMISTRY=false
            CHECK_NAMELIST=false
            CHECK_MODULES=false
            shift
            ;;
        --check-executables)
            CHECK_FILES=false
            CHECK_EXECUTABLES=true
            CHECK_CHEMISTRY=false
            CHECK_NAMELIST=false
            CHECK_MODULES=false
            shift
            ;;
        --check-chemistry)
            CHECK_FILES=false
            CHECK_EXECUTABLES=false
            CHECK_CHEMISTRY=true
            CHECK_NAMELIST=false
            CHECK_MODULES=false
            shift
            ;;
        --check-namelist)
            CHECK_FILES=false
            CHECK_EXECUTABLES=false
            CHECK_CHEMISTRY=false
            CHECK_NAMELIST=true
            CHECK_MODULES=false
            shift
            ;;
        --check-modules)
            CHECK_FILES=false
            CHECK_EXECUTABLES=false
            CHECK_CHEMISTRY=false
            CHECK_NAMELIST=false
            CHECK_MODULES=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
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

print_status "WRF-Chem Setup Verification"
print_status "============================"

# Initialize counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# Function to run a check
run_check() {
    local check_name="$1"
    local check_function="$2"
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    print_status "Checking: $check_name"
    
    if $check_function; then
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
    echo ""
}

# Function to check for required files
check_files() {
    local files_found=0
    local total_files=0
    
    # Check for namelist.input
    total_files=$((total_files + 1))
    if [[ -f "namelist.input" ]]; then
        print_success "✓ namelist.input found"
        files_found=$((files_found + 1))
    else
        print_error "✗ namelist.input not found"
        return 1
    fi
    
    # Check for WPS files
    total_files=$((total_files + 1))
    WPS_FILES=$(ls met_em.d01.* 2>/dev/null | wc -l)
    if [[ $WPS_FILES -gt 0 ]]; then
        print_success "✓ Found $WPS_FILES WPS files"
        files_found=$((files_found + 1))
    else
        print_error "✗ No WPS files found"
        return 1
    fi
    
    return 0
}

# Function to check for WRF-Chem executables
check_executables() {
    local exec_found=0
    local total_exec=0
    
    # Check for real.exe
    total_exec=$((total_exec + 1))
    if [[ -f "real.exe" ]]; then
        print_success "✓ real.exe found"
        exec_found=$((exec_found + 1))
        if [[ "$VERBOSE" == true ]]; then
            print_status "  Size: $(ls -lh real.exe | awk '{print $5}')"
            print_status "  Permissions: $(ls -l real.exe | awk '{print $1}')"
        fi
    else
        print_error "✗ real.exe not found"
        return 1
    fi
    
    # Check for wrf.exe
    total_exec=$((total_exec + 1))
    if [[ -f "wrf.exe" ]]; then
        print_success "✓ wrf.exe found"
        exec_found=$((exec_found + 1))
        if [[ "$VERBOSE" == true ]]; then
            print_status "  Size: $(ls -lh wrf.exe | awk '{print $5}')"
            print_status "  Permissions: $(ls -l wrf.exe | awk '{print $1}')"
        fi
    else
        print_error "✗ wrf.exe not found"
        return 1
    fi
    
    return 0
}

# Function to check for chemistry files
check_chemistry() {
    local chem_found=0
    local total_chem=0
    
    # Check for chemistry emission files
    total_chem=$((total_chem + 1))
    CHEM_FILES=$(ls wrfchemi_d* 2>/dev/null | wc -l)
    if [[ $CHEM_FILES -gt 0 ]]; then
        print_success "✓ Found $CHEM_FILES chemistry emission files"
        chem_found=$((chem_found + 1))
        if [[ "$VERBOSE" == true ]]; then
            print_status "  Files: $(ls wrfchemi_d* 2>/dev/null | head -3 | tr '\n' ' ')"
            if [[ $CHEM_FILES -gt 3 ]]; then
                print_status "  ... and $((CHEM_FILES - 3)) more"
            fi
        fi
    else
        print_warning "⚠ No chemistry emission files found"
        WARNING_CHECKS=$((WARNING_CHECKS + 1))
    fi
    
    # Check for fire emission files
    FIRE_FILES=$(ls wrffirechemi_d* 2>/dev/null | wc -l)
    if [[ $FIRE_FILES -gt 0 ]]; then
        print_success "✓ Found $FIRE_FILES fire emission files"
        chem_found=$((chem_found + 1))
    else
        print_warning "⚠ No fire emission files found"
    fi
    
    # Check for biogenic emission files
    BIO_FILES=$(ls wrfbiochemi_d* 2>/dev/null | wc -l)
    if [[ $BIO_FILES -gt 0 ]]; then
        print_success "✓ Found $BIO_FILES biogenic emission files"
        chem_found=$((chem_found + 1))
    else
        print_warning "⚠ No biogenic emission files found"
    fi
    
    return 0
}

# Function to check namelist configuration
check_namelist() {
    if [[ ! -f "namelist.input" ]]; then
        print_error "✗ namelist.input not found"
        return 1
    fi
    
    local config_ok=true
    
    # Check chem_in_opt
    if grep -q "chem_in_opt.*=.*0.*,.*0" namelist.input; then
        print_success "✓ chem_in_opt correctly set to 0"
    elif grep -q "chem_in_opt.*=.*1.*,.*1" namelist.input; then
        print_error "✗ chem_in_opt set to 1 - this will cause metadata error"
        config_ok=false
    else
        print_warning "⚠ chem_in_opt not found or not set"
    fi
    
    # Check chem_opt
    if grep -q "chem_opt.*=" namelist.input; then
        CHEM_OPT=$(grep "chem_opt.*=" namelist.input | head -1)
        print_success "✓ Chemistry option found: $CHEM_OPT"
    else
        print_warning "⚠ No chem_opt found"
    fi
    
    # Check have_bcs_chem
    if grep -q "have_bcs_chem.*=.*\.true\." namelist.input; then
        print_success "✓ have_bcs_chem set to .true."
    else
        print_warning "⚠ have_bcs_chem not set to .true."
    fi
    
    if [[ "$VERBOSE" == true ]]; then
        print_status "Chemistry configuration:"
        grep -A 5 -B 5 "&chem" namelist.input | head -20
    fi
    
    if [[ "$config_ok" == true ]]; then
        return 0
    else
        return 1
    fi
}

# Function to check loaded modules
check_modules() {
    if command -v module &> /dev/null; then
        print_status "Loaded modules:"
        module list 2>/dev/null || print_warning "Cannot list modules"
        
        # Check for specific modules
        if module list 2>/dev/null | grep -q "chpc/parallel_studio_xe"; then
            print_success "✓ Intel compiler module loaded"
        else
            print_warning "⚠ Intel compiler module not loaded"
        fi
        
        if module list 2>/dev/null | grep -q "chpc/netcdf"; then
            print_success "✓ NetCDF module loaded"
        else
            print_warning "⚠ NetCDF module not loaded"
        fi
        
        if module list 2>/dev/null | grep -q "chpc/hdf5"; then
            print_success "✓ HDF5 module loaded"
        else
            print_warning "⚠ HDF5 module not loaded"
        fi
    else
        print_warning "⚠ Module system not available"
    fi
    
    return 0
}

# Run checks based on options
if [[ "$CHECK_FILES" == true ]]; then
    run_check "Required Files" check_files
fi

if [[ "$CHECK_EXECUTABLES" == true ]]; then
    run_check "WRF-Chem Executables" check_executables
fi

if [[ "$CHECK_CHEMISTRY" == true ]]; then
    run_check "Chemistry Files" check_chemistry
fi

if [[ "$CHECK_NAMELIST" == true ]]; then
    run_check "Namelist Configuration" check_namelist
fi

if [[ "$CHECK_MODULES" == true ]]; then
    run_check "Loaded Modules" check_modules
fi

# Print summary
print_status "Verification Summary"
print_status "==================="
print_status "Total checks: $TOTAL_CHECKS"
print_success "Passed: $PASSED_CHECKS"
if [[ $FAILED_CHECKS -gt 0 ]]; then
    print_error "Failed: $FAILED_CHECKS"
fi
if [[ $WARNING_CHECKS -gt 0 ]]; then
    print_warning "Warnings: $WARNING_CHECKS"
fi

# Overall status
if [[ $FAILED_CHECKS -eq 0 ]]; then
    print_success "✓ All critical checks passed - WRF-Chem is ready to run!"
    exit 0
else
    print_error "✗ Some checks failed - please fix the issues before running WRF-Chem"
    exit 1
fi


























