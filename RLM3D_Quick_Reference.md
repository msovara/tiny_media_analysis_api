# RLM3D Quick Reference - Lengau Cluster

## 🚀 Quick Start

```bash
# Load RLM3D module
module load chpc/earth/rlm3d/3.3.2

# Test RLM3D
RLM3D_v3.3.2 -h
```

## 📋 Essential Commands

| Command | Description |
|---------|-------------|
| `module load chpc/earth/rlm3d/3.3.2` | Load RLM3D module |
| `module unload chpc/earth/rlm3d/3.3.2` | Unload RLM3D module |
| `which RLM3D_v3.3.2` | Check if RLM3D is available |
| `RLM3D_v3.3.2 -h` | Show RLM3D help |
| `echo $RLM3D_ROOT` | Show installation directory |

## 🔧 Environment Variables

- `RLM3D_ROOT`: `/home/apps/chpc/earth/rlm3d/`
- `RLM3D_VERSION`: `3.3.2`
- `RLM3D_COMPILER`: `intel-2020u1`
- `OMP_NUM_THREADS`: `1` (default)

## ⚡ Parallel Execution

```bash
# Set OpenMP threads
export OMP_NUM_THREADS=4

# Run with parallel processing
RLM3D_v3.3.2 -np 8 [options]
```

## 📝 PBS Job Example

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

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Module not found | `module avail rlm3d` |
| Permission denied | Check file permissions |
| RLM3D not found | `module list` to check if loaded |
| Tcl errors | Reload module: `module purge && module load chpc/earth/rlm3d/3.3.2` |

## 📞 Support

- **Module Help**: `module help chpc/earth/rlm3d/3.3.2`
- **RLM3D Help**: `RLM3D_v3.3.2 -h`
- **Version Info**: `echo $RLM3D_VERSION`

---

**Version**: 3.3.2 | **Cluster**: Lengau | **Compiler**: Intel 2020u1

























