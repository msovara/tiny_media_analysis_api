from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from .api import router as media_router
from .job_api import router as job_router

# Create FastAPI app
app = FastAPI(
    title="Lengau Cluster Job Management API",
    description="A REST API for managing job submissions on the Lengau cluster at CHPC, with additional media analysis capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(media_router, prefix="/api/v1/media", tags=["Media Analysis"])
app.include_router(job_router, prefix="/api/v1/cluster", tags=["Cluster Management"])

# Serve static files for the dashboard
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Lengau Cluster Job Management API",
        "version": "1.0.0",
        "endpoints": {
            "media_analysis": {
                "articles": "/api/v1/media/articles",
                "stats": "/api/v1/media/stats"
            },
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
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 