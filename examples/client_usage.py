#!/usr/bin/env python3
"""
Client example for using the Lengau Cluster Job Management API from a local machine.

This script demonstrates how to interact with the API running on the cluster
through an SSH tunnel.
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration for accessing the API via SSH tunnel
API_CONFIG = {
    "base_url": "http://localhost:8000/api/v1/cluster",  # Via SSH tunnel
    "timeout": 30,
    "headers": {
        "Content-Type": "application/json"
    }
}

class LengauAPIClient:
    """Client for interacting with the Lengau Cluster Job Management API."""
    
    def __init__(self, base_url: str = None, timeout: int = 30):
        self.base_url = base_url or API_CONFIG["base_url"]
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(API_CONFIG["headers"])
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a request to the API."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(
                method, url, timeout=self.timeout, **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            raise
    
    def get_cluster_info(self) -> Dict[str, Any]:
        """Get cluster information."""
        return self._make_request("GET", "/cluster/info")
    
    def submit_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a job to the cluster."""
        return self._make_request("POST", "/jobs", json=job_data)
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get the status of a specific job."""
        return self._make_request("GET", f"/jobs/{job_id}")
    
    def list_jobs(self, user: str = None) -> Dict[str, Any]:
        """List all jobs."""
        params = {"user": user} if user else {}
        return self._make_request("GET", "/jobs", params=params)
    
    def cancel_job(self, job_id: str) -> Dict[str, Any]:
        """Cancel a job."""
        return self._make_request("DELETE", f"/jobs/{job_id}")
    
    def get_job_logs(self, job_id: str) -> Dict[str, Any]:
        """Get job logs."""
        return self._make_request("GET", f"/jobs/{job_id}/logs")
    
    def get_available_queues(self) -> Dict[str, Any]:
        """Get available queues."""
        return self._make_request("GET", "/cluster/queues")
    
    def get_default_modules(self) -> Dict[str, Any]:
        """Get default modules."""
        return self._make_request("GET", "/cluster/modules")


def test_api_connection():
    """Test the API connection."""
    print("🔗 Testing API connection...")
    
    try:
        client = LengauAPIClient()
        cluster_info = client.get_cluster_info()
        print(f"✅ Connected to {cluster_info['cluster_name']} cluster")
        print(f"   Available queues: {cluster_info['available_queues']}")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to API: {e}")
        print("   Make sure:")
        print("   1. The API is running on the cluster")
        print("   2. You have an SSH tunnel: ssh -L 8000:localhost:8000 username@lengau.chpc.ac.za")
        print("   3. The API is accessible at http://localhost:8000")
        return False


def submit_simple_job():
    """Submit a simple test job."""
    print("\n📤 Submitting simple test job...")
    
    job_data = {
        "job_name": "api_test_job",
        "script_content": """#!/bin/bash
echo "Hello from API-submitted job!"
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
        client = LengauAPIClient()
        result = client.submit_job(job_data)
        print(f"✅ Job submitted successfully!")
        print(f"   Job ID: {result['job_id']}")
        print(f"   Status: {result['status']}")
        return result['job_id']
    except Exception as e:
        print(f"❌ Failed to submit job: {e}")
        return None


def monitor_job(job_id: str, max_wait: int = 300):
    """Monitor a job until completion."""
    print(f"\n👀 Monitoring job {job_id}...")
    
    client = LengauAPIClient()
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            status = client.get_job_status(job_id)
            print(f"   Status: {status['status']}")
            
            if status['status'] in ['COMPLETED', 'FAILED', 'CANCELLED']:
                print(f"   Job finished with status: {status['status']}")
                
                # Get logs
                logs = client.get_job_logs(job_id)
                if logs.get('stdout'):
                    print(f"   STDOUT: {logs['stdout'][:200]}...")
                if logs.get('stderr'):
                    print(f"   STDERR: {logs['stderr'][:200]}...")
                
                return status['status']
            
            time.sleep(10)  # Wait 10 seconds before checking again
            
        except Exception as e:
            print(f"   Error checking job status: {e}")
            time.sleep(10)
    
    print(f"   Timeout waiting for job completion")
    return None


def list_user_jobs():
    """List all jobs for the current user."""
    print("\n📋 Listing user jobs...")
    
    try:
        client = LengauAPIClient()
        jobs = client.list_jobs()
        print(f"   Total jobs: {jobs['total_jobs']}")
        
        for job in jobs['jobs']:
            print(f"   - {job['job_id']}: {job['job_name']} ({job['status']})")
        
        return jobs['jobs']
    except Exception as e:
        print(f"❌ Failed to list jobs: {e}")
        return []


def main():
    """Main function demonstrating API usage."""
    print("🚀 Lengau Cluster Job Management API - Client Example")
    print("=" * 60)
    
    # Test connection
    if not test_api_connection():
        return
    
    # Get cluster info
    try:
        client = LengauAPIClient()
        cluster_info = client.get_cluster_info()
        print(f"\n📊 Cluster Information:")
        print(f"   Name: {cluster_info['cluster_name']}")
        print(f"   Max nodes: {cluster_info['max_nodes']}")
        print(f"   Max cores per node: {cluster_info['max_cores_per_node']}")
        print(f"   Max memory per node: {cluster_info['max_memory_per_node']}")
    except Exception as e:
        print(f"❌ Failed to get cluster info: {e}")
    
    # List existing jobs
    list_user_jobs()
    
    # Submit a test job
    job_id = submit_simple_job()
    
    if job_id:
        # Monitor the job
        final_status = monitor_job(job_id)
        print(f"\n✅ Job monitoring complete. Final status: {final_status}")
    
    print("\n🎉 Client example completed!")
    print("\n💡 Tips:")
    print("   - Keep the SSH tunnel open while using the API")
    print("   - Use the interactive docs at http://localhost:8000/docs")
    print("   - Check the cluster documentation for more examples")


if __name__ == "__main__":
    main()



