from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from enum import Enum


class Article(BaseModel):
    """Article model representing a news article."""
    id: int
    title: str
    body: str
    source: str
    date: str
    url: Optional[str] = ""
    tags: Optional[List[str]] = []


class ArticleResponse(BaseModel):
    """Response model for articles with tags."""
    id: int
    title: str
    body: str
    source: str
    date: str
    url: Optional[str] = ""
    tags: List[str]


class StatsResponse(BaseModel):
    """Response model for statistics."""
    tags: dict[str, int]
    sources: dict[str, int]
    total_articles: int


class JobStatus(str, Enum):
    """Job status enumeration."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    SUSPENDED = "SUSPENDED"


class JobSubmissionRequest(BaseModel):
    """Request model for job submission."""
    job_name: str
    script_content: str
    queue: Optional[str] = "normal"
    nodes: Optional[int] = 1
    cores_per_node: Optional[int] = 1
    memory_per_node: Optional[str] = "4GB"
    walltime: Optional[str] = "01:00:00"
    email: Optional[str] = None
    email_events: Optional[str] = "END"
    working_directory: Optional[str] = None
    environment_variables: Optional[Dict[str, str]] = {}
    dependencies: Optional[List[str]] = []
    modules: Optional[List[str]] = []


class JobSubmissionResponse(BaseModel):
    """Response model for job submission."""
    job_id: str
    job_name: str
    status: JobStatus
    submission_time: datetime
    message: str


class JobStatusResponse(BaseModel):
    """Response model for job status."""
    job_id: str
    job_name: str
    status: JobStatus
    queue: str
    nodes: int
    cores_per_node: int
    memory_per_node: str
    walltime: str
    submit_time: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    exit_code: Optional[int] = None
    working_directory: Optional[str] = None
    output_file: Optional[str] = None
    error_file: Optional[str] = None


class JobListResponse(BaseModel):
    """Response model for job listing."""
    jobs: List[JobStatusResponse]
    total_jobs: int


class ClusterInfoResponse(BaseModel):
    """Response model for cluster information."""
    cluster_name: str
    available_queues: List[str]
    max_nodes: int
    max_cores_per_node: int
    max_memory_per_node: str
    max_walltime: str
    default_modules: List[str]


class JobCancelResponse(BaseModel):
    """Response model for job cancellation."""
    job_id: str
    status: JobStatus
    message: str


class JobLogResponse(BaseModel):
    """Response model for job logs."""
    job_id: str
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    log_file: Optional[str] = None 