import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from src.main import app
from src.models import JobStatus, JobSubmissionRequest

client = TestClient(app)


class TestJobSubmission:
    """Test job submission endpoints."""
    
    def test_submit_job_success(self):
        """Test successful job submission."""
        job_data = {
            "job_name": "test_job",
            "script_content": "echo 'Hello World'",
            "queue": "normal",
            "nodes": 1,
            "cores_per_node": 1,
            "memory_per_node": "4GB",
            "walltime": "00:10:00"
        }
        
        with patch('src.job_service.JobService.submit_job') as mock_submit:
            mock_submit.return_value = {
                "job_id": "12345",
                "job_name": "test_job",
                "status": JobStatus.PENDING,
                "submission_time": "2024-01-01T00:00:00",
                "message": "Job submitted successfully"
            }
            
            response = client.post("/api/v1/cluster/jobs", json=job_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["job_id"] == "12345"
            assert data["job_name"] == "test_job"
            assert data["status"] == "PENDING"
    
    def test_submit_job_missing_required_fields(self):
        """Test job submission with missing required fields."""
        job_data = {
            "queue": "normal"
            # Missing job_name and script_content
        }
        
        response = client.post("/api/v1/cluster/jobs", json=job_data)
        assert response.status_code == 422  # Validation error
    
    def test_submit_job_service_error(self):
        """Test job submission when service raises an error."""
        job_data = {
            "job_name": "test_job",
            "script_content": "echo 'Hello World'"
        }
        
        with patch('src.job_service.JobService.submit_job') as mock_submit:
            mock_submit.side_effect = Exception("Submission failed")
            
            response = client.post("/api/v1/cluster/jobs", json=job_data)
            assert response.status_code == 400
            assert "Submission failed" in response.json()["detail"]


class TestJobStatus:
    """Test job status endpoints."""
    
    def test_get_job_status_success(self):
        """Test successful job status retrieval."""
        with patch('src.job_service.JobService.get_job_status') as mock_status:
            mock_status.return_value = {
                "job_id": "12345",
                "job_name": "test_job",
                "status": JobStatus.RUNNING,
                "queue": "normal",
                "nodes": 1,
                "cores_per_node": 1,
                "memory_per_node": "4GB",
                "walltime": "01:00:00",
                "submit_time": "2024-01-01T00:00:00",
                "start_time": "2024-01-01T00:05:00",
                "end_time": None,
                "exit_code": None,
                "working_directory": "/home/user",
                "output_file": "/home/user/test_job.out",
                "error_file": "/home/user/test_job.err"
            }
            
            response = client.get("/api/v1/cluster/jobs/12345")
            assert response.status_code == 200
            data = response.json()
            assert data["job_id"] == "12345"
            assert data["status"] == "RUNNING"
    
    def test_get_job_status_not_found(self):
        """Test job status retrieval for non-existent job."""
        with patch('src.job_service.JobService.get_job_status') as mock_status:
            mock_status.side_effect = Exception("Job not found")
            
            response = client.get("/api/v1/cluster/jobs/99999")
            assert response.status_code == 404


class TestJobListing:
    """Test job listing endpoints."""
    
    def test_list_jobs_success(self):
        """Test successful job listing."""
        with patch('src.job_service.JobService.list_jobs') as mock_list:
            mock_list.return_value = [
                {
                    "job_id": "12345",
                    "job_name": "test_job_1",
                    "status": JobStatus.RUNNING,
                    "queue": "normal",
                    "nodes": 1,
                    "cores_per_node": 1,
                    "memory_per_node": "4GB",
                    "walltime": "01:00:00"
                },
                {
                    "job_id": "12346",
                    "job_name": "test_job_2",
                    "status": JobStatus.COMPLETED,
                    "queue": "normal",
                    "nodes": 1,
                    "cores_per_node": 1,
                    "memory_per_node": "4GB",
                    "walltime": "01:00:00"
                }
            ]
            
            response = client.get("/api/v1/cluster/jobs")
            assert response.status_code == 200
            data = response.json()
            assert data["total_jobs"] == 2
            assert len(data["jobs"]) == 2
            assert data["jobs"][0]["job_id"] == "12345"
            assert data["jobs"][1]["job_id"] == "12346"
    
    def test_list_jobs_with_user_filter(self):
        """Test job listing with user filter."""
        with patch('src.job_service.JobService.list_jobs') as mock_list:
            mock_list.return_value = []
            
            response = client.get("/api/v1/cluster/jobs?user=testuser")
            assert response.status_code == 200
            mock_list.assert_called_once_with("testuser")


class TestJobCancellation:
    """Test job cancellation endpoints."""
    
    def test_cancel_job_success(self):
        """Test successful job cancellation."""
        with patch('src.job_service.JobService.cancel_job') as mock_cancel:
            mock_cancel.return_value = {
                "job_id": "12345",
                "status": JobStatus.CANCELLED,
                "message": "Job cancelled successfully"
            }
            
            response = client.delete("/api/v1/cluster/jobs/12345")
            assert response.status_code == 200
            data = response.json()
            assert data["job_id"] == "12345"
            assert data["status"] == "CANCELLED"
    
    def test_cancel_job_error(self):
        """Test job cancellation error."""
        with patch('src.job_service.JobService.cancel_job') as mock_cancel:
            mock_cancel.side_effect = Exception("Cannot cancel job")
            
            response = client.delete("/api/v1/cluster/jobs/12345")
            assert response.status_code == 400
            assert "Cannot cancel job" in response.json()["detail"]


class TestJobLogs:
    """Test job logs endpoints."""
    
    def test_get_job_logs_success(self):
        """Test successful job logs retrieval."""
        with patch('src.job_service.JobService.get_job_logs') as mock_logs:
            mock_logs.return_value = {
                "job_id": "12345",
                "stdout": "Hello World\nJob completed successfully",
                "stderr": "",
                "log_file": "/home/user/test_job.log"
            }
            
            response = client.get("/api/v1/cluster/jobs/12345/logs")
            assert response.status_code == 200
            data = response.json()
            assert data["job_id"] == "12345"
            assert "Hello World" in data["stdout"]
    
    def test_get_job_logs_not_found(self):
        """Test job logs retrieval for non-existent job."""
        with patch('src.job_service.JobService.get_job_logs') as mock_logs:
            mock_logs.side_effect = Exception("Job not found")
            
            response = client.get("/api/v1/cluster/jobs/99999/logs")
            assert response.status_code == 404


class TestClusterInfo:
    """Test cluster information endpoints."""
    
    def test_get_cluster_info_success(self):
        """Test successful cluster info retrieval."""
        with patch('src.job_service.JobService.get_cluster_info') as mock_info:
            mock_info.return_value = {
                "cluster_name": "Lengau",
                "available_queues": ["normal", "long", "short", "debug"],
                "max_nodes": 1000,
                "max_cores_per_node": 64,
                "max_memory_per_node": "256GB",
                "max_walltime": "168:00:00",
                "default_modules": [
                    "chpc/parallel_studio_xe/16.0.1/2016.1.150",
                    "chpc/netcdf/4.4.3-F/intel/16.0.1"
                ]
            }
            
            response = client.get("/api/v1/cluster/info")
            assert response.status_code == 200
            data = response.json()
            assert data["cluster_name"] == "Lengau"
            assert "normal" in data["available_queues"]
            assert data["max_nodes"] == 1000
    
    def test_get_available_queues(self):
        """Test available queues endpoint."""
        with patch('src.job_service.JobService.get_cluster_info') as mock_info:
            mock_info.return_value = {
                "cluster_name": "Lengau",
                "available_queues": ["normal", "long", "short", "debug"],
                "max_nodes": 1000,
                "max_cores_per_node": 64,
                "max_memory_per_node": "256GB",
                "max_walltime": "168:00:00",
                "default_modules": []
            }
            
            response = client.get("/api/v1/cluster/queues")
            assert response.status_code == 200
            data = response.json()
            assert "queues" in data
            assert "normal" in data["queues"]
    
    def test_get_default_modules(self):
        """Test default modules endpoint."""
        with patch('src.job_service.JobService.get_cluster_info') as mock_info:
            mock_info.return_value = {
                "cluster_name": "Lengau",
                "available_queues": [],
                "max_nodes": 1000,
                "max_cores_per_node": 64,
                "max_memory_per_node": "256GB",
                "max_walltime": "168:00:00",
                "default_modules": [
                    "chpc/parallel_studio_xe/16.0.1/2016.1.150",
                    "chpc/netcdf/4.4.3-F/intel/16.0.1"
                ]
            }
            
            response = client.get("/api/v1/cluster/modules")
            assert response.status_code == 200
            data = response.json()
            assert "modules" in data
            assert "chpc/parallel_studio_xe/16.0.1/2016.1.150" in data["modules"]


class TestJobHoldRelease:
    """Test job hold and release endpoints."""
    
    def test_hold_job_not_implemented(self):
        """Test that hold job endpoint returns not implemented."""
        response = client.post("/api/v1/cluster/jobs/12345/hold")
        assert response.status_code == 501
        assert "not yet implemented" in response.json()["detail"]
    
    def test_release_job_not_implemented(self):
        """Test that release job endpoint returns not implemented."""
        response = client.post("/api/v1/cluster/jobs/12345/release")
        assert response.status_code == 501
        assert "not yet implemented" in response.json()["detail"]


class TestRootEndpoints:
    """Test root application endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "endpoints" in data
        assert "cluster_management" in data["endpoints"]
        assert "media_analysis" in data["endpoints"]
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestJobSubmissionValidation:
    """Test job submission request validation."""
    
    def test_valid_job_submission_request(self):
        """Test that valid job submission request is accepted."""
        request = JobSubmissionRequest(
            job_name="test_job",
            script_content="echo 'Hello World'",
            queue="normal",
            nodes=2,
            cores_per_node=4,
            memory_per_node="8GB",
            walltime="02:00:00",
            email="user@example.com",
            email_events="END",
            working_directory="/home/user",
            environment_variables={"VAR1": "value1"},
            dependencies=["12345"],
            modules=["module1", "module2"]
        )
        
        assert request.job_name == "test_job"
        assert request.script_content == "echo 'Hello World'"
        assert request.queue == "normal"
        assert request.nodes == 2
        assert request.cores_per_node == 4
        assert request.memory_per_node == "8GB"
        assert request.walltime == "02:00:00"
        assert request.email == "user@example.com"
        assert request.email_events == "END"
        assert request.working_directory == "/home/user"
        assert request.environment_variables == {"VAR1": "value1"}
        assert request.dependencies == ["12345"]
        assert request.modules == ["module1", "module2"]
    
    def test_job_submission_request_defaults(self):
        """Test that job submission request uses correct defaults."""
        request = JobSubmissionRequest(
            job_name="test_job",
            script_content="echo 'Hello World'"
        )
        
        assert request.queue == "normal"
        assert request.nodes == 1
        assert request.cores_per_node == 1
        assert request.memory_per_node == "4GB"
        assert request.walltime == "01:00:00"
        assert request.email_events == "END"
        assert request.environment_variables == {}
        assert request.dependencies == []
        assert request.modules == []



































