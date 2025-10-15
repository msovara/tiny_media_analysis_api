"""
Configuration settings for the Lengau Cluster Job Management API.
"""

import os
from typing import List, Dict, Any

# Cluster Configuration
CLUSTER_CONFIG = {
    "name": "Lengau",
    "default_queues": ["normal", "long", "short", "debug"],
    "max_nodes": 1000,
    "max_cores_per_node": 64,
    "max_memory_per_node": "256GB",
    "max_walltime": "168:00:00",
    "default_modules": [
        "chpc/parallel_studio_xe/16.0.1/2016.1.150",
        "chpc/netcdf/4.4.3-F/intel/16.0.1",
        "chpc/hdf5/1.8.16/intel/16.0.1"
    ]
}

# Job Submission Defaults
JOB_DEFAULTS = {
    "queue": "normal",
    "nodes": 1,
    "cores_per_node": 1,
    "memory_per_node": "4GB",
    "walltime": "01:00:00",
    "email_events": "END"
}

# API Configuration
API_CONFIG = {
    "title": "Lengau Cluster Job Management API",
    "description": "A REST API for managing job submissions on the Lengau cluster at CHPC",
    "version": "1.0.0",
    "host": "0.0.0.0",  # Bind to all interfaces for cluster access
    "port": 8000,
    "debug": False
}

# PBS/SLURM Commands
CLUSTER_COMMANDS = {
    "submit": "qsub",
    "status": "qstat",
    "cancel": "qdel",
    "hold": "qhold",
    "release": "qrls",
    "list_queues": "qconf -sql"
}

# File Paths
PATHS = {
    "working_directory": os.getenv("PBS_O_WORKDIR", "/home"),
    "log_directory": os.getenv("PBS_O_WORKDIR", "/home"),
    "temp_directory": "/tmp"
}

# Environment Variables
ENV_VARS = {
    "OMP_NUM_THREADS": "1",
    "MPI_NUM_THREADS": "1"
}

# ARWpost Specific Configuration
ARWPOST_CONFIG = {
    "module_name": "arwpost/3.1",
    "required_modules": [
        "chpc/parallel_studio_xe/16.0.1/2016.1.150",
        "chpc/netcdf/4.4.3-F/intel/16.0.1",
        "chpc/hdf5/1.8.16/intel/16.0.1"
    ],
    "default_resources": {
        "nodes": 2,
        "cores_per_node": 8,
        "memory_per_node": "32GB",
        "walltime": "02:00:00"
    }
}

# WRF Specific Configuration
WRF_CONFIG = {
    "required_modules": [
        "chpc/parallel_studio_xe/16.0.1/2016.1.150",
        "chpc/netcdf/4.4.3-F/intel/16.0.1",
        "chpc/hdf5/1.8.16/intel/16.0.1"
    ],
    "default_resources": {
        "nodes": 4,
        "cores_per_node": 16,
        "memory_per_node": "64GB",
        "walltime": "24:00:00"
    }
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "api.log"
}

# Security Configuration
SECURITY_CONFIG = {
    "cors_origins": ["*"],  # In production, specify actual origins
    "cors_credentials": True,
    "cors_methods": ["*"],
    "cors_headers": ["*"]
}

# Cluster Network Configuration
CLUSTER_NETWORK = {
    "login_node": "lengau.chpc.ac.za",
    "internal_port": 8000,
    "external_port": 8000,  # May be different if using SSH tunnel
    "ssh_tunnel": True,  # Whether to use SSH tunnel for access
    "allowed_hosts": ["*.chpc.ac.za", "localhost", "127.0.0.1"]
}

def get_cluster_config() -> Dict[str, Any]:
    """Get cluster configuration."""
    return CLUSTER_CONFIG.copy()

def get_job_defaults() -> Dict[str, Any]:
    """Get job submission defaults."""
    return JOB_DEFAULTS.copy()

def get_api_config() -> Dict[str, Any]:
    """Get API configuration."""
    return API_CONFIG.copy()

def get_cluster_commands() -> Dict[str, str]:
    """Get cluster command mappings."""
    return CLUSTER_COMMANDS.copy()

def get_paths() -> Dict[str, str]:
    """Get file paths configuration."""
    return PATHS.copy()

def get_env_vars() -> Dict[str, str]:
    """Get default environment variables."""
    return ENV_VARS.copy()

def get_arwpost_config() -> Dict[str, Any]:
    """Get ARWpost-specific configuration."""
    return ARWPOST_CONFIG.copy()

def get_wrf_config() -> Dict[str, Any]:
    """Get WRF-specific configuration."""
    return WRF_CONFIG.copy()

def get_logging_config() -> Dict[str, Any]:
    """Get logging configuration."""
    return LOGGING_CONFIG.copy()

def get_security_config() -> Dict[str, Any]:
    """Get security configuration."""
    return SECURITY_CONFIG.copy()
