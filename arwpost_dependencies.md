# ARWpost Dependencies and Prerequisites

## Overview
ARWpost is a post-processing tool for WRF (Weather Research and Forecasting) model output. It converts WRF binary files to formats readable by visualization and analysis tools.

## Required Dependencies

### 1. System Requirements
- **Operating System**: Linux (x86_64 architecture)
- **Memory**: Minimum 2GB RAM (4GB+ recommended)
- **Disk Space**: ~100MB for source code and compiled binary
- **Write Permissions**: Access to installation directory

### 2. Compilers (Required)
Choose one of the following compiler suites:

#### Option A: GNU Compiler Collection (GCC)
- **GCC**: GNU C Compiler (version 4.8+)
- **GFortran**: GNU Fortran Compiler (version 4.8+)
- **G++**: GNU C++ Compiler (version 4.8+)

#### Option B: Intel oneAPI (Recommended for Performance)
- **icc**: Intel C Compiler (version 19.0+)
- **ifort**: Intel Fortran Compiler (version 19.0+)
- **icpc**: Intel C++ Compiler (version 19.0+)

**Note**: Intel compilers often provide better performance optimizations for scientific computing applications.

### 3. Libraries (Required)
- **NetCDF**: Network Common Data Form library
  - Version: 4.x (4.1.3 or later)
  - Purpose: Reading/writing scientific data formats
  - Dependencies: HDF5, zlib, curl

- **HDF5**: Hierarchical Data Format library
  - Version: 1.8+ (1.12.x recommended)
  - Purpose: Data storage and I/O
  - Dependencies: zlib

- **zlib**: Compression library
  - Usually included with system
  - Purpose: Data compression

### 4. Build Tools (Required)
- **make**: Build automation tool
- **wget** or **curl**: Download source code
- **tar**: Extract compressed files
- **pkg-config**: Library configuration

## Optional Dependencies

### 1. MPI (Message Passing Interface)
- **Purpose**: Parallel processing capabilities
- **Versions**: OpenMPI, MPICH, or Intel MPI
- **Use Case**: Processing large datasets in parallel

### 2. OpenMP
- **Purpose**: Shared memory parallelism
- **Use Case**: Multi-threaded processing on single node

## Installation Methods

### Method 1: Using CHPC Modules (Recommended)

#### Option A: GCC Compilers
```bash
# Check available modules
module avail

# Load required modules
module purge
module load chpc/compiler/gcc-9.3.0
module load chpc/netcdf/4.7.4
module load chpc/hdf5/1.12.0

# Optional: Load MPI
module load chpc/mpi/openmpi-4.0.5
```

#### Option B: Intel Compilers (Recommended for Performance)
```bash
# Check available modules
module avail

# Load required modules
module purge
module load chpc/compiler/intel-2021.4.0  # or available Intel version
module load chpc/netcdf/4.7.4
module load chpc/hdf5/1.12.0

# Optional: Load MPI
module load chpc/mpi/openmpi-4.0.5
```

### Method 2: Manual Installation
If modules are not available, you may need to install dependencies manually:

#### Installing NetCDF
```bash
# Download and install NetCDF
wget https://github.com/Unidata/netcdf-c/archive/v4.8.1.tar.gz
tar -xzf v4.8.1.tar.gz
cd netcdf-c-4.8.1
./configure --prefix=/home/apps/chpc/earth/netcdf
make && make install
```

#### Installing HDF5
```bash
# Download and install HDF5
wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.2/src/hdf5-1.12.2.tar.gz
tar -xzf hdf5-1.12.2.tar.gz
cd hdf5-1.12.2
./configure --prefix=/home/apps/chpc/earth/hdf5
make && make install
```

## Environment Variables

Set these environment variables before compiling ARWpost:

### For GCC Compilers
```bash
export NETCDF=/path/to/netcdf
export HDF5=/path/to/hdf5
export FC=gfortran
export CC=gcc
export CXX=g++
export CPPFLAGS="-I$NETCDF/include -I$HDF5/include"
export LDFLAGS="-L$NETCDF/lib -L$HDF5/lib"
export LD_LIBRARY_PATH="$NETCDF/lib:$HDF5/lib:$LD_LIBRARY_PATH"
```

### For Intel Compilers (Recommended)
```bash
export NETCDF=/path/to/netcdf
export HDF5=/path/to/hdf5
export FC=ifort
export CC=icc
export CXX=icpc
export FCFLAGS="-O2 -xHost -ipo"
export CFLAGS="-O2 -xHost -ipo"
export CXXFLAGS="-O2 -xHost -ipo"
export CPPFLAGS="-I$NETCDF/include -I$HDF5/include"
export LDFLAGS="-L$NETCDF/lib -L$HDF5/lib"
export LD_LIBRARY_PATH="$NETCDF/lib:$HDF5/lib:$LD_LIBRARY_PATH"
```

## Verification Commands

### Check Compilers
```bash
gcc --version
gfortran --version
g++ --version
```

### Check Libraries
```bash
# Check NetCDF
pkg-config --exists netcdf && echo "NetCDF found"
nc-config --version

# Check HDF5
pkg-config --exists hdf5 && echo "HDF5 found"
h5cc -showconfig | grep "HDF5 Version"
```

### Check Build Tools
```bash
make --version
wget --version
tar --version
```

## Common Issues and Solutions

### 1. Compiler Not Found
**Problem**: `gfortran: command not found`
**Solution**: Load compiler module or install GNU Fortran

### 2. NetCDF Not Found
**Problem**: `configure: error: netcdf library not found`
**Solution**: 
- Load NetCDF module
- Set NETCDF environment variable
- Install NetCDF manually

### 3. HDF5 Not Found
**Problem**: `configure: error: hdf5 library not found`
**Solution**:
- Load HDF5 module
- Set HDF5 environment variable
- Install HDF5 manually

### 4. Permission Denied
**Problem**: `mkdir: cannot create directory: Permission denied`
**Solution**: 
- Check write permissions
- Contact system administrator
- Use alternative installation directory

## CHPC-Specific Notes

### Available Modules on Lengau
Common module names on CHPC systems:
- `chpc/compiler/gcc-9.3.0`
- `chpc/netcdf/4.7.4`
- `chpc/hdf5/1.12.0`
- `chpc/mpi/openmpi-4.0.5`

### Installation Directory
- **Recommended**: `/home/apps/chpc/earth`
- **Alternative**: `$HOME/arwpost` (if no write access to /home/apps)

### Support
For missing dependencies or installation issues:
- Email: helpdesk@chpc.ac.za
- Check CHPC documentation
- Contact system administrators

## Next Steps

1. Run the dependency checker: `./check_dependencies.sh`
2. Load required modules
3. Set environment variables
4. Proceed with ARWpost installation: `./install_arwpost.sh`
