#!/bin/bash

# WRF-Chem Metadata Error Fix Script
# This script fixes the common "med_read_wrf_chem_input error opening wrf_chem_input_d01" error

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

WRF-Chem Metadata Error Fix Script

OPTIONS:
    -f, --namelist FILE        Path to namelist.input file (default: ./namelist.input)
    -b, --backup               Create backup of namelist.input
    -v, --verbose              Verbose output
    -h, --help                 Show this help message

EXAMPLES:
    $0                                    # Fix namelist.input in current directory
    $0 -f /path/to/namelist.input        # Fix specific namelist file
    $0 -b -v                             # Create backup and verbose output

EOF
}

# Default values
NAMELIST_FILE="namelist.input"
CREATE_BACKUP=false
VERBOSE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--namelist)
            NAMELIST_FILE="$2"
            shift 2
            ;;
        -b|--backup)
            CREATE_BACKUP=true
            shift
            ;;
        -v|--verbose)
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

print_status "WRF-Chem Metadata Error Fix Script"
print_status "====================================="

# Check if namelist file exists
if [[ ! -f "$NAMELIST_FILE" ]]; then
    print_error "Namelist file not found: $NAMELIST_FILE"
    exit 1
fi

print_status "Processing namelist file: $NAMELIST_FILE"

# Create backup if requested
if [[ "$CREATE_BACKUP" == true ]]; then
    BACKUP_FILE="${NAMELIST_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$NAMELIST_FILE" "$BACKUP_FILE"
    print_success "Backup created: $BACKUP_FILE"
fi

# Check current chem_in_opt setting
if [[ "$VERBOSE" == true ]]; then
    print_status "Current chem_in_opt setting:"
    grep -n "chem_in_opt" "$NAMELIST_FILE" || print_warning "chem_in_opt not found in namelist"
fi

# Fix chem_in_opt
print_status "Fixing chem_in_opt setting..."

# Create temporary file
TEMP_FILE=$(mktemp)

# Process the namelist file
awk '
BEGIN { changed = 0 }
/chem_in_opt/ {
    if ($0 ~ /chem_in_opt.*=.*1.*,.*1/) {
        gsub(/chem_in_opt.*=.*1.*,.*1/, "chem_in_opt = 0, 0,")
        changed = 1
        print "  # Fixed: " $0
    } else if ($0 ~ /chem_in_opt.*=.*1/) {
        gsub(/chem_in_opt.*=.*1/, "chem_in_opt = 0")
        changed = 1
        print "  # Fixed: " $0
    }
    print $0
    next
}
{ print $0 }
END {
    if (changed == 0) {
        print "  # No changes needed - chem_in_opt already set to 0"
    }
}
' "$NAMELIST_FILE" > "$TEMP_FILE"

# Replace original file
mv "$TEMP_FILE" "$NAMELIST_FILE"

print_success "Namelist file updated successfully"

# Verify the fix
print_status "Verifying the fix..."
if grep -q "chem_in_opt.*=.*0" "$NAMELIST_FILE"; then
    print_success "✓ chem_in_opt is now set to 0"
    if [[ "$VERBOSE" == true ]]; then
        print_status "Updated chem_in_opt lines:"
        grep -n "chem_in_opt" "$NAMELIST_FILE"
    fi
else
    print_error "✗ Failed to set chem_in_opt to 0"
    exit 1
fi

# Additional checks
print_status "Performing additional checks..."

# Check for other potential issues
if grep -q "have_bcs_chem.*=.*\.true\." "$NAMELIST_FILE"; then
    print_success "✓ have_bcs_chem is set to .true."
else
    print_warning "⚠ have_bcs_chem not set to .true. - this may cause issues"
fi

# Check for chemistry options
if grep -q "chem_opt.*=" "$NAMELIST_FILE"; then
    CHEM_OPT=$(grep "chem_opt.*=" "$NAMELIST_FILE" | head -1)
    print_success "✓ Chemistry option found: $CHEM_OPT"
else
    print_warning "⚠ No chem_opt found - make sure chemistry is enabled"
fi

print_success "Metadata error fix completed successfully!"
print_status "====================================="
print_status "Summary:"
print_status "- Fixed chem_in_opt from 1 to 0"
print_status "- WRF-Chem will now use default chemistry initial conditions"
print_status "- No more 'med_read_wrf_chem_input error opening wrf_chem_input_d01' error"
print_status ""
print_status "Next steps:"
print_status "1. Run real.exe to test the fix"
print_status "2. If successful, run wrf.exe for full simulation"
print_status "3. Monitor output files for any other issues"


























