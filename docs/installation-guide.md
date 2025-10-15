# WRF-Chem Installation Guide

This guide provides step-by-step instructions for setting up WRF-Chem on HPC clusters, specifically tested on the Lengau cluster at CHPC.

## 📋 Prerequisites

### System Requirements
- Access to HPC cluster (tested on Lengau/CHPC)
- Intel compilers (Intel Parallel Studio XE)
- NetCDF and HDF5 libraries
- Sufficient storage space (at least 50GB for WRF-Chem)
- Chemistry emission data

### Required Modules
```bash
module load chpc/parallel_studio_xe/16.0.1/2016.1.150
module load chpc/netcdf/4.4.3-F/intel/16.0.1
module load chpc/hdf5/1.8.16/intel/16.0.1
```

## 🚀 Quick Installation

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd wrf-chem-metadata-debugging
```

### Step 2: Run Setup Script
```bash
chmod +x scripts/setup_wrf_chem.sh
./scripts/setup_wrf_chem.sh -d /path/to/wrf -c /path/to/chem -e /path/to/exec
```

### Step 3: Verify Installation
```bash
./tests/verify_setup.sh
```

## 📁 Directory Structure Setup

### Recommended Structure
```
/home/username/wrf_chem_simulation/
├── WRF/                    # Main WRF-Chem run directory
├── WPS/                    # WPS preprocessing directory
├── chem_data/             # Chemistry emission files
├── wrf_chem_tools/        # WRF-Chem preprocessing tools
└── output/                # Simulation output files
```

### Create Directories
```bash
mkdir -p /home/username/wrf_chem_simulation/{WRF,WPS,chem_data,output}
```

## 🔧 WRF-Chem Compilation

### Step 1: Download WRF-Chem Source
```bash
# Download WRF-Chem source code
wget https://github.com/wrf-model/WRF/archive/v4.6.0.tar.gz
tar -xzf v4.6.0.tar.gz
cd WRF-4.6.0
```

### Step 2: Configure WRF-Chem
```bash
# Load required modules
module purge
module load chpc/parallel_studio_xe/16.0.1/2016.1.150
module load chpc/netcdf/4.4.3-F/intel/16.0.1
module load chpc/hdf5/1.8.16/intel/16.0.1

# Configure WRF-Chem
./configure
# Select: 15. (dmpar) INTEL (ifort/icc)
# Select: 1. Basic nesting
```

### Step 3: Compile WRF-Chem
```bash
# Compile WRF-Chem
./compile -j 8 em_real 2>&1 | tee compile.log

# Check for successful compilation
ls -la main/real.exe main/wrf.exe
```

## 📊 Chemistry Data Preparation

### Emission Data Sources
1. **EDGAR-HTAP**: Global anthropogenic emissions
2. **MEGAN**: Biogenic emissions
3. **FINN**: Fire emissions
4. **Custom**: User-specific emission data

### Preprocessing Tools
```bash
# Navigate to WRF-Chem tools
cd /path/to/wrf_chem_tools/

# ANTHRO - Anthropogenic emissions
cd ANTHRO/src
make clean
make

# MEGAN - Biogenic emissions
cd ../megan_bio_emiss
make clean
make
```

### Generate Chemistry Files
```bash
# Generate anthropogenic emissions
./anthro_emis < anthro_emis.inp

# Generate biogenic emissions
./megan_bio_emiss < megan_bio_emiss.inp
```

## ⚙️ Configuration

### Namelist.input Setup
```fortran
&chem
 chem_opt                            = 201,    201,
 chem_in_opt                         = 0,      0,    # Use default initial conditions
 bio_emiss_opt                       = 1,      1,
 dust_opt                            = 1,      1,
 dmsemis_opt                         = 1,      1,
 biomass_burn_opt                    = 1,      1,
 plumerisefire_frq                   = 0,      0,
 aer_ra_feedback                     = 1,      1,
 opt_pars_out                        = 1,      1,
 have_bcs_chem                       = .true., .true.,
 have_bcs_tracer                     = .true., .true.,
/
```

### Domain Configuration
```fortran
&domains
 time_step                           = 180,
 max_dom                             = 2,
 e_we                                = 74,     148,
 e_sn                                = 61,     121,
 e_vert                              = 28,     28,
 dx                                  = 30000,  15000,
 dy                                  = 30000,  15000,
/
```

## 🧪 Testing Installation

### Test 1: Basic Setup
```bash
cd /path/to/wrf/run/directory
./tests/verify_setup.sh --check-files --check-executables
```

### Test 2: Chemistry Configuration
```bash
./tests/verify_setup.sh --check-chemistry --check-namelist
```

### Test 3: Full Verification
```bash
./tests/verify_setup.sh --verbose
```

## 🚀 Running WRF-Chem

### Step 1: Prepare Input Data
```bash
# Link chemistry files
ln -sf /path/to/chem_data/wrfchemi_d* .
ln -sf /path/to/chem_data/wrffirechemi_d* .
ln -sf /path/to/chem_data/wrfbiochemi_d* .

# Link WRF-Chem executables
ln -sf /path/to/wrf/main/real.exe .
ln -sf /path/to/wrf/main/wrf.exe .
```

### Step 2: Fix Metadata Error
```bash
./scripts/fix_metadata_error.sh
```

### Step 3: Submit Job
```bash
qsub wrf_chem_job.pbs
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Compilation Errors
```bash
# Check compiler version
ifort --version
icc --version

# Check module loading
module list

# Clean and recompile
make clean
./compile -j 8 em_real
```

#### 2. Missing Libraries
```bash
# Check NetCDF
ncdump -h /path/to/netcdf/lib/libnetcdf.so

# Check HDF5
h5dump -H /path/to/hdf5/lib/libhdf5.so
```

#### 3. Chemistry Data Issues
```bash
# Check file naming
ls -la wrfchemi_d*

# Check file format
ncdump -h wrfchemi_d01_2017-10-20_06:00:00
```

### Debug Commands
```bash
# Check WRF-Chem configuration
grep -A 10 "&chem" namelist.input

# Check for errors
grep -i "error\|failed" rsl.error.0000

# Check file permissions
ls -la *.exe
```

## 📚 Additional Resources

### Documentation
- [WRF-Chem User Guide](https://www2.acom.ucar.edu/wrf-chem)
- [WRF-Chem Tutorial](https://www2.acom.ucar.edu/wrf-chem/tutorial)
- [Chemistry Mechanisms](https://www2.acom.ucar.edu/wrf-chem/mechanisms)

### Support
- WRF-Chem Community Forum
- CHPC Support (for Lengau cluster)
- This repository's issue tracker

## ✅ Verification Checklist

- [ ] WRF-Chem compiled successfully
- [ ] Required modules loaded
- [ ] Chemistry data prepared
- [ ] Namelist configured correctly
- [ ] Symbolic links created
- [ ] Metadata error fixed
- [ ] Test run completed successfully

## 🎯 Next Steps

1. **Run test simulation** with small domain
2. **Validate results** against observations
3. **Scale up** to production simulation
4. **Monitor performance** and optimize
5. **Archive results** for analysis

---

**Last Updated:** December 2024  
**Tested on:** Lengau cluster (CHPC)  
**WRF-Chem Version:** 4.6.0


























