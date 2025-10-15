import subprocess
import os
import tempfile
import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from .models import (
    JobStatus, JobSubmissionRequest, JobStatusResponse, 
    ClusterInfoResponse, JobLogResponse
)


class JobService:
    """Service class for managing job submissions on Lengau cluster."""
    
    def __init__(self):
        self.cluster_name = "Lengau"
        self.default_queues = ["normal", "long", "short", "debug"]
        self.max_nodes = 1000
        self.max_cores_per_node = 64
        self.max_memory_per_node = "256GB"
        self.max_walltime = "168:00:00"
        self.default_modules = [
            "chpc/parallel_studio_xe/16.0.1/2016.1.150",
            "chpc/netcdf/4.4.3-F/intel/16.0.1",
            "chpc/hdf5/1.8.16/intel/16.0.1"
        ]
    
    def _run_command(self, command: List[str]) -> Tuple[int, str, str]:
        """Run a shell command and return exit code, stdout, and stderr."""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)
    
    def _parse_job_status(self, status_line: str) -> JobStatus:
        """Parse job status from PBS/SLURM output."""
        status_line = status_line.upper()
        if "Q" in status_line or "PENDING" in status_line:
            return JobStatus.PENDING
        elif "R" in status_line or "RUNNING" in status_line:
            return JobStatus.RUNNING
        elif "C" in status_line or "COMPLETED" in status_line:
            return JobStatus.COMPLETED
        elif "F" in status_line or "FAILED" in status_line:
            return JobStatus.FAILED
        elif "X" in status_line or "CANCELLED" in status_line:
            return JobStatus.CANCELLED
        elif "S" in status_line or "SUSPENDED" in status_line:
            return JobStatus.SUSPENDED
        else:
            return JobStatus.PENDING
    
    def _create_job_script(self, request: JobSubmissionRequest) -> str:
        """Create a PBS job script from the request."""
        script_lines = [
            "#!/bin/bash",
            f"#PBS -N {request.job_name}",
            f"#PBS -q {request.queue}",
            f"#PBS -l nodes={request.nodes}:ppn={request.cores_per_node}",
            f"#PBS -l mem={request.memory_per_node}",
            f"#PBS -l walltime={request.walltime}",
        ]
        
        # Add email notifications if specified
        if request.email:
            script_lines.append(f"#PBS -M {request.email}")
            script_lines.append(f"#PBS -m {request.email_events}")
        
        # Add working directory
        if request.working_directory:
            script_lines.append(f"#PBS -d {request.working_directory}")
        
        # Add job dependencies
        if request.dependencies:
            script_lines.append(f"#PBS -W depend=afterok:{':'.join(request.dependencies)}")
        
        # Add output and error files
        script_lines.extend([
            f"#PBS -o $PBS_O_WORKDIR/{request.job_name}.out",
            f"#PBS -e $PBS_O_WORKDIR/{request.job_name}.err"
        ])
        
        # Add environment variables
        for key, value in request.environment_variables.items():
            script_lines.append(f"export {key}={value}")
        
        # Add module loads
        for module in request.modules:
            script_lines.append(f"module load {module}")
        
        # Add the actual script content
        script_lines.append("")
        script_lines.append(request.script_content)
        
        return "\n".join(script_lines)
    
    def submit_job(self, request: JobSubmissionRequest) -> Dict[str, any]:
        """Submit a job to the cluster."""
        try:
            # Create job script
            script_content = self._create_job_script(request)
            
            # Write script to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.pbs', delete=False) as f:
                f.write(script_content)
                script_path = f.name
            
            # Submit job using qsub
            exit_code, stdout, stderr = self._run_command(["qsub", script_path])
            
            # Clean up temporary file
            os.unlink(script_path)
            
            if exit_code == 0:
                # Extract job ID from output
                job_id_match = re.search(r'(\d+)', stdout.strip())
                if job_id_match:
                    job_id = job_id_match.group(1)
                    return {
                        "job_id": job_id,
                        "job_name": request.job_name,
                        "status": JobStatus.PENDING,
                        "submission_time": datetime.now(),
                        "message": f"Job submitted successfully with ID: {job_id}"
                    }
                else:
                    raise Exception("Could not extract job ID from submission output")
            else:
                raise Exception(f"Job submission failed: {stderr}")
                
        except Exception as e:
            raise Exception(f"Failed to submit job: {str(e)}")
    
    def get_job_status(self, job_id: str) -> JobStatusResponse:
        """Get the status of a specific job."""
        try:
            # Get job details using qstat
            exit_code, stdout, stderr = self._run_command(["qstat", "-f", job_id])
            
            if exit_code != 0:
                raise Exception(f"Failed to get job status: {stderr}")
            
            # Parse qstat output
            job_info = self._parse_qstat_output(stdout)
            
            return JobStatusResponse(
                job_id=job_id,
                job_name=job_info.get("Job_Name", "Unknown"),
                status=self._parse_job_status(job_info.get("job_state", "Q")),
                queue=job_info.get("queue", "normal"),
                nodes=int(job_info.get("Resource_List.nodes", "1").split(":")[0]),
                cores_per_node=int(job_info.get("Resource_List.ppn", "1")),
                memory_per_node=job_info.get("Resource_List.mem", "4GB"),
                walltime=job_info.get("Resource_List.walltime", "01:00:00"),
                submit_time=self._parse_datetime(job_info.get("ctime")),
                start_time=self._parse_datetime(job_info.get("start_time")),
                end_time=self._parse_datetime(job_info.get("end_time")),
                exit_code=job_info.get("Exit_status"),
                working_directory=job_info.get("PBS_O_WORKDIR"),
                output_file=job_info.get("Output_Path"),
                error_file=job_info.get("Error_Path")
            )
            
        except Exception as e:
            raise Exception(f"Failed to get job status: {str(e)}")
    
    def _parse_qstat_output(self, output: str) -> Dict[str, str]:
        """Parse qstat -f output into a dictionary."""
        job_info = {}
        current_key = None
        
        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Check if this is a key-value pair
            if '=' in line:
                key, value = line.split('=', 1)
                current_key = key.strip()
                job_info[current_key] = value.strip()
            elif current_key and line:
                # Multi-line value
                job_info[current_key] += " " + line
        
        return job_info
    
    def _parse_datetime(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse datetime string from PBS output."""
        if not date_str:
            return None
        
        try:
            # PBS uses different date formats, try common ones
            formats = [
                "%a %b %d %H:%M:%S %Y",
                "%Y-%m-%d %H:%M:%S",
                "%m/%d/%Y %H:%M:%S"
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            return None
        except Exception:
            return None
    
    def list_jobs(self, user: Optional[str] = None) -> List[JobStatusResponse]:
        """List all jobs for a user."""
        try:
            command = ["qstat", "-u", user] if user else ["qstat"]
            exit_code, stdout, stderr = self._run_command(command)
            
            if exit_code != 0:
                raise Exception(f"Failed to list jobs: {stderr}")
            
            jobs = []
            lines = stdout.strip().split('\n')
            
            # Skip header lines
            for line in lines[2:]:  # Skip first two header lines
                if line.strip():
                    job_data = self._parse_job_line(line)
                    if job_data:
                        jobs.append(job_data)
            
            return jobs
            
        except Exception as e:
            raise Exception(f"Failed to list jobs: {str(e)}")
    
    def _parse_job_line(self, line: str) -> Optional[JobStatusResponse]:
        """Parse a single job line from qstat output."""
        try:
            parts = line.split()
            if len(parts) < 6:
                return None
            
            job_id = parts[0]
            username = parts[1]
            queue = parts[2]
            job_name = parts[3]
            status = parts[4]
            
            return JobStatusResponse(
                job_id=job_id,
                job_name=job_name,
                status=self._parse_job_status(status),
                queue=queue,
                nodes=1,  # Default values, would need qstat -f for details
                cores_per_node=1,
                memory_per_node="4GB",
                walltime="01:00:00"
            )
        except Exception:
            return None
    
    def cancel_job(self, job_id: str) -> Dict[str, any]:
        """Cancel a job."""
        try:
            exit_code, stdout, stderr = self._run_command(["qdel", job_id])
            
            if exit_code == 0:
                return {
                    "job_id": job_id,
                    "status": JobStatus.CANCELLED,
                    "message": f"Job {job_id} cancelled successfully"
                }
            else:
                raise Exception(f"Failed to cancel job: {stderr}")
                
        except Exception as e:
            raise Exception(f"Failed to cancel job: {str(e)}")
    
    def get_job_logs(self, job_id: str) -> JobLogResponse:
        """Get job logs (stdout, stderr)."""
        try:
            # Get job status to find log file paths
            job_status = self.get_job_status(job_id)
            
            logs = JobLogResponse(job_id=job_id)
            
            # Read output file if it exists
            if job_status.output_file and os.path.exists(job_status.output_file):
                with open(job_status.output_file, 'r') as f:
                    logs.stdout = f.read()
            
            # Read error file if it exists
            if job_status.error_file and os.path.exists(job_status.error_file):
                with open(job_status.error_file, 'r') as f:
                    logs.stderr = f.read()
            
            return logs
            
        except Exception as e:
            raise Exception(f"Failed to get job logs: {str(e)}")
    
    def get_cluster_info(self) -> ClusterInfoResponse:
        """Get cluster information."""
        try:
            # Get available queues
            exit_code, stdout, stderr = self._run_command(["qconf", "-sql"])
            available_queues = []
            if exit_code == 0:
                available_queues = [line.strip() for line in stdout.split('\n') if line.strip()]
            else:
                available_queues = self.default_queues
            
            return ClusterInfoResponse(
                cluster_name=self.cluster_name,
                available_queues=available_queues,
                max_nodes=self.max_nodes,
                max_cores_per_node=self.max_cores_per_node,
                max_memory_per_node=self.max_memory_per_node,
                max_walltime=self.max_walltime,
                default_modules=self.default_modules
            )
            
        except Exception as e:
            raise Exception(f"Failed to get cluster info: {str(e)}")



































