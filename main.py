#!/usr/bin/env python3
"""
Main FastAPI Application for Lengau Cluster Job Management
Includes both general job management and WRF-specific endpoints
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Import the job service and models directly
from src.job_service import JobService
from src.wrf_service import WRFService
from src.models import (
    JobStatus, JobSubmissionRequest, JobSubmissionResponse,
    JobStatusResponse, JobListResponse, ClusterInfoResponse,
    JobCancelResponse, JobLogResponse
)

# Import WRF API router
from src.wrf_api import wrf_router

app = FastAPI(
    title="Lengau Cluster Job Management API",
    description="A REST API for managing job submissions on the Lengau cluster at CHPC, including WRF simulations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for web dashboard
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize services
job_service = JobService()
wrf_service = WRFService()

# Include WRF router
app.include_router(wrf_router)

# General job management endpoints
@app.post("/api/v1/cluster/jobs", response_model=JobSubmissionResponse)
async def submit_job(request: JobSubmissionRequest):
    """Submit a new job to the Lengau cluster."""
    try:
        result = job_service.submit_job(request)
        return JobSubmissionResponse(**result)
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/cluster/jobs", response_model=JobListResponse)
async def list_jobs():
    """List all jobs for the current user."""
    try:
        result = job_service.list_jobs()
        return JobListResponse(**result)
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/cluster/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get the status of a specific job."""
    try:
        result = job_service.get_job_status(job_id)
        return JobStatusResponse(**result)
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/api/v1/cluster/jobs/{job_id}", response_model=JobCancelResponse)
async def cancel_job(job_id: str):
    """Cancel a specific job."""
    try:
        result = job_service.cancel_job(job_id)
        return JobCancelResponse(**result)
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/cluster/jobs/{job_id}/logs", response_model=JobLogResponse)
async def get_job_logs(job_id: str):
    """Get logs for a specific job."""
    try:
        result = job_service.get_job_logs(job_id)
        return JobLogResponse(**result)
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/v1/cluster/info", response_model=ClusterInfoResponse)
async def get_cluster_info():
    """Get general cluster information."""
    try:
        result = job_service.get_cluster_info()
        return ClusterInfoResponse(**result)
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/cluster/queues")
async def get_queues():
    """Get available PBS queues."""
    try:
        result = job_service.get_queues()
        return result
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/cluster/modules")
async def get_modules():
    """Get available software modules."""
    try:
        result = job_service.get_modules()
        return result
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint with API information
@app.get("/")
async def root():
    return {
        "message": "Lengau Cluster Job Management API",
        "version": "1.0.0",
        "endpoints": {
            "cluster_management": {
                "submit_job": "/api/v1/cluster/jobs",
                "list_jobs": "/api/v1/cluster/jobs",
                "job_status": "/api/v1/cluster/jobs/{job_id}",
                "cancel_job": "/api/v1/cluster/jobs/{job_id}",
                "job_logs": "/api/v1/cluster/jobs/{job_id}/logs",
                "cluster_info": "/api/v1/cluster/info",
                "queues": "/api/v1/cluster/queues",
                "modules": "/api/v1/cluster/modules"
            },
            "wrf_management": {
                "wrf_info": "/api/v1/wrf/info",
                "submit_wrf_job": "/api/v1/wrf/jobs",
                "list_wrf_jobs": "/api/v1/wrf/jobs",
                "wrf_job_status": "/api/v1/wrf/jobs/{job_id}",
                "cancel_wrf_job": "/api/v1/wrf/jobs/{job_id}",
                "wrf_job_logs": "/api/v1/wrf/jobs/{job_id}/logs",
                "namelist_template": "/api/v1/wrf/templates/namelist",
                "wps_namelist_template": "/api/v1/wrf/templates/wps-namelist",
                "validate_config": "/api/v1/wrf/validate-config",
                "examples": "/api/v1/wrf/examples"
            },
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Web dashboard endpoint
@app.get("/dashboard")
async def dashboard():
    """Serve the WRF API web dashboard."""
    if os.path.exists("static/wrf_dashboard.html"):
        return FileResponse("static/wrf_dashboard.html")
    else:
        return {"error": "Dashboard not found. Please ensure static/wrf_dashboard.html exists."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
