#!/usr/bin/env python3
"""
WRF Service for Lengau Cluster
Handles WRF-specific job submissions and management
"""

import os
import subprocess
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
import shutil

logger = logging.getLogger(__name__)

class WRFService:
    """Service for managing WRF jobs on Lengau cluster"""
    
    def __init__(self):
        self.wrf_base_path = "/apps/chpc/earth/WRF-4.1.1-impi"
        self.default_modules = [
            "chpc/parallel_studio_xe/16.0.1/2016.1.150",
            "chpc/netcdf/4.4.3-F/intel/16.0.1",
            "chpc/hdf5/1.8.16/intel/16.0.1"
        ]
        self.wrf_exe_path = f"{self.wrf_base_path}/main"
        self.wps_exe_path = f"{self.wrf_base_path}/WPS"
        
    def _run_command(self, command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        """Run a shell command and return results"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=30
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Command timed out",
                "returncode": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    def get_wrf_info(self) -> Dict[str, Any]:
        """Get WRF installation information"""
        info = {
            "wrf_version": "4.1.1",
            "wrf_base_path": self.wrf_base_path,
            "wrf_exe_path": self.wrf_exe_path,
            "wps_exe_path": self.wps_exe_path,
            "default_modules": self.default_modules,
            "available_executables": []
        }
        
        # Check available WRF executables
        if os.path.exists(self.wrf_exe_path):
            try:
                executables = os.listdir(self.wrf_exe_path)
                info["available_executables"] = [exe for exe in executables if exe.endswith('.exe')]
            except Exception as e:
                logger.error(f"Error listing WRF executables: {e}")
        
        # Check WPS executables
        if os.path.exists(self.wps_exe_path):
            try:
                wps_executables = os.listdir(self.wps_exe_path)
                info["wps_executables"] = [exe for exe in wps_executables if exe.endswith('.exe')]
            except Exception as e:
                logger.error(f"Error listing WPS executables: {e}")
        
        return info
    
    def create_wrf_namelist(self, config: Dict[str, Any]) -> str:
        """Create WRF namelist.input content"""
        namelist_template = f"""&time_control
 run_days                            = {config.get('run_days', 0)},
 run_hours                           = {config.get('run_hours', 24)},
 run_minutes                         = {config.get('run_minutes', 0)},
 run_seconds                         = {config.get('run_seconds', 0)},
 start_year                          = {config.get('start_year', 2023)},
 start_month                         = {config.get('start_month', 1)},
 start_day                           = {config.get('start_day', 1)},
 start_hour                          = {config.get('start_hour', 0)},
 start_minute                        = {config.get('start_minute', 0)},
 start_second                        = {config.get('start_second', 0)},
 end_year                            = {config.get('end_year', 2023)},
 end_month                           = {config.get('end_month', 1)},
 end_day                             = {config.get('end_day', 2)},
 end_hour                            = {config.get('end_hour', 0)},
 end_minute                          = {config.get('end_minute', 0)},
 end_second                          = {config.get('end_second', 0)},
 interval_seconds                    = {config.get('interval_seconds', 21600)},
 input_from_file                     = .true.,
 history_interval                    = {config.get('history_interval', 180)},
 frames_per_outfile                  = {config.get('frames_per_outfile', 1000)},
 restart                             = .false.,
 restart_interval                    = {config.get('restart_interval', 5000)},
 io_form_history                     = 2,
 io_form_restart                     = 2,
 io_form_input                       = 2,
 io_form_boundary                    = 2,
 debug_level                         = 0,
/

&domains
 time_step                           = {config.get('time_step', 180)},
 time_step_fract_num                 = 0,
 time_step_fract_den                 = 1,
 max_dom                             = {config.get('max_dom', 1)},
 e_we                                = {config.get('e_we', [74])},
 e_sn                                = {config.get('e_sn', [61])},
 e_vert                              = {config.get('e_vert', [28])},
 p_top_requested                     = {config.get('p_top_requested', 5000)},
 num_metgrid_levels                  = {config.get('num_metgrid_levels', 27)},
 num_metgrid_soil_levels             = {config.get('num_metgrid_soil_levels', 4)},
 dx                                  = {config.get('dx', [30000])},
 dy                                  = {config.get('dy', [30000])},
 grid_id                             = {config.get('grid_id', [1])},
 parent_id                           = {config.get('parent_id', [1])},
 i_parent_start                      = {config.get('i_parent_start', [1])},
 j_parent_start                      = {config.get('j_parent_start', [1])},
 parent_grid_ratio                   = {config.get('parent_grid_ratio', [1])},
 parent_time_step_ratio              = {config.get('parent_time_step_ratio', [1])},
 feedback                            = 1,
 smooth_option                       = 0,
/

&physics
 mp_physics                          = {config.get('mp_physics', [3])},
 ra_lw_physics                       = {config.get('ra_lw_physics', [1])},
 ra_sw_physics                       = {config.get('ra_sw_physics', [1])},
 radt                                = {config.get('radt', [30])},
 sf_sfclay_physics                   = {config.get('sf_sfclay_physics', [1])},
 sf_surface_physics                  = {config.get('sf_surface_physics', [1])},
 bl_pbl_physics                      = {config.get('bl_pbl_physics', [1])},
 bldt                                = {config.get('bldt', [0])},
 cu_physics                          = {config.get('cu_physics', [1])},
 cudt                                = {config.get('cudt', [5])},
 isfflx                              = {config.get('isfflx', 1)},
 ifsnow                              = {config.get('ifsnow', 0)},
 icloud                              = {config.get('icloud', 1)},
 surface_input_source                = {config.get('surface_input_source', 1)},
 num_soil_layers                     = {config.get('num_soil_layers', 4)},
 sf_urban_physics                    = {config.get('sf_urban_physics', 0)},
/

&fdda
/

&dynamics
 w_damping                           = {config.get('w_damping', 0)},
 diff_opt                            = {config.get('diff_opt', [1])},
 km_opt                              = {config.get('km_opt', [4])},
 diff_6th_opt                        = {config.get('diff_6th_opt', 0)},
 diff_6th_factor                     = {config.get('diff_6th_factor', 0.12)},
 base_temp                           = {config.get('base_temp', 290.)},
 damp_opt                            = {config.get('damp_opt', 0)},
 zdamp                               = {config.get('zdamp', 5000.)},
 dampcoef                            = {config.get('dampcoef', 0.2)},
 khdif                               = {config.get('khdif', 0)},
 kvdif                               = {config.get('kvdif', 0)},
 non_hydrostatic                     = {config.get('non_hydrostatic', '.true.')},
 moist_adv_opt                       = {config.get('moist_adv_opt', [1])},
 scalar_adv_opt                      = {config.get('scalar_adv_opt', [1])},
/

&bdy_control
 spec_bdy_width                      = {config.get('spec_bdy_width', 5)},
 spec_zone                           = {config.get('spec_zone', 1)},
 relax_zone                          = {config.get('relax_zone', 4)},
 specified                           = {config.get('specified', '.true.')},
 nested                              = {config.get('nested', '.false.')},
/

&grib2
/

&namelist_quilt
 nio_tasks_per_group = 0,
 nio_groups = 1,
/
"""
        return namelist_template
    
    def create_wps_namelist(self, config: Dict[str, Any]) -> str:
        """Create WPS namelist.wps content"""
        namelist_template = f"""&share
 wrf_core = 'ARW',
 max_dom = {config.get('max_dom', 1)},
 start_date = '{config.get('start_date', '2023-01-01_00:00:00')}',
 end_date   = '{config.get('end_date', '2023-01-02_00:00:00')}',
 interval_seconds = {config.get('interval_seconds', 21600)},
 io_form_geogrid = 2,
/

&geogrid
 parent_id         = {config.get('parent_id', [1])},
 parent_grid_ratio = {config.get('parent_grid_ratio', [1])},
 i_parent_start    = {config.get('i_parent_start', [1])},
 j_parent_start    = {config.get('j_parent_start', [1])},
 e_we              = {config.get('e_we', [74])},
 e_sn              = {config.get('e_sn', [61])},
 geog_data_res     = '{config.get('geog_data_res', 'default')}',
 dx = {config.get('dx', [30000])},
 dy = {config.get('dy', [30000])},
 map_proj = '{config.get('map_proj', 'lambert')}',
 ref_lat   = {config.get('ref_lat', -34.0)},
 ref_lon   = {config.get('ref_lon', 18.5)},
 truelat1  = {config.get('truelat1', -34.0)},
 truelat2  = {config.get('truelat2', -34.0)},
 stand_lon = {config.get('stand_lon', 18.5)},
 geog_data_path = '{config.get('geog_data_path', '/apps/chpc/earth/WPS_GEOG')}',
/

&ungrib
 out_format = 'WPS',
 prefix = '{config.get('prefix', 'FILE')}',
/

&metgrid
 fg_name = '{config.get('fg_name', 'FILE')}',
 io_form_metgrid = 2,
/
"""
        return namelist_template
    
    def submit_wrf_job(self, job_config: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a WRF job with the given configuration"""
        try:
            # Create job directory
            job_name = job_config.get('job_name', 'wrf_simulation')
            job_dir = f"~/wrf_jobs/{job_name}"
            os.makedirs(job_dir, exist_ok=True)
            
            # Create WRF namelist
            wrf_namelist = self.create_wrf_namelist(job_config.get('wrf_config', {}))
            with open(f"{job_dir}/namelist.input", 'w') as f:
                f.write(wrf_namelist)
            
            # Create WPS namelist if needed
            if job_config.get('run_wps', False):
                wps_namelist = self.create_wps_namelist(job_config.get('wps_config', {}))
                with open(f"{job_dir}/namelist.wps", 'w') as f:
                    f.write(wps_namelist)
            
            # Create job script
            job_script = self._create_wrf_job_script(job_config, job_dir)
            
            # Submit job
            result = self._submit_job_script(job_script, job_name)
            
            return {
                "success": True,
                "job_id": result.get("job_id"),
                "job_dir": job_dir,
                "message": f"WRF job '{job_name}' submitted successfully"
            }
            
        except Exception as e:
            logger.error(f"Error submitting WRF job: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_wrf_job_script(self, job_config: Dict[str, Any], job_dir: str) -> str:
        """Create PBS job script for WRF"""
        job_name = job_config.get('job_name', 'wrf_simulation')
        queue = job_config.get('queue', 'normal')
        nodes = job_config.get('nodes', 2)
        cores_per_node = job_config.get('cores_per_node', 16)
        memory_per_node = job_config.get('memory_per_node', '64GB')
        walltime = job_config.get('walltime', '24:00:00')
        run_wps = job_config.get('run_wps', False)
        
        script = f"""#!/bin/bash
#PBS -N {job_name}
#PBS -q {queue}
#PBS -l nodes={nodes}:ppn={cores_per_node}
#PBS -l mem={memory_per_node}
#PBS -l walltime={walltime}
#PBS -o {job_dir}/wrf.out
#PBS -e {job_dir}/wrf.err

cd {job_dir}

# Load required modules
module load chpc/parallel_studio_xe/16.0.1/2016.1.150
module load chpc/netcdf/4.4.3-F/intel/16.0.1
module load chpc/hdf5/1.8.16/intel/16.0.1

# Set environment variables
export OMP_NUM_THREADS=1
export I_MPI_PIN_DOMAIN=omp

echo "Starting WRF simulation: {job_name}"
echo "Job directory: $PWD"
echo "Date: $(date)"
echo "Hostname: $(hostname)"

# Run WPS if requested
"""
        
        if run_wps:
            script += f"""
# Run WPS preprocessing
echo "Running WPS..."
cd {self.wps_exe_path}

# Link WPS data
./link_grib.csh /path/to/grib/data/*

# Run geogrid
./geogrid.exe

# Run ungrib
./ungrib.exe

# Run metgrid
./metgrid.exe

cd {job_dir}
"""
        
        script += f"""
# Run WRF
echo "Running WRF..."
cd {self.wrf_exe_path}

# Real data initialization
./real.exe

# WRF model run
mpirun -np $((PBS_NUM_NODES * PBS_NUM_PPN)) ./wrf.exe

echo "WRF simulation completed: $(date)"
"""
        
        return script
    
    def _submit_job_script(self, script_content: str, job_name: str) -> Dict[str, Any]:
        """Submit the job script to PBS"""
        # Create temporary script file
        script_file = f"/tmp/{job_name}.pbs"
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        # Submit job
        result = self._run_command(f"qsub {script_file}")
        
        if result["success"]:
            job_id = result["stdout"].strip()
            return {"job_id": job_id, "success": True}
        else:
            return {"success": False, "error": result["stderr"]}
    
    def get_wrf_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get status of a WRF job"""
        result = self._run_command(f"qstat {job_id}")
        
        if result["success"]:
            # Parse qstat output
            lines = result["stdout"].strip().split('\n')
            if len(lines) >= 2:
                job_line = lines[1]
                parts = job_line.split()
                if len(parts) >= 5:
                    return {
                        "job_id": parts[0],
                        "job_name": parts[1],
                        "status": parts[4],
                        "queue": parts[2],
                        "success": True
                    }
        
        return {"success": False, "error": "Job not found or error parsing status"}
    
    def list_wrf_jobs(self) -> Dict[str, Any]:
        """List all WRF jobs for the current user"""
        result = self._run_command("qstat -u $USER")
        
        if result["success"]:
            lines = result["stdout"].strip().split('\n')
            jobs = []
            
            for line in lines[2:]:  # Skip header lines
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 5:
                        job_info = {
                            "job_id": parts[0],
                            "job_name": parts[1],
                            "status": parts[4],
                            "queue": parts[2]
                        }
                        # Filter for WRF jobs (you can customize this)
                        if "wrf" in job_info["job_name"].lower():
                            jobs.append(job_info)
            
            return {
                "success": True,
                "jobs": jobs,
                "total_jobs": len(jobs)
            }
        
        return {"success": False, "error": result["stderr"]}
    
    def cancel_wrf_job(self, job_id: str) -> Dict[str, Any]:
        """Cancel a WRF job"""
        result = self._run_command(f"qdel {job_id}")
        
        return {
            "success": result["success"],
            "message": "Job cancelled successfully" if result["success"] else result["stderr"]
        }
    
    def get_wrf_job_logs(self, job_id: str) -> Dict[str, Any]:
        """Get logs for a WRF job"""
        # Get job details
        status_result = self.get_wrf_job_status(job_id)
        if not status_result["success"]:
            return status_result
        
        job_name = status_result.get("job_name", "unknown")
        
        # Try to find log files
        log_files = []
        possible_paths = [
            f"~/wrf_jobs/{job_name}/wrf.out",
            f"~/wrf_jobs/{job_name}/wrf.err",
            f"~/wrf_jobs/{job_name}/rsl.out.0000",
            f"~/wrf_jobs/{job_name}/rsl.error.0000"
        ]
        
        logs = {}
        for path in possible_paths:
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                try:
                    with open(expanded_path, 'r') as f:
                        logs[os.path.basename(path)] = f.read()
                except Exception as e:
                    logs[os.path.basename(path)] = f"Error reading file: {e}"
        
        return {
            "success": True,
            "job_id": job_id,
            "job_name": job_name,
            "logs": logs
        }
