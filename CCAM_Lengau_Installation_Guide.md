# CCAM Installation Guide for Lengau Cluster

This guide provides step-by-step instructions for installing CCAM (Conformal Cubic Atmospheric Model) on the Lengau supercomputer using the Intel toolchain.

## Overview

CCAM is a high-resolution atmospheric model developed by CSIRO (Commonwealth Scientific and Industrial Research Organisation) that uses a conformal cubic grid for global atmospheric modeling. This installation is optimized for the Lengau cluster using Intel Parallel Studio XE 2018.2.046.

## Prerequisites

### Access Requirements
- Valid Lengau cluster account
- Access to CCAM source code (requires registration with CSIRO)
- Intel Parallel Studio XE 2018.2.046 module available on Lengau

### Dependencies
- Intel Fortran Compiler (ifort)
- Intel C Compiler (icc)
- Intel C++ Compiler (icpc)
- Intel MPI
- NetCDF library
- HDF5 library

## Installation Steps

### 1. Download and Prepare Source Code

**Important**: CCAM source code requires registration with CSIRO. You must obtain the source code through official channels before proceeding.

```bash
# Create installation directory
mkdir -p /mnt/lustre/users/msovara/SoftwareBuilds/CCAM
cd /mnt/lustre/users/msovara/SoftwareBuilds/CCAM

# Place your CCAM source code in the build directory
# The source should be in: /mnt/lustre/users/msovara/SoftwareBuilds/CCAM/build/ccam/
```

### 2. Run the Installation Script

```bash
# Make the installation script executable
chmod +x install_ccam_lengau_intel.sh

# Run the installation
./install_ccam_lengau_intel.sh
```

The installation script will:
- Load Intel Parallel Studio XE 2018.2.046
- Configure Intel MPI environment
- Load compatible NetCDF and HDF5 modules
- Set up Intel compiler environment variables
- Compile CCAM with Intel optimizations
- Create module files for easy loading
- Generate installation logs

### 3. Create Module File (Alternative Method)

If you prefer to create the module file separately:

```bash
# Make the module creation script executable
chmod +x create_ccam_module.sh

# Run the module creation script
./create_ccam_module.sh
```

### 4. Test the Installation

```bash
# Make the test script executable
chmod +x test_ccam_installation.sh

# Run the installation test
./test_ccam_installation.sh
```

## Usage

### Loading CCAM Module

```bash
# Load the CCAM module
module load ccam/2023

# Or load from installation directory
module load /mnt/lustre/users/msovara/SoftwareBuilds/CCAM/modulefiles/ccam-lengau
```

### Running CCAM

```bash
# Basic execution
ccam

# With help
ccam -h

# Parallel execution with OpenMP
export OMP_NUM_THREADS=4
ccam

# MPI parallel execution
mpirun -np 8 ccam
```

### Environment Setup

The module automatically sets up:
- `CCAM_ROOT`: Installation directory
- `CCAM_VERSION`: Version information
- `CCAM_COMPILER`: Compiler information
- `PATH`: Includes CCAM binaries
- `LD_LIBRARY_PATH`: Includes CCAM libraries

## Configuration

### Compiler Optimizations

The installation uses Intel-specific optimizations:
- `-O2`: Standard optimization level
- `-xHost`: Optimize for the target architecture
- `-qopenmp`: Enable OpenMP support

### OpenMP Configuration

```bash
# Set number of OpenMP threads
export OMP_NUM_THREADS=4

# Set OpenMP stack size
export OMP_STACKSIZE=64M
```

### MPI Configuration

```bash
# For MPI parallel execution
mpirun -np 8 ccam
```

## File Structure

After installation, the following structure is created:

```
/mnt/lustre/users/msovara/SoftwareBuilds/CCAM/
├── bin/                    # CCAM executables
├── lib/                    # CCAM libraries
├── include/                # Header files
├── share/ccam/             # Source files and documentation
├── modulefiles/            # Module files
│   └── ccam-lengau
├── setup_ccam_lengau.sh    # Setup script
└── install_log.txt         # Installation log
```

## Troubleshooting

### Common Issues

1. **Source Code Access**
   - Ensure you have proper access to CCAM source code
   - Contact CSIRO for source code access if needed

2. **Module Loading Issues**
   - Check if module file exists: `ls /mnt/lustre/users/msovara/SoftwareBuilds/CCAM/modulefiles/`
   - Verify module syntax: `module show ccam/2023`

3. **Compilation Errors**
   - Check Intel compiler availability: `module avail intel`
   - Verify NetCDF/HDF5 modules: `module avail netcdf`
   - Review compilation logs in installation directory

4. **Runtime Issues**
   - Check environment variables: `env | grep CCAM`
   - Verify executable permissions: `ls -la /mnt/lustre/users/msovara/SoftwareBuilds/CCAM/bin/`

### Debugging Commands

```bash
# Check module status
module list

# Check environment variables
env | grep CCAM

# Check executable
which ccam

# Check libraries
ldd $(which ccam)

# Check compilation log
cat /mnt/lustre/users/msovara/SoftwareBuilds/CCAM/install_log.txt
```

## Performance Optimization

### Intel-Specific Optimizations

The installation includes several Intel-specific optimizations:

1. **Compiler Flags**
   - `-O2`: Balanced optimization
   - `-xHost`: Architecture-specific optimization
   - `-qopenmp`: OpenMP support

2. **MPI Configuration**
   - Intel MPI for optimal performance
   - Optimized for Lengau cluster architecture

3. **Memory Management**
   - OpenMP stack size optimization
   - Efficient memory allocation

### Recommended Settings

```bash
# For single-node execution
export OMP_NUM_THREADS=16

# For multi-node execution
mpirun -np 32 ccam

# For memory-intensive runs
export OMP_STACKSIZE=128M
```

## Support and Documentation

### CCAM Documentation
- CSIRO CCAM User Guide
- CCAM Technical Documentation
- CCAM Community Forums

### Lengau Cluster Support
- CHPC User Support
- Lengau Documentation
- Cluster-specific optimizations

### Installation Support
- Review installation logs
- Check module files
- Verify environment setup

## Version Information

- **CCAM Version**: 2023
- **Compiler**: Intel Parallel Studio XE 2018.2.046
- **MPI**: Intel MPI
- **NetCDF**: Compatible with CHPC modules
- **HDF5**: Compatible with CHPC modules

## License and Access

CCAM is proprietary software developed by CSIRO. Access to the source code requires:
1. Registration with CSIRO
2. Agreement to license terms
3. Proper attribution in publications

## Contact Information

For technical support:
- CCAM: Contact CSIRO directly
- Lengau Cluster: CHPC User Support
- Installation Issues: Review this guide and installation logs

---

**Note**: This installation guide is specifically tailored for the Lengau cluster using Intel toolchain. For other systems or compilers, modifications may be required.




























