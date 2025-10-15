# RLM3D Module User Guide - Lengau Cluster

## Overview

RLM3D (3D Ray Launching Method) is now available as a module on the Lengau cluster. This guide provides instructions for loading and using RLM3D.

## Quick Start

### 1. Load the RLM3D Module

```bash
# Load the RLM3D module
module load chpc/earth/rlm3d/3.3.2
```

### 2. Verify Installation

```bash
# Check if RLM3D is available
which RLM3D_v3.3.2

# Test RLM3D with help
RLM3D_v3.3.2 -h
```

### 3. Check Environment

```bash
# View environment variables
echo $RLM3D_ROOT
echo $RLM3D_VERSION
echo $RLM3D_COMPILER
```

## Module Information

- **Version**: 3.3.2
- **Compiler**: Intel Parallel Studio XE 2020u1
- **Installation**: `/home/apps/chpc/earth/rlm3d/`
- **Dependencies**: Intel compiler and MPI libraries

## Usage Examples

### Basic Usage

```bash
# Load the module
module load chpc/earth/rlm3d/3.3.2

# Run RLM3D with help
RLM3D_v3.3.2 -h

# Run RLM3D with your input files
RLM3D_v3.3.2 [options] [input_files]
```

### Parallel Execution

```bash
# Set OpenMP threads
export OMP_NUM_THREADS=4

# Run with parallel processing
RLM3D_v3.3.2 -np 8 [options]
```

### Job Submission (PBS)

```bash
#!/bin/bash
#PBS -N rlm3d_job
#PBS -l select=1:ncpus=8:mpiprocs=8
#PBS -l walltime=02:00:00
#PBS -q normal

# Load modules
module load chpc/earth/rlm3d/3.3.2

# Set environment
export OMP_NUM_THREADS=4

# Run RLM3D
cd $PBS_O_WORKDIR
RLM3D_v3.3.2 [your_options] [input_files]
```

## Environment Variables

When the module is loaded, the following environment variables are set:

- `RLM3D_ROOT`: Installation directory (`/home/apps/chpc/earth/rlm3d/`)
- `RLM3D_VERSION`: Version number (`3.3.2`)
- `RLM3D_COMPILER`: Compiler used (`intel-2020u1`)
- `OMP_NUM_THREADS`: OpenMP threads (default: 1)
- `OMP_STACKSIZE`: OpenMP stack size (default: 64M)

## Dependencies

The RLM3D module automatically loads:
- `chpc/parallel_studio_xe/2020u1` (Intel compiler and MPI)

## Troubleshooting

### Module Not Found

```bash
# Check if module is available
module avail rlm3d

# If not found, try:
module avail chpc/earth/rlm3d
```

### Permission Denied

```bash
# Check if you can access the executable
ls -la /home/apps/chpc/earth/rlm3d/bin/RLM3D_v3.3.2

# Check module permissions
module show chpc/earth/rlm3d/3.3.2
```

### RLM3D Not Found

```bash
# Check if module is loaded
module list

# Reload the module
module purge
module load chpc/earth/rlm3d/3.3.2
```

## Support

For technical support or questions about RLM3D:

1. **Check module help**: `module help chpc/earth/rlm3d/3.3.2`
2. **View RLM3D help**: `RLM3D_v3.3.2 -h`
3. **Contact**: [Your contact information]

## Version Information

- **RLM3D Version**: 3.3.2
- **Build Date**: Aug 27 2025 09:21:04
- **Compiler**: Intel(R) Fortran Intel(R) 64 Compiler Version 19.1.1.217
- **MPI**: Intel(R) MPI Library 2019 Update 7
- **PETSc**: Version 3.19.6

---

**Last Updated**: September 2024  
**Cluster**: Lengau (CHPC)  
**Module**: chpc/earth/rlm3d/3.3.2

























