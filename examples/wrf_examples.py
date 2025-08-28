#!/usr/bin/env python3
"""
WRF API Examples for Lengau Cluster
Demonstrates how to use the WRF API for various simulation scenarios
"""

import requests
import json
import time
from typing import Dict, Any

# API Configuration
BASE_URL = "http://localhost:8080"  # Update with your API URL
WRF_API_BASE = f"{BASE_URL}/api/v1/wrf"

def print_response(response: requests.Response, title: str):
    """Print API response in a formatted way"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except:
        print(response.text)
    print(f"{'='*50}\n")

def test_wrf_info():
    """Test getting WRF information"""
    print("Testing WRF Information...")
    response = requests.get(f"{WRF_API_BASE}/info")
    print_response(response, "WRF Installation Information")

def test_namelist_templates():
    """Test getting namelist templates"""
    print("Testing Namelist Templates...")
    
    # WRF namelist template
    response = requests.get(f"{WRF_API_BASE}/templates/namelist")
    print_response(response, "WRF Namelist Template")
    
    # WPS namelist template
    response = requests.get(f"{WRF_API_BASE}/templates/wps-namelist")
    print_response(response, "WPS Namelist Template")

def test_examples():
    """Test getting example configurations"""
    print("Testing Example Configurations...")
    response = requests.get(f"{WRF_API_BASE}/examples")
    print_response(response, "WRF Example Configurations")

def submit_simple_wrf_job():
    """Submit a simple WRF job"""
    print("Submitting Simple WRF Job...")
    
    job_config = {
        "job_name": "simple_wrf_test",
        "queue": "normal",
        "nodes": 2,
        "cores_per_node": 16,
        "memory_per_node": "64GB",
        "walltime": "24:00:00",
        "run_wps": False,
        "wrf_config": {
            "run_hours": 24,
            "start_year": 2023,
            "start_month": 1,
            "start_day": 1,
            "end_year": 2023,
            "end_month": 1,
            "end_day": 2,
            "time_step": 180,
            "dx": [30000],
            "dy": [30000],
            "e_we": [74],
            "e_sn": [61],
            "e_vert": [28],
            "mp_physics": [3],
            "ra_lw_physics": [1],
            "ra_sw_physics": [1],
            "sf_sfclay_physics": [1],
            "sf_surface_physics": [1],
            "bl_pbl_physics": [1],
            "cu_physics": [1]
        }
    }
    
    response = requests.post(f"{WRF_API_BASE}/jobs", json=job_config)
    print_response(response, "Simple WRF Job Submission")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return data.get("job_id")
    
    return None

def submit_south_africa_case():
    """Submit a South Africa regional case"""
    print("Submitting South Africa Regional Case...")
    
    job_config = {
        "job_name": "sa_regional_case",
        "queue": "normal",
        "nodes": 4,
        "cores_per_node": 32,
        "memory_per_node": "128GB",
        "walltime": "48:00:00",
        "run_wps": True,
        "wrf_config": {
            "run_hours": 48,
            "start_year": 2023,
            "start_month": 1,
            "start_day": 1,
            "end_year": 2023,
            "end_month": 1,
            "end_day": 3,
            "time_step": 180,
            "dx": [15000],
            "dy": [15000],
            "e_we": [148],
            "e_sn": [121],
            "e_vert": [35],
            "mp_physics": [3],
            "ra_lw_physics": [1],
            "ra_sw_physics": [1],
            "sf_sfclay_physics": [1],
            "sf_surface_physics": [1],
            "bl_pbl_physics": [1],
            "cu_physics": [1]
        },
        "wps_config": {
            "start_date": "2023-01-01_00:00:00",
            "end_date": "2023-01-03_00:00:00",
            "interval_seconds": 21600,
            "geog_data_res": "default",
            "map_proj": "lambert",
            "ref_lat": -34.0,
            "ref_lon": 18.5,
            "truelat1": -34.0,
            "truelat2": -34.0,
            "stand_lon": 18.5,
            "geog_data_path": "/apps/chpc/earth/WPS_GEOG"
        }
    }
    
    response = requests.post(f"{WRF_API_BASE}/jobs", json=job_config)
    print_response(response, "South Africa Regional Case Submission")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return data.get("job_id")
    
    return None

def submit_high_resolution_case():
    """Submit a high resolution urban case"""
    print("Submitting High Resolution Urban Case...")
    
    job_config = {
        "job_name": "high_res_urban",
        "queue": "normal",
        "nodes": 8,
        "cores_per_node": 32,
        "memory_per_node": "128GB",
        "walltime": "72:00:00",
        "run_wps": True,
        "wrf_config": {
            "run_hours": 72,
            "start_year": 2023,
            "start_month": 1,
            "start_day": 1,
            "end_year": 2023,
            "end_month": 1,
            "end_day": 4,
            "time_step": 60,
            "dx": [5000],
            "dy": [5000],
            "e_we": [200],
            "e_sn": [200],
            "e_vert": [40],
            "mp_physics": [8],
            "ra_lw_physics": [3],
            "ra_sw_physics": [3],
            "sf_sfclay_physics": [2],
            "sf_surface_physics": [2],
            "bl_pbl_physics": [2],
            "cu_physics": [2],
            "sf_urban_physics": [1]
        },
        "wps_config": {
            "start_date": "2023-01-01_00:00:00",
            "end_date": "2023-01-04_00:00:00",
            "interval_seconds": 21600,
            "geog_data_res": "30s",
            "map_proj": "lambert",
            "ref_lat": -34.0,
            "ref_lon": 18.5,
            "truelat1": -34.0,
            "truelat2": -34.0,
            "stand_lon": 18.5
        }
    }
    
    response = requests.post(f"{WRF_API_BASE}/jobs", json=job_config)
    print_response(response, "High Resolution Urban Case Submission")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return data.get("job_id")
    
    return None

def monitor_job(job_id: str, max_checks: int = 10):
    """Monitor a WRF job"""
    print(f"Monitoring WRF Job: {job_id}")
    
    for i in range(max_checks):
        response = requests.get(f"{WRF_API_BASE}/jobs/{job_id}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                status = data.get("status", "UNKNOWN")
                print(f"Check {i+1}: Job {job_id} status = {status}")
                
                if status in ["COMPLETED", "FAILED", "CANCELLED"]:
                    print(f"Job {job_id} finished with status: {status}")
                    return status
            else:
                print(f"Check {i+1}: Error getting job status")
        else:
            print(f"Check {i+1}: HTTP error {response.status_code}")
        
        # Wait 30 seconds before next check
        if i < max_checks - 1:
            print("Waiting 30 seconds before next check...")
            time.sleep(30)
    
    print(f"Monitoring timeout for job {job_id}")
    return "TIMEOUT"

def get_job_logs(job_id: str):
    """Get logs for a WRF job"""
    print(f"Getting logs for WRF Job: {job_id}")
    response = requests.get(f"{WRF_API_BASE}/jobs/{job_id}/logs")
    print_response(response, f"WRF Job Logs for {job_id}")

def list_wrf_jobs():
    """List all WRF jobs"""
    print("Listing WRF Jobs...")
    response = requests.get(f"{WRF_API_BASE}/jobs")
    print_response(response, "WRF Jobs List")

def validate_config():
    """Test configuration validation"""
    print("Testing Configuration Validation...")
    
    # Valid configuration
    valid_config = {
        "run_hours": 24,
        "start_year": 2023,
        "end_year": 2023,
        "time_step": 180,
        "dx": [30000],
        "dy": [30000],
        "e_we": [74],
        "e_sn": [61]
    }
    
    response = requests.post(f"{WRF_API_BASE}/validate-config", json=valid_config)
    print_response(response, "Valid Configuration Test")
    
    # Invalid configuration
    invalid_config = {
        "run_hours": 24,
        "start_year": 2024,  # Start year after end year
        "end_year": 2023,
        "time_step": -180,   # Negative time step
        "dx": [30000],
        "dy": [30000],
        "e_we": [74],
        "e_sn": [61]
    }
    
    response = requests.post(f"{WRF_API_BASE}/validate-config", json=invalid_config)
    print_response(response, "Invalid Configuration Test")

def main():
    """Main function to run all examples"""
    print("WRF API Examples for Lengau Cluster")
    print("=" * 50)
    
    # Test basic functionality
    test_wrf_info()
    test_namelist_templates()
    test_examples()
    validate_config()
    
    # List existing jobs
    list_wrf_jobs()
    
    # Submit different types of jobs
    print("\nSubmitting WRF Jobs...")
    
    # Simple case
    simple_job_id = submit_simple_wrf_job()
    
    # South Africa case
    sa_job_id = submit_south_africa_case()
    
    # High resolution case
    hr_job_id = submit_high_resolution_case()
    
    # Monitor jobs if they were submitted successfully
    if simple_job_id:
        print(f"\nMonitoring simple job: {simple_job_id}")
        status = monitor_job(simple_job_id, max_checks=5)
        if status in ["COMPLETED", "FAILED"]:
            get_job_logs(simple_job_id)
    
    if sa_job_id:
        print(f"\nMonitoring SA regional job: {sa_job_id}")
        status = monitor_job(sa_job_id, max_checks=3)
        if status in ["COMPLETED", "FAILED"]:
            get_job_logs(sa_job_id)
    
    if hr_job_id:
        print(f"\nMonitoring high resolution job: {hr_job_id}")
        status = monitor_job(hr_job_id, max_checks=3)
        if status in ["COMPLETED", "FAILED"]:
            get_job_logs(hr_job_id)
    
    # Final job list
    print("\nFinal WRF Jobs List:")
    list_wrf_jobs()
    
    print("\nWRF API Examples completed!")

if __name__ == "__main__":
    main()
