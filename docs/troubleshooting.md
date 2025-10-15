# WRF-Chem Troubleshooting Guide

This guide provides solutions for common WRF-Chem issues encountered on HPC clusters.

## 🚨 Common Errors and Solutions

### 1. Metadata Error
**Error Message:**
```
med_read_wrf_chem_input error opening wrf_chem_input_d01
```

**Cause:** `chem_in_opt = 1` in namelist.input but `wrf_chem_input_d01` file doesn't exist.

**Solution:**
```bash
# Quick fix
./scripts/fix_metadata_error.sh

# Manual fix
sed -i 's/chem_in_opt.*=.*1.*,.*1.*,/chem_in_opt = 0, 0,/' namelist.input
```

### 2. Missing Chemistry Files
**Error Message:**
```
Error opening wrfchemi_d01_2017-10-20_06:00:00
```

**Cause:** Chemistry emission files not linked to WRF run directory.

**Solution:**
```bash
# Create symbolic links
ln -sf /path/to/chem_data/wrfchemi_d* .
ln -sf /path/to/chem_data/wrffirechemi_d* .
ln -sf /path/to/chem_data/wrfbiochemi_d* .
```

### 3. Missing Executables
**Error Message:**
```
./real.exe: No such file or directory
```

**Cause:** WRF-Chem executables not linked to run directory.

**Solution:**
```bash
# Link executables
ln -sf /path/to/wrf/main/real.exe .
ln -sf /path/to/wrf/main/wrf.exe .
```

### 4. Module Loading Issues
**Error Message:**
```
module: command not found
```

**Cause:** Module system not available or not loaded.

**Solution:**
```bash
# Check if module system is available
which module

# Load modules manually
export PATH=/apps/compilers/intel/parallel_studio_xe_2018_update2/compilers_and_libraries/linux/bin/intel64:$PATH
export LD_LIBRARY_PATH=/apps/chpc/earth/netcdf-4.1.3-intel2016/lib:$LD_LIBRARY_PATH
```

### 5. NetCDF/HDF5 Library Issues
**Error Message:**
```
NetCDF: NetCDF library not found
```

**Cause:** NetCDF or HDF5 libraries not properly linked.

**Solution:**
```bash
# Check library paths
echo $NETCDF
echo $HDF5

# Set library paths manually
export NETCDF=/apps/chpc/earth/netcdf-4.1.3-intel2016
export HDF5=/apps/chpc/earth/hdf5-1.8.16-intel2016
export LD_LIBRARY_PATH=$NETCDF/lib:$HDF5/lib:$LD_LIBRARY_PATH
```

## 🔧 Diagnostic Commands

### Check WRF-Chem Setup
```bash
# Run verification script
./tests/verify_setup.sh --verbose

# Check specific components
./tests/verify_setup.sh --check-files
./tests/verify_setup.sh --check-executables
./tests/verify_setup.sh --check-chemistry
```

### Check File Permissions
```bash
# Check executable permissions
ls -la *.exe

# Fix permissions if needed
chmod +x real.exe wrf.exe
```

### Check File Sizes
```bash
# Check chemistry file sizes
ls -lh wrfchemi_d*

# Check if files are corrupted
ncdump -h wrfchemi_d01_2017-10-20_06:00:00 | head -10
```

### Check Namelist Configuration
```bash
# Check chemistry options
grep -A 10 "&chem" namelist.input

# Check for common issues
grep -i "chem_in_opt" namelist.input
grep -i "chem_opt" namelist.input
grep -i "have_bcs_chem" namelist.input
```

## 🐛 Debugging Steps

### Step 1: Check Error Logs
```bash
# Check for errors in output
grep -i "error\|failed" rsl.error.0000

# Check for warnings
grep -i "warning" rsl.out.0000

# Check for specific chemistry errors
grep -i "chem\|metadata" rsl.error.0000
```

### Step 2: Verify File Structure
```bash
# Check directory structure
ls -la

# Check symbolic links
ls -la wrfchemi_d* | head -5
ls -la *.exe
```

### Step 3: Test Individual Components
```bash
# Test real.exe only
./real.exe

# Check if real.exe completed
ls -la wrfinput_d* wrfbdy_d*

# Test wrf.exe only (after real.exe succeeds)
./wrf.exe
```

### Step 4: Check Resource Usage
```bash
# Check available memory
free -h

# Check disk space
df -h

# Check CPU usage
top -n 1
```

## 🔍 Advanced Troubleshooting

### Memory Issues
**Symptoms:** Job killed, out of memory errors

**Solutions:**
```bash
# Increase memory in PBS script
#PBS -l mem=128GB

# Reduce domain size
# Edit namelist.input to use smaller domain

# Use fewer cores
#PBS -l nodes=2:ppn=16
```

### Performance Issues
**Symptoms:** Slow execution, high CPU usage

**Solutions:**
```bash
# Optimize MPI settings
export I_MPI_PIN_DOMAIN=omp
export I_MPI_PIN_PROCESSOR_LIST=0-15

# Use appropriate number of cores
# Don't use more cores than available
```

### File System Issues
**Symptoms:** Permission denied, file not found

**Solutions:**
```bash
# Check file permissions
ls -la /path/to/files

# Fix permissions
chmod 755 /path/to/directory
chmod 644 /path/to/files

# Check disk quota
quota -u
```

## 📊 Monitoring and Logging

### Real-time Monitoring
```bash
# Monitor job output
tail -f wrf_chem.out

# Monitor error log
tail -f wrf_chem.err

# Check job status
qstat -u $USER
```

### Log Analysis
```bash
# Count errors
grep -c "error" rsl.error.0000

# Find specific errors
grep -n "metadata" rsl.error.0000

# Check timing information
grep "Timing for" rsl.out.0000
```

## 🛠️ Recovery Procedures

### After Failed Job
```bash
# Clean up failed files
rm -f wrfinput_d* wrfbdy_d* wrfout_d*

# Check what went wrong
grep -i "error\|failed" rsl.error.0000

# Fix the issue and resubmit
qsub wrf_chem_job.pbs
```

### After Successful Job
```bash
# Check output files
ls -la wrfout_d*

# Verify file sizes
du -h wrfout_d*

# Check file contents
ncdump -h wrfout_d01_2017-10-20_06:00:00 | head -20
```

## 📞 Getting Help

### Self-Help Resources
1. **Check this repository's documentation**
2. **Run diagnostic scripts**
3. **Review error logs carefully**
4. **Check WRF-Chem user guide**

### When to Ask for Help
- Error persists after trying solutions
- Unusual error messages not covered here
- Performance issues not resolved
- Need help with specific chemistry mechanisms

### Information to Provide
1. **Error messages** (exact text)
2. **System information** (cluster, modules)
3. **Configuration files** (namelist.input)
4. **Log files** (rsl.error.0000, rsl.out.0000)
5. **Steps already tried**

## ✅ Prevention Checklist

- [ ] Always run verification script before submitting jobs
- [ ] Check file permissions and symbolic links
- [ ] Verify namelist configuration
- [ ] Test with small domain first
- [ ] Monitor resource usage
- [ ] Keep backups of working configurations

## 🎯 Best Practices

1. **Start small:** Test with small domain first
2. **Verify setup:** Always run verification scripts
3. **Monitor logs:** Check output and error logs regularly
4. **Keep backups:** Save working configurations
5. **Document issues:** Keep track of problems and solutions
6. **Update regularly:** Keep WRF-Chem and tools updated

---

**Last Updated:** December 2024  
**Tested on:** Lengau cluster (CHPC)  
**WRF-Chem Version:** 4.6.0


























