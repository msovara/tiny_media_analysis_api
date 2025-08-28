#!/usr/bin/env python3
"""
WRF API Client for Lengau Cluster
Simple client script for interacting with the WRF API
"""

import requests
import json
import time
from typing import Dict, Any, Optional

class WRFClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the WRF client."""
        self.base_url = base_url
        self.wrf_api_base = f"{base_url}/api/v1/wrf"
        
    def get_wrf_info(self) -> Dict[str, Any]:
        """Get WRF installation information."""
        try:
            response = requests.get(f"{self.wrf_api_base}/info")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get WRF info: {str(e)}"}
    
    def get_examples(self) -> Dict[str, Any]:
        """Get example WRF configurations."""
        try:
            response = requests.get(f"{self.wrf_api_base}/examples")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get examples: {str(e)}"}
    
    def submit_wrf_job(self, job_config: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a WRF job."""
        try:
            response = requests.post(f"{self.wrf_api_base}/jobs", json=job_config)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to submit job: {str(e)}"}
    
    def list_wrf_jobs(self) -> Dict[str, Any]:
        """List all WRF jobs."""
        try:
            response = requests.get(f"{self.wrf_api_base}/jobs")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to list jobs: {str(e)}"}
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get status of a specific WRF job."""
        try:
            response = requests.get(f"{self.wrf_api_base}/jobs/{job_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get job status: {str(e)}"}
    
    def get_job_logs(self, job_id: str) -> Dict[str, Any]:
        """Get logs of a specific WRF job."""
        try:
            response = requests.get(f"{self.wrf_api_base}/jobs/{job_id}/logs")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get job logs: {str(e)}"}
    
    def cancel_wrf_job(self, job_id: str) -> Dict[str, Any]:
        """Cancel a WRF job."""
        try:
            response = requests.delete(f"{self.wrf_api_base}/jobs/{job_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to cancel job: {str(e)}"}
    
    def get_namelist_template(self) -> Dict[str, Any]:
        """Get WRF namelist template."""
        try:
            response = requests.get(f"{self.wrf_api_base}/templates/namelist")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get namelist template: {str(e)}"}
    
    def get_wps_namelist_template(self) -> Dict[str, Any]:
        """Get WPS namelist template."""
        try:
            response = requests.get(f"{self.wrf_api_base}/templates/wps-namelist")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get WPS namelist template: {str(e)}"}
    
    def validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate WRF configuration."""
        try:
            response = requests.post(f"{self.wrf_api_base}/validate-config", json=config)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to validate config: {str(e)}"}
    
    def monitor_job(self, job_id: str, max_checks: int = 10, interval: int = 30) -> None:
        """Monitor a job until completion."""
        print(f"Monitoring job {job_id}...")
        
        for i in range(max_checks):
            status = self.get_job_status(job_id)
            
            if "error" in status:
                print(f"Error getting job status: {status['error']}")
                break
            
            job_status = status.get("status", "UNKNOWN")
            print(f"Check {i+1}/{max_checks}: Job {job_id} status: {job_status}")
            
            if job_status in ["COMPLETED", "FAILED", "CANCELLED"]:
                print(f"Job {job_id} finished with status: {job_status}")
                break
            
            if i < max_checks - 1:
                print(f"Waiting {interval} seconds before next check...")
                time.sleep(interval)
        else:
            print(f"Monitoring timeout after {max_checks} checks")

def print_response(response: Dict[str, Any], title: str):
    """Print a formatted response."""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(json.dumps(response, indent=2))

def main():
    """Main function demonstrating WRF client usage."""
    print("WRF API Client for Lengau Cluster")
    print("="*50)
    
    # Initialize client
    client = WRFClient()
    
    # Test basic functionality
    print_response(client.get_wrf_info(), "WRF Installation Info")
    print_response(client.get_examples(), "Example Configurations")
    
    # Example job submission
    job_config = {
        "job_name": "client_test_simulation",
        "queue": "normal",
        "nodes": 1,
        "cores_per_node": 8,
        "walltime": "02:00:00",
        "wrf_config": {
            "domain": "south_africa",
            "resolution": "12km",
            "simulation_days": 3
        }
    }
    
    print_response(client.validate_config(job_config["wrf_config"]), "Configuration Validation")
    print_response(client.submit_wrf_job(job_config), "Job Submission")
    
    # List jobs
    print_response(client.list_wrf_jobs(), "Current WRF Jobs")
    
    # Get templates
    print_response(client.get_namelist_template(), "WRF Namelist Template")
    print_response(client.get_wps_namelist_template(), "WPS Namelist Template")

if __name__ == "__main__":
    main()

