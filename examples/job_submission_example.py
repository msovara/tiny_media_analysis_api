#!/usr/bin/env python3
"""
Example script demonstrating how to use the Lengau Cluster Job Management API.

This script shows various examples of job submissions including:
- Simple shell script jobs
- ARWpost jobs
- WRF model jobs
- Data processing jobs
"""

import requests
import json
import time
from typing import Dict, Any

# API base URL
API_BASE_URL = "http://localhost:8000/api/v1/cluster"

def submit_job(job_data: Dict[str, Any]) -> Dict[str, Any]:
    """Submit a job to the cluster."""
    response = requests.post(f"{API_BASE_URL}/jobs", json=job_data)
    response.raise_for_status()
    return response.json()

def get_job_status(job_id: str) -> Dict[str, Any]:
    """Get the status of a job."""
    response = requests.get(f"{API_BASE_URL}/jobs/{job_id}")
    response.raise_for_status()
    return response.json()

def list_jobs() -> Dict[str, Any]:
    """List all jobs."""
    response = requests.get(f"{API_BASE_URL}/jobs")
    response.raise_for_status()
    return response.json()

def get_job_logs(job_id: str) -> Dict[str, Any]:
    """Get job logs."""
    response = requests.get(f"{API_BASE_URL}/jobs/{job_id}/logs")
    response.raise_for_status()
    return response.json()

def cancel_job(job_id: str) -> Dict[str, Any]:
    """Cancel a job."""
    response = requests.delete(f"{API_BASE_URL}/jobs/{job_id}")
    response.raise_for_status()
    return response.json()

def get_cluster_info() -> Dict[str, Any]:
    """Get cluster information."""
    response = requests.get(f"{API_BASE_URL}/cluster/info")
    response.raise_for_status()
    return response.json()

def example_1_simple_shell_job():
    """Example 1: Simple shell script job."""
    print("=== Example 1: Simple Shell Script Job ===")
    
    job_data = {
        "job_name": "simple_test_job",
        "script_content": """#!/bin/bash
echo "Hello from Lengau cluster!"
echo "Current date: $(date)"
echo "Hostname: $(hostname)"
echo "Working directory: $(pwd)"
echo "Job completed successfully!"
""",
        "queue": "normal",
        "nodes": 1,
        "cores_per_node": 1,
        "memory_per_node": "4GB",
        "walltime": "00:10:00"
    }
    
    try:
        result = submit_job(job_data)
        print(f"Job submitted successfully: {result}")
        return result["job_id"]
    except Exception as e:
        print(f"Error submitting job: {e}")
        return None

def example_2_arwpost_job():
    """Example 2: ARWpost job for WRF post-processing."""
    print("\n=== Example 2: ARWpost Job ===")
    
    job_data = {
        "job_name": "arwpost_processing",
        "script_content": """#!/bin/bash
# Load required modules
module load arwpost/3.1
module load chpc/netcdf/4.4.3-F/intel/16.0.1

# Set working directory
cd $PBS_O_WORKDIR

# Create ARWpost namelist
cat > namelist.ARWpost << EOF
&datetime
 start_date = '2023-01-01_00:00:00',
 end_date   = '2023-01-02_00:00:00',
 interval_seconds = 3600,
 tacc = 0,
 debug_level = 0,
/

&io
 io_form_input = 2,
 io_form_output = 2,
 input_root_name = './wrfout_d01_',
 output_root_name = './ARWpost_output_',
 plot = 'all_list',
 plot_fields = 'height,pressure,temp,rh,wind_speed,wind_dir',
/
EOF

# Run ARWpost
echo "Starting ARWpost processing..."
ARWpost

if [ $? -eq 0 ]; then
    echo "ARWpost completed successfully!"
else
    echo "ARWpost failed!"
    exit 1
fi
""",
        "queue": "normal",
        "nodes": 2,
        "cores_per_node": 8,
        "memory_per_node": "32GB",
        "walltime": "02:00:00",
        "modules": [
            "chpc/parallel_studio_xe/16.0.1/2016.1.150",
            "chpc/netcdf/4.4.3-F/intel/16.0.1",
            "chpc/hdf5/1.8.16/intel/16.0.1"
        ],
        "environment_variables": {
            "OMP_NUM_THREADS": "8",
            "MPI_NUM_THREADS": "8"
        }
    }
    
    try:
        result = submit_job(job_data)
        print(f"ARWpost job submitted successfully: {result}")
        return result["job_id"]
    except Exception as e:
        print(f"Error submitting ARWpost job: {e}")
        return None

def example_3_wrf_model_job():
    """Example 3: WRF model simulation job."""
    print("\n=== Example 3: WRF Model Job ===")
    
    job_data = {
        "job_name": "wrf_simulation",
        "script_content": """#!/bin/bash
# Load WRF modules
module load chpc/parallel_studio_xe/16.0.1/2016.1.150
module load chpc/netcdf/4.4.3-F/intel/16.0.1
module load chpc/hdf5/1.8.16/intel/16.0.1

# Set working directory
cd $PBS_O_WORKDIR

# Set environment variables
export OMP_NUM_THREADS=8
export MPI_NUM_THREADS=8

# Run WRF real.exe
echo "Running WRF real.exe..."
mpirun -np 16 ./real.exe

if [ $? -ne 0 ]; then
    echo "real.exe failed!"
    exit 1
fi

# Run WRF wrf.exe
echo "Running WRF wrf.exe..."
mpirun -np 16 ./wrf.exe

if [ $? -eq 0 ]; then
    echo "WRF simulation completed successfully!"
else
    echo "WRF simulation failed!"
    exit 1
fi
""",
        "queue": "long",
        "nodes": 4,
        "cores_per_node": 16,
        "memory_per_node": "64GB",
        "walltime": "24:00:00",
        "modules": [
            "chpc/parallel_studio_xe/16.0.1/2016.1.150",
            "chpc/netcdf/4.4.3-F/intel/16.0.1",
            "chpc/hdf5/1.8.16/intel/16.0.1"
        ],
        "environment_variables": {
            "OMP_NUM_THREADS": "8",
            "MPI_NUM_THREADS": "8",
            "WRF_NUM_TILES": "4"
        }
    }
    
    try:
        result = submit_job(job_data)
        print(f"WRF job submitted successfully: {result}")
        return result["job_id"]
    except Exception as e:
        print(f"Error submitting WRF job: {e}")
        return None

def example_4_data_processing_job():
    """Example 4: Data processing job with Python."""
    print("\n=== Example 4: Data Processing Job ===")
    
    job_data = {
        "job_name": "data_analysis",
        "script_content": """#!/bin/bash
# Load Python module
module load chpc/python/3.8.5

# Set working directory
cd $PBS_O_WORKDIR

# Create Python script
cat > data_analysis.py << 'EOF'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

print(f"Starting data analysis at {datetime.now()}")

# Generate sample data
np.random.seed(42)
data = np.random.normal(0, 1, 1000)

# Perform analysis
mean_val = np.mean(data)
std_val = np.std(data)
print(f"Mean: {mean_val:.4f}")
print(f"Standard deviation: {std_val:.4f}")

# Create plot
plt.figure(figsize=(10, 6))
plt.hist(data, bins=50, alpha=0.7, color='blue')
plt.axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.4f}')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Data Distribution')
plt.legend()
plt.savefig('data_analysis_plot.png', dpi=300, bbox_inches='tight')
plt.close()

print("Data analysis completed successfully!")
EOF

# Run Python script
python data_analysis.py

if [ $? -eq 0 ]; then
    echo "Data analysis completed successfully!"
else
    echo "Data analysis failed!"
    exit 1
fi
""",
        "queue": "normal",
        "nodes": 1,
        "cores_per_node": 4,
        "memory_per_node": "16GB",
        "walltime": "01:00:00",
        "modules": ["chpc/python/3.8.5"]
    }
    
    try:
        result = submit_job(job_data)
        print(f"Data processing job submitted successfully: {result}")
        return result["job_id"]
    except Exception as e:
        print(f"Error submitting data processing job: {e}")
        return None

def monitor_jobs(job_ids: list):
    """Monitor the status of submitted jobs."""
    print("\n=== Monitoring Jobs ===")
    
    for job_id in job_ids:
        if job_id:
            try:
                status = get_job_status(job_id)
                print(f"Job {job_id}: {status['status']}")
                
                # If job is completed, show logs
                if status['status'] in ['COMPLETED', 'FAILED']:
                    logs = get_job_logs(job_id)
                    if logs.get('stdout'):
                        print(f"  STDOUT: {logs['stdout'][:200]}...")
                    if logs.get('stderr'):
                        print(f"  STDERR: {logs['stderr'][:200]}...")
                        
            except Exception as e:
                print(f"Error getting status for job {job_id}: {e}")

def main():
    """Main function to run all examples."""
    print("Lengau Cluster Job Management API Examples")
    print("=" * 50)
    
    # Get cluster info
    try:
        cluster_info = get_cluster_info()
        print(f"Cluster: {cluster_info['cluster_name']}")
        print(f"Available queues: {cluster_info['available_queues']}")
    except Exception as e:
        print(f"Error getting cluster info: {e}")
    
    # Submit example jobs
    job_ids = []
    
    # Example 1: Simple shell job
    job_id = example_1_simple_shell_job()
    job_ids.append(job_id)
    
    # Example 2: ARWpost job
    job_id = example_2_arwpost_job()
    job_ids.append(job_id)
    
    # Example 3: WRF model job
    job_id = example_3_wrf_model_job()
    job_ids.append(job_id)
    
    # Example 4: Data processing job
    job_id = example_4_data_processing_job()
    job_ids.append(job_id)
    
    # List all jobs
    try:
        jobs = list_jobs()
        print(f"\nTotal jobs in queue: {jobs['total_jobs']}")
    except Exception as e:
        print(f"Error listing jobs: {e}")
    
    # Monitor jobs
    monitor_jobs(job_ids)
    
    print("\n=== Examples Completed ===")
    print("Check the API documentation at http://localhost:8000/docs for more details.")

if __name__ == "__main__":
    main()



































