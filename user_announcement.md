# 📢 Lengau Cluster Job Management API - Now Available!

## 🎉 **New Service Announcement**

We're excited to announce that the **Lengau Cluster Job Management API** is now available for all users! This new service provides a modern, programmatic interface for managing your computational jobs on the cluster.

## 🚀 **What's New**

### **Web-Based Job Management**
- Submit jobs via REST API
- Monitor job status in real-time
- List and manage all your jobs
- Access cluster information
- Interactive web documentation

### **Easy Access**
- **API URL**: `http://login2.lengau.chpc.ac.za:8080`
- **Interactive Docs**: `http://login2.lengau.chpc.ac.za:8080/docs`
- **No SSH tunnel required** - direct access from cluster

## 📋 **Quick Start**

### **1. Test the API**
```bash
# Health check
curl http://login2.lengau.chpc.ac.za:8080/health

# List your jobs
curl http://login2.lengau.chpc.ac.za:8080/api/v1/cluster/jobs
```

### **2. Submit Your First Job**
```bash
curl -X POST http://login2.lengau.chpc.ac.za:8080/api/v1/cluster/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "job_name": "my_first_api_job",
    "script_content": "#!/bin/bash\necho \"Hello from API!\"\ndate\nhostname",
    "queue": "normal",
    "nodes": 1,
    "cores_per_node": 1,
    "memory_per_node": "4GB",
    "walltime": "00:10:00"
  }'
```

### **3. Use Interactive Documentation**
Open your browser and go to: **http://login2.lengau.chpc.ac.za:8080/docs**

This provides a user-friendly interface where you can:
- Test all endpoints interactively
- See examples and documentation
- Try different parameters
- View API schemas

## 🐍 **Python Client Example**

```python
import requests

# API base URL
BASE_URL = "http://login2.lengau.chpc.ac.za:8080"

# Submit a job
job_data = {
    "job_name": "python_test",
    "script_content": "#!/bin/bash\necho 'Python API test'\npython --version",
    "queue": "normal",
    "nodes": 1,
    "cores_per_node": 1,
    "memory_per_node": "4GB",
    "walltime": "00:10:00"
}

response = requests.post(f"{BASE_URL}/api/v1/cluster/jobs", json=job_data)
job_id = response.json()["job_id"]
print(f"Submitted job: {job_id}")

# Monitor job status
status_response = requests.get(f"{BASE_URL}/api/v1/cluster/jobs/{job_id}")
print(f"Job status: {status_response.json()['status']}")
```

## 📡 **Available Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/docs` | GET | Interactive documentation |
| `/api/v1/cluster/jobs` | POST | Submit new job |
| `/api/v1/cluster/jobs` | GET | List all jobs |
| `/api/v1/cluster/jobs/{job_id}` | GET | Get job status |
| `/api/v1/cluster/jobs/{job_id}` | DELETE | Cancel job |
| `/api/v1/cluster/jobs/{job_id}/logs` | GET | Get job logs |
| `/api/v1/cluster/info` | GET | Cluster information |
| `/api/v1/cluster/queues` | GET | Available queues |
| `/api/v1/cluster/modules` | GET | Available modules |

## 🌪️ **Special Features**

### **ARWpost Integration**
Submit ARWpost processing jobs with pre-configured settings:

```bash
curl -X POST http://login2.lengau.chpc.ac.za:8080/api/v1/cluster/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "job_name": "arwpost_analysis",
    "script_content": "#!/bin/bash\nmodule load wrf/4.3.3\narwpost.exe",
    "queue": "normal",
    "nodes": 2,
    "cores_per_node": 16,
    "memory_per_node": "64GB",
    "walltime": "02:00:00"
  }'
```

### **WRF Model Jobs**
Submit WRF simulations with optimized resource allocation:

```bash
curl -X POST http://login2.lengau.chpc.ac.za:8080/api/v1/cluster/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "job_name": "wrf_simulation",
    "script_content": "#!/bin/bash\nmodule load wrf/4.3.3\nmpirun -np 32 wrf.exe",
    "queue": "normal",
    "nodes": 4,
    "cores_per_node": 32,
    "memory_per_node": "128GB",
    "walltime": "24:00:00"
  }'
```

## 🔧 **Advanced Usage**

### **Job Dependencies**
Submit jobs that depend on other jobs:

```json
{
  "job_name": "dependent_job",
  "script_content": "#!/bin/bash\necho 'This runs after job 12345'",
  "dependencies": ["12345.sched01"],
  "queue": "normal"
}
```

### **Environment Variables**
Set custom environment variables:

```json
{
  "job_name": "custom_env_job",
  "script_content": "#!/bin/bash\necho $CUSTOM_VAR",
  "environment_variables": {
    "CUSTOM_VAR": "Hello World",
    "OMP_NUM_THREADS": "4"
  }
}
```

### **Module Loading**
Automatically load required modules:

```json
{
  "job_name": "module_job",
  "script_content": "#!/bin/bash\npython my_script.py",
  "modules": ["python/3.9.0", "numpy/1.21.0"]
}
```

## 🛡️ **Security & Best Practices**

### **Responsible Usage**
- Monitor your job submissions
- Clean up completed jobs when possible
- Don't submit malicious scripts
- Respect cluster resource limits

### **Resource Management**
- Use appropriate queue and resource requests
- Monitor job status and cancel if needed
- Check job logs for errors

## 🆘 **Support & Troubleshooting**

### **Common Issues**

1. **API not responding**:
   ```bash
   curl http://login2.lengau.chpc.ac.za:8080/health
   ```

2. **Job submission failed**:
   - Check script syntax
   - Verify queue and resource limits
   - Review job logs

3. **Permission denied**:
   - Ensure you're on the cluster
   - Check if you have PBS access

### **Getting Help**

- **Interactive Docs**: http://login2.lengau.chpc.ac.za:8080/docs
- **API Status**: http://login2.lengau.chpc.ac.za:8080/proxy/status
- **Contact**: msovara@chpc.ac.za

## 📚 **Documentation & Examples**

- **Full Documentation**: See the project README
- **Examples**: Check the `examples/` directory
- **Tutorial**: Use the interactive docs at `/docs`

## 🎯 **Benefits**

### **For Users**
- **No more SSH tunnels** - direct web access
- **Interactive documentation** - learn as you go
- **Programmatic access** - integrate with your workflows
- **Real-time monitoring** - track job progress
- **Easy job management** - submit, monitor, cancel

### **For Workflows**
- **Automation** - script your job submissions
- **Integration** - connect to other tools
- **Monitoring** - track multiple jobs
- **Error handling** - programmatic error detection

## 🚀 **What's Next**

This is just the beginning! Future enhancements may include:
- User authentication and quotas
- Job templates and workflows
- Advanced monitoring and analytics
- Integration with other cluster services

## 📞 **Feedback**

We'd love to hear your feedback! Please let us know:
- What features you'd like to see
- Any issues you encounter
- How you're using the API
- Suggestions for improvements

---

**Happy Computing! 🎉**

*The Lengau Cluster Team*
*msovara@chpc.ac.za*
