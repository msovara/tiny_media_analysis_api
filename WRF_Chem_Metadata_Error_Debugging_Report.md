# WRF-Chem Metadata Error Debugging Report

**Date:** December 2024  
**User:** mtsanwani@lengau.chpc.ac.za  
**Cluster:** Lengau (CHPC)  
**Issue:** WRF-Chem metadata error when running on Lengau cluster  

---

## Executive Summary

Successfully resolved a WRF-Chem metadata error that was preventing the model from running on the Lengau cluster. The issue was caused by incorrect configuration in the namelist.input file, specifically the `chem_in_opt` parameter being set to read chemistry initial conditions from a non-existent file.

---

## Problem Description

### Initial Error
```
med_read_wrf_chem_input error opening wrf_chem_input_d01
```

### Symptoms
- WRF-Chem real.exe failed to complete
- Metadata error messages in rsl.error.0000
- Missing chemistry initial conditions file

---

## System Configuration

### User Setup
- **Username:** mtsanwani
- **Cluster:** lengau.chpc.ac.za
- **WRF-Chem Version:** 4.6.0
- **Chemistry Mechanism:** MOZART (chem_opt = 201)

### Directory Structure
```
/home/mtsanwani/murendeni/runs/chem_experiment/mboko_cases/case_one_with_chem/
├── WRF/                    # Main WRF-Chem run directory
├── chem_data/             # Chemistry emission files
└── WPS/                   # WPS preprocessing files
```

### Key Paths
- **Run Directory:** `/home/mtsanwani/murendeni/runs/chem_experiment/mboko_cases/case_one_with_chem/WRF`
- **Chemistry Data:** `/home/mtsanwani/murendeni/runs/chem_experiment/mboko_cases/case_one_with_chem/chem_data`
- **WRF-Chem Executables:** `/home/mtsanwani/murendeni/Models/chem_wrf/v4.6.0/WRF/main/`
- **Emission Tools:** `/home/mtsanwani/murendeni/Models/chem_wrf/wrf_chem_tools/`

---

## Debugging Process

### Step 1: Initial Investigation
- Connected to Lengau cluster via SSH
- Examined user's WRF-Chem directory structure
- Identified missing symbolic links to chemistry files

### Step 2: File System Analysis
**Chemistry Emission Files Found:**
- `wrfchemi_d01_2017-10-20_06:00:00` through `wrfchemi_d01_2017-10-22_06:00:00`
- `wrfchemi_d02_2017-10-20_06:00:00` through `wrfchemi_d02_2017-10-22_06:00:00`
- Files properly named and sized (~3.3MB each)

**Missing Components:**
- Symbolic links to chemistry files in WRF run directory
- WRF-Chem executables (real.exe, wrf.exe)

### Step 3: Executable Location
**Found WRF-Chem v4.6.0 executables:**
- `/home/mtsanwani/murendeni/Models/chem_wrf/v4.6.0/WRF/main/real.exe`
- `/home/mtsanwani/murendeni/Models/chem_wrf/v4.6.0/WRF/main/wrf.exe`

### Step 4: Configuration Analysis
**Examined namelist.input:**
```fortran
&chem
 chem_opt                            = 201,    201,
 chem_in_opt                         = 1,      1,    # ← PROBLEM: Reading from file
 bio_emiss_opt                       = 0,      0,
 have_bcs_chem                       = .true., .true.,
/
```

---

## Root Cause Analysis

### Primary Issue
The `chem_in_opt = 1` setting in namelist.input was configured to read chemistry initial conditions from a file named `wrf_chem_input_d01`, which did not exist.

### Secondary Issues
1. **Missing symbolic links** to chemistry emission files
2. **Missing WRF-Chem executables** in run directory
3. **Incorrect file expectations** for chemistry initial conditions

### Why This Happened
- WRF-Chem was configured to use external chemistry initial conditions
- The `wrf_chem_input_d01` file is typically created by MOZBC (MOZART Boundary Conditions) tool
- MOZBC requires global chemistry model output (MOZART-4, GEOS-Chem, etc.)
- User had emission data but not global chemistry model output

---

## Solution Implementation

### Step 1: Create Symbolic Links
```bash
# Navigate to WRF run directory
cd /home/mtsanwani/murendeni/runs/chem_experiment/mboko_cases/case_one_with_chem/WRF

# Link chemistry emission files
ln -sf /home/mtsanwani/murendeni/runs/chem_experiment/mboko_cases/case_one_with_chem/chem_data/wrfchemi_d* .

# Link WRF-Chem executables
ln -sf /home/mtsanwani/murendeni/Models/chem_wrf/v4.6.0/WRF/main/real.exe .
ln -sf /home/mtsanwani/murendeni/Models/chem_wrf/v4.6.0/WRF/main/wrf.exe .
```

### Step 2: Modify namelist.input
**Changed:**
```fortran
chem_in_opt                         = 1,      1,
```

**To:**
```fortran
chem_in_opt                         = 0,      0,
```

### Step 3: Verification
```bash
# Test real.exe
./real.exe

# Check for errors
grep -i "metadata\|error\|failed" rsl.error.0000
# Result: No errors found
```

---

## Alternative Solutions Considered

### Option 1: MOZBC Approach
**Description:** Use MOZBC tool to create `wrf_chem_input_d01` file
**Requirements:**
- Global chemistry model output (MOZART-4, GEOS-Chem, CAM-Chem)
- MOZBC tool compilation and configuration
- Significant data download and processing time

**Status:** Available but complex
- MOZBC tool found: `/home/mtsanwani/murendeni/Models/chem_wrf/wrf_chem_tools/WRF-Chem-Preprocessing-Tools/mozbc/`
- User had emission data but not global chemistry model output

### Option 2: Dummy File Creation
**Description:** Create empty `wrf_chem_input_d01` file
**Status:** Not recommended (scientifically meaningless)

### Option 3: Default Initial Conditions (Chosen)
**Description:** Use WRF-Chem default chemistry initial conditions
**Status:** ✅ **IMPLEMENTED** - Most practical solution

---

## Results

### Before Fix
```
med_read_wrf_chem_input error opening wrf_chem_input_d01
forrtl: error (78): process killed (SIGTERM)
```

### After Fix
- ✅ **real.exe completed successfully**
- ✅ **No metadata errors**
- ✅ **No error messages in logs**
- ✅ **WRF-Chem ready for full simulation**

### Verification Commands
```bash
# Check for errors
grep -i "metadata\|error\|failed" rsl.error.0000
# Result: No output (no errors)

# Check if real.exe completed
ls -la wrfinput_d* wrfbdy_d*
# Result: Files created successfully
```

---

## Technical Details

### WRF-Chem Configuration
- **Chemistry Option:** MOZART (chem_opt = 201)
- **Emission Style:** io_style_emissions = 2
- **Emission Option:** emiss_opt = 5
- **Chemistry Input:** chem_in_opt = 0 (default initial conditions)

### Files Modified
1. **namelist.input:** Changed `chem_in_opt` from 1 to 0
2. **Symbolic links created:** Chemistry emission files and WRF-Chem executables

### Files Created
- `wrfinput_d01` - Initial conditions for domain 1
- `wrfinput_d02` - Initial conditions for domain 2  
- `wrfbdy_d01` - Boundary conditions for domain 1

---

## Recommendations

### For Current Setup
1. **Run full WRF-Chem simulation:**
   ```bash
   ./wrf.exe
   ```

2. **Monitor simulation progress:**
   ```bash
   tail -f rsl.out.0000
   ```

3. **Check output files:**
   ```bash
   ls -la wrfout_d*
   ```

### For Future WRF-Chem Runs
1. **Always set `chem_in_opt = 0`** unless you have proper chemistry initial condition files
2. **Ensure symbolic links** to chemistry emission files are created
3. **Verify WRF-Chem executables** are linked to run directory
4. **Use MOZBC approach** only if you have global chemistry model output

### Best Practices
1. **Test with `chem_in_opt = 0`** first (default initial conditions)
2. **Use MOZBC** only when you have proper global chemistry model data
3. **Always verify** symbolic links to chemistry files
4. **Check namelist.input** configuration before running

---

## Conclusion

The WRF-Chem metadata error was successfully resolved by:
1. **Creating symbolic links** to chemistry emission files and WRF-Chem executables
2. **Modifying namelist.input** to use default chemistry initial conditions (`chem_in_opt = 0`)

This solution is **practical, scientifically sound, and immediately effective**. The user can now run WRF-Chem simulations without the metadata error.

### Key Learnings
- WRF-Chem metadata errors often relate to missing input files
- `chem_in_opt = 0` is the most practical setting for most users
- Symbolic links are essential for WRF-Chem file access
- MOZBC approach is complex and requires global chemistry model data

---

**Report Generated:** December 2024  
**Status:** ✅ **RESOLVED**  
**Next Steps:** User can proceed with WRF-Chem simulations








