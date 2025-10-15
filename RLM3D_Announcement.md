# 🎉 RLM3D Now Available on Lengau Cluster!

## What is RLM3D?

RLM3D (3D Ray Launching Method) is a powerful electromagnetic propagation simulation tool for complex 3D geometries. It's now available as a module on the Lengau cluster!

## 🚀 How to Use

### Quick Start
```bash
# Load the module
module load chpc/earth/rlm3d/3.3.2

# Test it works
RLM3D_v3.3.2 -h
```

### Key Features
- ✅ 3D Ray Launching Method for electromagnetic propagation
- ✅ High-frequency electromagnetic field calculations
- ✅ Complex 3D geometry support
- ✅ Parallel processing capabilities
- ✅ Intel compiler optimization

## 📋 Module Details

- **Version**: 3.3.2
- **Compiler**: Intel Parallel Studio XE 2020u1
- **Installation**: `/home/apps/chpc/earth/rlm3d/`
- **Dependencies**: Automatically loads Intel compiler and MPI

## 🔧 Usage Examples

### Basic Usage
```bash
module load chpc/earth/rlm3d/3.3.2
RLM3D_v3.3.2 [options] [input_files]
```

### Parallel Execution
```bash
export OMP_NUM_THREADS=4
RLM3D_v3.3.2 -np 8 [options]
```

### PBS Job
```bash
#!/bin/bash
#PBS -N rlm3d_job
#PBS -l select=1:ncpus=8:mpiprocs=8
#PBS -l walltime=02:00:00
#PBS -q normal

module load chpc/earth/rlm3d/3.3.2
export OMP_NUM_THREADS=4
cd $PBS_O_WORKDIR
RLM3D_v3.3.2 [your_options] [input_files]
```

## 🆘 Need Help?

- **Module Help**: `module help chpc/earth/rlm3d/3.3.2`
- **RLM3D Help**: `RLM3D_v3.3.2 -h`
- **Check Installation**: `echo $RLM3D_ROOT`

## 📚 Documentation

- **User Guide**: Available in project documentation
- **Quick Reference**: See RLM3D_Quick_Reference.md
- **Version Info**: RLM3D v3.3.2 with Intel compiler

---

**Available Now**: All users can access RLM3D by loading the module!  
**Contact**: [Your contact information] for support

























