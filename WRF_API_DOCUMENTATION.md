# WRF API Documentation for Lengau Cluster

## 🌪️ Overview

The WRF (Weather Research and Forecasting) API provides a comprehensive interface for managing WRF simulations on the CHPC Lengau cluster. This API allows users to submit, monitor, and manage WRF jobs programmatically, with support for both WRF model runs and WPS (WRF Preprocessing System) preprocessing.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   WRF API       │    │   WRF Service   │    │   Lengau PBS    │
│                 │◄──►│                 │◄──►│                 │
│ - REST Endpoints│    │ - Job Creation  │    │ - Job Execution │
│ - Validation    │    │ - Namelist Gen  │    │ - Resource Mgmt │
│ - Monitoring    │    │ - PBS Scripts   │    │ - WRF Execution │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

### WRF Installation
- WRF 4.1.1 installed at `/apps/chpc/earth/WRF-4.1.1-impi`
- WPS (WRF Preprocessing System) available
- Required modules: Intel Parallel Studio, NetCDF, HDF5

### API Access
- API running on cluster (see main README for setup)
- Access to PBS job scheduler
- Sufficient cluster resources for WRF simulations

## 🚀 Quick Start

### 1. Check WRF Installation

```bash
# Get WRF information
curl http://localhost:8080/api/v1/wrf/info
```

### 2. Submit a Simple WRF Job

```bash
curl -X POST http://localhost:8080/api/v1/wrf/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "job_name": "simple_wrf_test",
    "queue": "normal",
    "nodes": 2,
    "cores_per_node": 16,
    "memory_per_node": "64GB",
    "walltime": "24:00:00",
    "run_wps": false,
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
      "e_sn": [61]
    }
  }'
```

### 3. Monitor Job Status

```bash
# Get job status
curl http://localhost:8080/api/v1/wrf/jobs/{job_id}

# Get job logs
curl http://localhost:8080/api/v1/wrf/jobs/{job_id}/logs
```

## 📡 API Endpoints

### WRF Information

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/wrf/info` | Get WRF installation information |

### Job Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/wrf/jobs` | Submit a WRF job |
| `GET` | `/api/v1/wrf/jobs` | List WRF jobs |
| `GET` | `/api/v1/wrf/jobs/{job_id}` | Get WRF job status |
| `DELETE` | `/api/v1/wrf/jobs/{job_id}` | Cancel WRF job |
| `GET` | `/api/v1/wrf/jobs/{job_id}/logs` | Get WRF job logs |

### Templates and Validation

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/wrf/templates/namelist` | Get WRF namelist template |
| `GET` | `/api/v1/wrf/templates/wps-namelist` | Get WPS namelist template |
| `POST` | `/api/v1/wrf/validate-config` | Validate WRF configuration |
| `GET` | `/api/v1/wrf/examples` | Get example configurations |

## 🔧 Configuration Parameters

### WRF Configuration (`wrf_config`)

#### Time Control
```json
{
  "run_days": 0,
  "run_hours": 24,
  "run_minutes": 0,
  "run_seconds": 0,
  "start_year": 2023,
  "start_month": 1,
  "start_day": 1,
  "start_hour": 0,
  "end_year": 2023,
  "end_month": 1,
  "end_day": 2,
  "end_hour": 0,
  "interval_seconds": 21600,
  "history_interval": 180,
  "frames_per_outfile": 1000
}
```

#### Domain Configuration
```json
{
  "time_step": 180,
  "max_dom": 1,
  "e_we": [74],
  "e_sn": [61],
  "e_vert": [28],
  "dx": [30000],
  "dy": [30000],
  "p_top_requested": 5000
}
```

#### Physics Schemes
```json
{
  "mp_physics": [3],
  "ra_lw_physics": [1],
  "ra_sw_physics": [1],
  "sf_sfclay_physics": [1],
  "sf_surface_physics": [1],
  "bl_pbl_physics": [1],
  "cu_physics": [1]
}
```

### WPS Configuration (`wps_config`)

```json
{
  "start_date": "2023-01-01_00:00:00",
  "end_date": "2023-01-02_00:00:00",
  "interval_seconds": 21600,
  "geog_data_res": "default",
  "map_proj": "lambert",
  "ref_lat": -34.0,
  "ref_lon": 18.5,
  "truelat1": -34.0,
  "truelat2": -34.0,
  "stand_lon": 18.5
}
```

## 🌍 Example Configurations

### 1. Simple Test Case

```json
{
  "job_name": "simple_test",
  "queue": "normal",
  "nodes": 2,
  "cores_per_node": 16,
  "memory_per_node": "64GB",
  "walltime": "24:00:00",
  "run_wps": false,
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
    "e_vert": [28]
  }
}
```

### 2. South Africa Regional Case

```json
{
  "job_name": "sa_regional",
  "queue": "normal",
  "nodes": 4,
  "cores_per_node": 32,
  "memory_per_node": "128GB",
  "walltime": "48:00:00",
  "run_wps": true,
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
    "e_vert": [35]
  },
  "wps_config": {
    "start_date": "2023-01-01_00:00:00",
    "end_date": "2023-01-03_00:00:00",
    "interval_seconds": 21600,
    "ref_lat": -34.0,
    "ref_lon": 18.5,
    "truelat1": -34.0,
    "truelat2": -34.0,
    "stand_lon": 18.5
  }
}
```

### 3. High Resolution Urban Case

```json
{
  "job_name": "high_res_urban",
  "queue": "normal",
  "nodes": 8,
  "cores_per_node": 32,
  "memory_per_node": "128GB",
  "walltime": "72:00:00",
  "run_wps": true,
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
    "sf_urban_physics": [1]
  },
  "wps_config": {
    "start_date": "2023-01-01_00:00:00",
    "end_date": "2023-01-04_00:00:00",
    "interval_seconds": 21600,
    "geog_data_res": "30s",
    "ref_lat": -34.0,
    "ref_lon": 18.5
  }
}
```

## 🐍 Python Client Examples

### Basic WRF Job Submission

```python
import requests
import json

# API configuration
BASE_URL = "http://localhost:8080"
WRF_API = f"{BASE_URL}/api/v1/wrf"

def submit_wrf_job(job_config):
    """Submit a WRF job"""
    response = requests.post(f"{WRF_API}/jobs", json=job_config)
    
    if response.status_code == 200:
        result = response.json()
        if result["success"]:
            print(f"Job submitted successfully: {result['job_id']}")
            return result["job_id"]
        else:
            print(f"Job submission failed: {result['error']}")
    else:
        print(f"HTTP error: {response.status_code}")
    
    return None

def monitor_wrf_job(job_id, max_checks=10):
    """Monitor a WRF job"""
    for i in range(max_checks):
        response = requests.get(f"{WRF_API}/jobs/{job_id}")
        
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                status = data["status"]
                print(f"Check {i+1}: Job {job_id} status = {status}")
                
                if status in ["COMPLETED", "FAILED", "CANCELLED"]:
                    return status
        
        time.sleep(30)  # Wait 30 seconds
    
    return "TIMEOUT"

# Example usage
job_config = {
    "job_name": "python_wrf_test",
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
        "e_sn": [61]
    }
}

# Submit and monitor job
job_id = submit_wrf_job(job_config)
if job_id:
    status = monitor_wrf_job(job_id)
    print(f"Final status: {status}")
```

### Advanced WRF Management

```python
import requests
import time

class WRFClient:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.wrf_api = f"{base_url}/api/v1/wrf"
    
    def get_wrf_info(self):
        """Get WRF installation information"""
        response = requests.get(f"{self.wrf_api}/info")
        return response.json() if response.status_code == 200 else None
    
    def list_jobs(self):
        """List all WRF jobs"""
        response = requests.get(f"{self.wrf_api}/jobs")
        return response.json() if response.status_code == 200 else None
    
    def submit_job(self, job_config):
        """Submit a WRF job"""
        response = requests.post(f"{self.wrf_api}/jobs", json=job_config)
        return response.json() if response.status_code == 200 else None
    
    def get_job_status(self, job_id):
        """Get job status"""
        response = requests.get(f"{self.wrf_api}/jobs/{job_id}")
        return response.json() if response.status_code == 200 else None
    
    def cancel_job(self, job_id):
        """Cancel a job"""
        response = requests.delete(f"{self.wrf_api}/jobs/{job_id}")
        return response.json() if response.status_code == 200 else None
    
    def get_job_logs(self, job_id):
        """Get job logs"""
        response = requests.get(f"{self.wrf_api}/jobs/{job_id}/logs")
        return response.json() if response.status_code == 200 else None
    
    def validate_config(self, wrf_config):
        """Validate WRF configuration"""
        response = requests.post(f"{self.wrf_api}/validate-config", json=wrf_config)
        return response.json() if response.status_code == 200 else None

# Usage example
client = WRFClient()

# Get WRF info
info = client.get_wrf_info()
print("WRF Info:", info)

# List existing jobs
jobs = client.list_jobs()
print("Existing jobs:", jobs)

# Submit a job
job_config = {
    "job_name": "client_test",
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
        "e_sn": [61]
    }
}

result = client.submit_job(job_config)
if result and result["success"]:
    job_id = result["job_id"]
    print(f"Job submitted: {job_id}")
    
    # Monitor job
    while True:
        status_data = client.get_job_status(job_id)
        if status_data and status_data["success"]:
            status = status_data["status"]
            print(f"Job status: {status}")
            
            if status in ["COMPLETED", "FAILED", "CANCELLED"]:
                # Get logs
                logs = client.get_job_logs(job_id)
                print("Job logs:", logs)
                break
        
        time.sleep(30)
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Job Submission Fails

**Problem**: Job submission returns error
**Solutions**:
- Check WRF installation: `curl http://localhost:8080/api/v1/wrf/info`
- Validate configuration: Use `/api/v1/wrf/validate-config`
- Check cluster resources: Ensure sufficient nodes/cores available

#### 2. WPS Preprocessing Fails

**Problem**: WPS jobs fail during preprocessing
**Solutions**:
- Verify WPS data paths in configuration
- Check geographic data availability
- Ensure proper namelist.wps configuration

#### 3. WRF Model Crashes

**Problem**: WRF model crashes during execution
**Solutions**:
- Check job logs: `curl http://localhost:8080/api/v1/wrf/jobs/{job_id}/logs`
- Verify namelist.input configuration
- Check resource allocation (memory, cores)

#### 4. Performance Issues

**Problem**: WRF jobs run slowly or inefficiently
**Solutions**:
- Optimize domain size and resolution
- Use appropriate physics schemes
- Adjust resource allocation

### Debug Commands

```bash
# Check WRF installation
curl http://localhost:8080/api/v1/wrf/info

# Validate configuration
curl -X POST http://localhost:8080/api/v1/wrf/validate-config \
  -H "Content-Type: application/json" \
  -d '{"run_hours": 24, "time_step": 180}'

# Get job logs
curl http://localhost:8080/api/v1/wrf/jobs/{job_id}/logs

# List all WRF jobs
curl http://localhost:8080/api/v1/wrf/jobs
```

## 📊 Best Practices

### Resource Allocation

1. **Node Selection**: Choose appropriate number of nodes based on domain size
2. **Memory**: Allocate sufficient memory (64GB-128GB per node for WRF)
3. **Wall Time**: Estimate runtime and add buffer time
4. **Queue Selection**: Use appropriate queue (normal, long, debug)

### Configuration Optimization

1. **Time Step**: Use appropriate time step (typically 6x grid spacing)
2. **Domain Size**: Balance resolution with computational cost
3. **Physics Schemes**: Choose schemes appropriate for your application
4. **Output Frequency**: Set reasonable history intervals

### Monitoring and Management

1. **Regular Status Checks**: Monitor job progress regularly
2. **Log Analysis**: Check logs for errors and warnings
3. **Resource Monitoring**: Monitor cluster resource usage
4. **Cleanup**: Remove completed jobs and output files

## 🔗 Integration with Other Tools

### Workflow Integration

The WRF API can be integrated with:
- **Workflow managers** (e.g., Apache Airflow, Nextflow)
- **Data processing pipelines**
- **Visualization tools**
- **Post-processing scripts**

### Example Workflow

```python
# Complete WRF workflow example
def run_wrf_workflow(config):
    # 1. Submit WRF job
    job_id = submit_wrf_job(config)
    
    # 2. Monitor until completion
    status = monitor_job(job_id)
    
    # 3. Get results if successful
    if status == "COMPLETED":
        logs = get_job_logs(job_id)
        # Process results
        process_wrf_output(job_id)
    
    return status
```

## 📚 Additional Resources

### WRF Documentation
- [WRF User's Guide](https://www2.mmm.ucar.edu/wrf/users/)
- [WRF Physics Options](https://www2.mmm.ucar.edu/wrf/users/docs/user_guide_V4/phys_schemes.html)
- [WRF Namelist Options](https://www2.mmm.ucar.edu/wrf/users/docs/user_guide_V4/namelist.html)

### CHPC Resources
- [Lengau Cluster Guide](https://wiki.chpc.ac.za/lengau)
- [PBS User Guide](https://wiki.chpc.ac.za/pbs)
- [Module System](https://wiki.chpc.ac.za/modules)

### API Documentation
- Interactive API docs: `http://localhost:8080/docs`
- OpenAPI specification: `http://localhost:8080/openapi.json`

---

**For support and questions, contact**: msovara@chpc.ac.za
