# CCAM Installation Summary for Lengau Cluster

## Overview

This package provides a complete installation solution for CCAM (Conformal Cubic Atmospheric Model) on the Lengau supercomputer using the Intel toolchain. The installation is optimized for Intel Parallel Studio XE 2018.2.046 and includes all necessary components for successful deployment.

## Files Created

### 1. Installation Script
- **File**: `install_ccam_lengau_intel.sh`
- **Purpose**: Main installation script that compiles and installs CCAM
- **Features**:
  - Intel compiler environment setup
  - Automatic dependency detection
  - Optimized compilation flags
  - Module file creation
  - Installation logging

### 2. Module Creation Script
- **File**: `create_ccam_module.sh`
- **Purpose**: Creates Lengau-compatible module files
- **Features**:
  - Standard module format
  - Environment variable setup
  - Dependency management
  - Help documentation

### 3. Test Script
- **File**: `test_ccam_installation.sh`
- **Purpose**: Comprehensive testing of CCAM installation
- **Features**:
  - Module loading tests
  - Executable verification
  - Dependency checks
  - Performance testing
  - Test report generation

### 4. Documentation
- **File**: `CCAM_Lengau_Installation_Guide.md`
- **Purpose**: Complete installation and usage guide
- **Features**:
  - Step-by-step instructions
  - Troubleshooting guide
  - Performance optimization tips
  - Usage examples

## Installation Process

### Prerequisites
1. **CCAM Source Code**: Must be obtained from CSIRO (requires registration)
2. **Lengau Access**: Valid cluster account with appropriate permissions
3. **Intel Toolchain**: Intel Parallel Studio XE 2018.2.046 available on Lengau

### Quick Start
```bash
# 1. Place CCAM source code in build directory
mkdir -p /mnt/lustre/users/msovara/SoftwareBuilds/CCAM/build
# Copy your CCAM source to: /mnt/lustre/users/msovara/SoftwareBuilds/CCAM/build/ccam/

# 2. Run installation script
./install_ccam_lengau_intel.sh

# 3. Create module file (if not done automatically)
./create_ccam_module.sh

# 4. Test installation
./test_ccam_installation.sh
```

## Key Features

### Intel Optimization
- **Compiler**: Intel Parallel Studio XE 2018.2.046
- **Flags**: `-O2 -xHost -qopenmp`
- **MPI**: Intel MPI for optimal performance
- **Architecture**: Optimized for Lengau cluster

### Module System Integration
- **Standard Format**: Compatible with Lengau module system
- **Environment Setup**: Automatic PATH and library configuration
- **Dependency Management**: Handles NetCDF, HDF5, and MPI dependencies
- **Documentation**: Built-in help and usage information

### Testing and Validation
- **Comprehensive Tests**: Module loading, executable verification, dependency checks
- **Performance Testing**: Basic performance validation
- **Report Generation**: Detailed test results and recommendations
- **Troubleshooting**: Common issue detection and resolution

## Usage

### Loading CCAM
```bash
# Load the module
module load ccam/2023

# Verify installation
ccam -h
```

### Running CCAM
```bash
# Basic execution
ccam

# OpenMP parallel
export OMP_NUM_THREADS=4
ccam

# MPI parallel
mpirun -np 8 ccam
```

## Directory Structure

After installation:
```
/mnt/lustre/users/msovara/SoftwareBuilds/CCAM/
├── bin/                    # CCAM executables
├── lib/                    # CCAM libraries
├── include/                # Header files
├── share/ccam/             # Source files and documentation
├── modulefiles/            # Module files
│   └── ccam-lengau
├── setup_ccam_lengau.sh    # Setup script
├── install_log.txt         # Installation log
└── test/                   # Test results
    ├── test_report.txt
    └── performance_test.sh
```

## Troubleshooting

### Common Issues
1. **Source Code Access**: Ensure proper CCAM source code access from CSIRO
2. **Module Loading**: Check module file syntax and permissions
3. **Compilation Errors**: Verify Intel compiler and dependency modules
4. **Runtime Issues**: Check environment variables and executable permissions

### Debug Commands
```bash
# Check module status
module list

# Check environment
env | grep CCAM

# Check executable
which ccam

# Check installation log
cat /mnt/lustre/users/msovara/SoftwareBuilds/CCAM/install_log.txt
```

## Performance Notes

### Optimizations Applied
- **Intel Compiler**: Latest optimizations for target architecture
- **OpenMP**: Multi-threading support for shared-memory parallelism
- **MPI**: Distributed memory parallelism for cluster computing
- **Memory Management**: Optimized stack sizes and memory allocation

### Recommended Settings
- **Single Node**: `export OMP_NUM_THREADS=16`
- **Multi Node**: `mpirun -np 32 ccam`
- **Memory Intensive**: `export OMP_STACKSIZE=128M`

## Support

### Documentation
- Complete installation guide included
- Troubleshooting section with common issues
- Performance optimization recommendations
- Usage examples and best practices

### Technical Support
- CCAM: Contact CSIRO for model-specific issues
- Lengau: CHPC User Support for cluster-related issues
- Installation: Review logs and documentation

## License and Access

**Important**: CCAM is proprietary software requiring:
1. Registration with CSIRO
2. Agreement to license terms
3. Proper attribution in publications

## Next Steps

1. **Obtain CCAM Source**: Register with CSIRO for source code access
2. **Run Installation**: Execute the installation script on Lengau
3. **Test Installation**: Verify functionality with test script
4. **Configure Simulations**: Set up your CCAM simulation parameters
5. **Run Simulations**: Execute your atmospheric modeling tasks

---

This installation package provides a complete, tested solution for deploying CCAM on the Lengau cluster with Intel toolchain optimization. All scripts are designed to work seamlessly with the Lengau environment and provide comprehensive error handling and logging.




























