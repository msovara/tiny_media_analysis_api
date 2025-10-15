from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
from .job_service import JobService
from .models import (
    JobSubmissionRequest, JobSubmissionResponse, JobStatusResponse,
    JobListResponse, ClusterInfoResponse, JobCancelResponse, JobLogResponse
)

# Initialize job service
job_service = JobService()

# Create router
router = APIRouter()


@router.post("/jobs", response_model=JobSubmissionResponse)
async def submit_job(request: JobSubmissionRequest):
    """
    Submit a new job to the Lengau cluster.
    
    - **job_name**: Name of the job
    - **script_content**: The actual script content to execute
    - **queue**: Queue to submit to (default: normal)
    - **nodes**: Number of nodes to request (default: 1)
    - **cores_per_node**: Number of cores per node (default: 1)
    - **memory_per_node**: Memory per node (default: 4GB)
    - **walltime**: Maximum wall time (default: 01:00:00)
    - **email**: Email for notifications (optional)
    - **email_events**: Email notification events (default: END)
    - **working_directory**: Working directory for the job (optional)
    - **environment_variables**: Environment variables to set (optional)
    - **dependencies**: Job dependencies (optional)
    - **modules**: Modules to load (optional)
    """
    try:
        result = job_service.submit_job(request)
        return JobSubmissionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/jobs", response_model=JobListResponse)
async def list_jobs(
    user: Optional[str] = Query(None, description="Filter by username")
):
    """
    List all jobs for the current user or a specific user.
    
    - **user**: Username to filter jobs by (optional)
    """
    try:
        jobs = job_service.list_jobs(user)
        return JobListResponse(jobs=jobs, total_jobs=len(jobs))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(
    job_id: str = Path(..., description="Job ID to get status for")
):
    """
    Get the status of a specific job.
    
    - **job_id**: The job ID to query
    """
    try:
        return job_service.get_job_status(job_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/jobs/{job_id}", response_model=JobCancelResponse)
async def cancel_job(
    job_id: str = Path(..., description="Job ID to cancel")
):
    """
    Cancel a running or pending job.
    
    - **job_id**: The job ID to cancel
    """
    try:
        result = job_service.cancel_job(job_id)
        return JobCancelResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/jobs/{job_id}/logs", response_model=JobLogResponse)
async def get_job_logs(
    job_id: str = Path(..., description="Job ID to get logs for")
):
    """
    Get the logs (stdout, stderr) for a specific job.
    
    - **job_id**: The job ID to get logs for
    """
    try:
        return job_service.get_job_logs(job_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/cluster/info", response_model=ClusterInfoResponse)
async def get_cluster_info():
    """
    Get information about the Lengau cluster.
    
    Returns cluster configuration including available queues,
    resource limits, and default modules.
    """
    try:
        return job_service.get_cluster_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cluster/queues")
async def get_available_queues():
    """
    Get list of available queues on the cluster.
    """
    try:
        cluster_info = job_service.get_cluster_info()
        return {"queues": cluster_info.available_queues}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cluster/modules")
async def get_default_modules():
    """
    Get list of default modules available on the cluster.
    """
    try:
        cluster_info = job_service.get_cluster_info()
        return {"modules": cluster_info.default_modules}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/jobs/{job_id}/hold")
async def hold_job(
    job_id: str = Path(..., description="Job ID to hold")
):
    """
    Hold a job (prevent it from running).
    
    - **job_id**: The job ID to hold
    """
    try:
        # This would require implementing qhold command
        raise HTTPException(status_code=501, detail="Hold functionality not yet implemented")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/jobs/{job_id}/release")
async def release_job(
    job_id: str = Path(..., description="Job ID to release")
):
    """
    Release a held job.
    
    - **job_id**: The job ID to release
    """
    try:
        # This would require implementing qrls command
        raise HTTPException(status_code=501, detail="Release functionality not yet implemented")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



































