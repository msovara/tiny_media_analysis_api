# WRF API User Access Guide

## 🌐 **How to Access the WRF API on Lengau Cluster**

This guide explains how different users can access and use the WRF API running on the Lengau cluster.

## 📋 **Prerequisites**

- CHPC account with access to Lengau cluster
- Basic knowledge of SSH and command line
- Python 3.6+ (for running client scripts)

## 🚀 **Access Methods**

### **Method 1: Direct Cluster Access (Recommended)**

If you have a CHPC account and can SSH to the cluster:

```bash
# SSH to the cluster
ssh YOUR_USERNAME@login2.lengau.chpc.ac.za

# Access the API directly
curl http://localhost:8000/api/v1/wrf/info

# Or use the Python client
python examples/wrf_examples.py
```

### **Method 2: SSH Tunnel (For External Users)**

If you're outside the CHPC network but have cluster access:

```bash
# Create SSH tunnel from your local machine
ssh -L 8000:localhost:8000 YOUR_USERNAME@login2.lengau.chpc.ac.za

# In another terminal, access the API locally
curl http://localhost:8000/api/v1/wrf/info
```

### **Method 3: Web Interface (Recommended for Users)**

Access the user-friendly web dashboard:

```bash
# Web Dashboard (most user-friendly)
http://localhost:8000/dashboard

# API Documentation (interactive)
http://localhost:8000/docs

# Alternative Documentation
http://localhost:8000/redoc
```

### **Method 4: Public Access (If Available)**

If the API is configured for public access:

```bash
# Access via public URL (if configured)
curl http://login2.lengau.chpc.ac.za:8080/api/v1/wrf/info
```

## 📚 **API Endpoints**

### **WRF Information**
```bash
# Get WRF installation info
curl http://localhost:8000/api/v1/wrf/info

# Get example configurations
curl http://localhost:8000/api/v1/wrf/examples
```

### **Job Management**
```bash
# Submit a WRF job
curl -X POST http://localhost:8000/api/v1/wrf/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "job_name": "my_wrf_simulation",
    "queue": "normal",
    "nodes": 2,
    "cores_per_node": 16,
    "walltime": "04:00:00",
    "wrf_config": {
      "domain": "south_africa",
      "resolution": "12km",
      "simulation_days": 7
    }
  }'

# List WRF jobs
curl http://localhost:8000/api/v1/wrf/jobs

# Get job status
curl http://localhost:8000/api/v1/wrf/jobs/JOB_ID

# Get job logs
curl http://localhost:8000/api/v1/wrf/jobs/JOB_ID/logs
```

### **Templates and Validation**
```bash
# Get WRF namelist template
curl http://localhost:8000/api/v1/wrf/templates/namelist

# Get WPS namelist template
curl http://localhost:8000/api/v1/wrf/templates/wps-namelist

# Validate configuration
curl -X POST http://localhost:8000/api/v1/wrf/validate-config \
  -H "Content-Type: application/json" \
  -d '{"domain": "south_africa", "resolution": "12km"}'
```

## 🌐 **Web Interface Usage**

### **Web Dashboard Features**
The web dashboard provides a user-friendly interface for:
- **System Information**: View WRF installation details and available executables
- **Job Submission**: Submit WRF jobs through an intuitive web form
- **Job Management**: Monitor job status, view logs, and cancel jobs
- **Templates**: View and copy WRF and WPS namelist templates
- **API Documentation**: Direct access to interactive API documentation

### **Accessing the Web Interface**
```bash
# From the cluster
http://localhost:8000/dashboard

# From external machine (via SSH tunnel)
ssh -L 8000:localhost:8000 USERNAME@login2.lengau.chpc.ac.za
# Then open: http://localhost:8000/dashboard
```

## 🐍 **Python Client Usage**

### **Install Required Packages**
```bash
pip install requests
```

### **Basic Client Script**
```python
import requests
import json

# API Configuration
BASE_URL = "http://localhost:8000"
WRF_API_BASE = f"{BASE_URL}/api/v1/wrf"

def get_wrf_info():
    """Get WRF installation information."""
    response = requests.get(f"{WRF_API_BASE}/info")
    return response.json()

def submit_wrf_job(job_config):
    """Submit a WRF job."""
    response = requests.post(f"{WRF_API_BASE}/jobs", json=job_config)
    return response.json()

def list_wrf_jobs():
    """List all WRF jobs."""
    response = requests.get(f"{WRF_API_BASE}/jobs")
    return response.json()

# Example usage
if __name__ == "__main__":
    # Get WRF info
    info = get_wrf_info()
    print("WRF Info:", json.dumps(info, indent=2))
    
    # Submit a job
    job_config = {
        "job_name": "test_simulation",
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
    
    result = submit_wrf_job(job_config)
    print("Job Submission:", json.dumps(result, indent=2))
```

## 📋 **Example Job Configurations**

### **South Africa Regional Simulation**
```json
{
  "job_name": "sa_regional_sim",
  "queue": "normal",
  "nodes": 2,
  "cores_per_node": 16,
  "walltime": "04:00:00",
  "wrf_config": {
    "domain": "south_africa",
    "resolution": "12km",
    "simulation_days": 7,
    "start_date": "2024-01-01",
    "end_date": "2024-01-08"
  }
}
```

### **High-Resolution Local Simulation**
```json
{
  "job_name": "high_res_local",
  "queue": "normal",
  "nodes": 4,
  "cores_per_node": 24,
  "walltime": "08:00:00",
  "wrf_config": {
    "domain": "local",
    "resolution": "3km",
    "simulation_days": 3,
    "start_date": "2024-01-01",
    "end_date": "2024-01-04"
  }
}
```

## 🔧 **Troubleshooting**

### **Connection Issues**
- **"Could not resolve hostname"**: You need to be on the CHPC network or use VPN
- **"Connection refused"**: The API might not be running, contact the administrator
- **"Permission denied"**: Check your SSH key configuration

### **API Errors**
- **404 Not Found**: Check the endpoint URL
- **400 Bad Request**: Validate your JSON payload
- **500 Internal Server Error**: Contact the API administrator

### **Job Submission Issues**
- **"Queue not found"**: Check available queues with `qconf -sql`
- **"Insufficient resources"**: Reduce node count or request different queue
- **"Project not found"**: Verify your project allocation

## 📞 **Support**

For issues with:
- **API Access**: Contact the API administrator (msovara)
- **WRF Configuration**: Check the WRF documentation
- **Cluster Access**: Contact CHPC support
- **Job Scheduling**: Use `qstat`, `qdel`, `qconf` commands

## 🔗 **Useful Links**

- **API Documentation**: http://localhost:8000/docs (when accessed from cluster)
- **WRF Documentation**: https://www.mmm.ucar.edu/weather-research-and-forecasting-model
- **CHPC Support**: https://www.chpc.ac.za/support
- **Lengau Cluster Info**: https://www.chpc.ac.za/index.php/lengau-cluster

## 📝 **Notes**

- The API runs on port 8000 on the cluster
- Jobs are submitted to the PBS queue system
- Output files are stored in `/mnt/lustre/users/msovara/wrf_jobs/`
- The API uses the RCHPC project for job submissions
- All times are in UTC
