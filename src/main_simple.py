"""
Simplified FastAPI application for Lengau Cluster Job Management API.

This version uses minimal dependencies and can run with just:
- fastapi
- uvicorn
- pydantic
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import only essential components
try:
    from .job_api import router as job_router
    from .api import router as media_router
    HAS_FULL_IMPORTS = True
except ImportError:
    print("⚠️  Some modules not available, running in minimal mode")
    HAS_FULL_IMPORTS = False

# Create FastAPI app
app = FastAPI(
    title="Lengau Cluster Job Management API (Minimal)",
    description="A REST API for managing job submissions on the Lengau cluster at CHPC",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes if available
if HAS_FULL_IMPORTS:
    app.include_router(media_router, prefix="/api/v1/media", tags=["Media Analysis"])
    app.include_router(job_router, prefix="/api/v1/cluster", tags=["Cluster Management"])
else:
    # Minimal endpoints for testing
    @app.get("/api/v1/cluster/info")
    async def get_cluster_info():
        """Get basic cluster information."""
        return {
            "cluster_name": "Lengau",
            "available_queues": ["normal", "long", "short", "debug"],
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
    
    @app.get("/api/v1/cluster/queues")
    async def get_available_queues():
        """Get available queues."""
        return {"queues": ["normal", "long", "short", "debug"]}
    
    @app.get("/api/v1/cluster/modules")
    async def get_default_modules():
        """Get default modules."""
        return {
            "modules": [
                "chpc/parallel_studio_xe/16.0.1/2016.1.150",
                "chpc/netcdf/4.4.3-F/intel/16.0.1",
                "chpc/hdf5/1.8.16/intel/16.0.1"
            ]
        }

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Lengau Cluster Job Management API (Minimal Mode)",
        "version": "1.0.0",
        "status": "running",
        "mode": "minimal" if not HAS_FULL_IMPORTS else "full",
        "endpoints": {
            "cluster_info": "/api/v1/cluster/info",
            "queues": "/api/v1/cluster/queues",
            "modules": "/api/v1/cluster/modules",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "mode": "minimal" if not HAS_FULL_IMPORTS else "full"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Lengau Cluster Job Management API (Minimal Mode)")
    print("=" * 60)
    print("Mode:", "minimal" if not HAS_FULL_IMPORTS else "full")
    print("Available at: http://0.0.0.0:8000")
    print("Interactive docs: http://0.0.0.0:8000/docs")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)


































