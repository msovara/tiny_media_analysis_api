#!/bin/bash

# Setup Public Access for Lengau API
# This script makes the API available to multiple users

set -e

# Configuration
API_PORT=8000
PROXY_PORT=8080
CLUSTER_HOSTNAME=$(hostname)
USER_HOME="$HOME"
API_DIR="$USER_HOME/lengau-api"
LOG_DIR="$USER_HOME/api_logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Lengau API Public Access Setup ===${NC}"

# Create log directory
mkdir -p "$LOG_DIR"

# Function to check if port is in use
check_port() {
    local port=$1
    if netstat -tlnp 2>/dev/null | grep -q ":$port "; then
        return 0
    else
        return 1
    fi
}

# Function to kill process on port
kill_port() {
    local port=$1
    echo -e "${YELLOW}Killing process on port $port...${NC}"
    pkill -f ":$port" || true
    sleep 2
}

# Step 1: Check if API is running
echo -e "${BLUE}Step 1: Checking API status...${NC}"
if check_port $API_PORT; then
    echo -e "${GREEN}✓ API is running on port $API_PORT${NC}"
else
    echo -e "${RED}✗ API is not running on port $API_PORT${NC}"
    echo -e "${YELLOW}Starting API...${NC}"
    cd "$API_DIR"
    nohup python main.py > "$LOG_DIR/api.log" 2>&1 &
    sleep 5
    
    if check_port $API_PORT; then
        echo -e "${GREEN}✓ API started successfully${NC}"
    else
        echo -e "${RED}✗ Failed to start API${NC}"
        exit 1
    fi
fi

# Step 2: Install reverse proxy dependencies
echo -e "${BLUE}Step 2: Installing reverse proxy dependencies...${NC}"
pip install httpx uvicorn fastapi

# Step 3: Create reverse proxy
echo -e "${BLUE}Step 3: Creating reverse proxy...${NC}"
cat > "$API_DIR/reverse_proxy.py" << 'EOF'
#!/usr/bin/env python3
"""
Reverse Proxy for Lengau API
Makes the API accessible to multiple users via a single endpoint
"""

import asyncio
import logging
from typing import Optional
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
import httpx
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
API_BACKEND_URL = "http://localhost:8000"
PROXY_HOST = "0.0.0.0"
PROXY_PORT = 8080

# Create FastAPI app for proxy
app = FastAPI(
    title="Lengau API Proxy",
    description="Reverse proxy for Lengau Cluster Job Management API",
    version="1.0.0"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    client_ip = request.client.host
    logger.info(f"{datetime.now()} - {client_ip} - {request.method} {request.url}")
    response = await call_next(request)
    return response

@app.get("/")
async def proxy_root():
    """Proxy root endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BACKEND_URL}/")
        return response.json()

@app.get("/health")
async def proxy_health():
    """Proxy health check"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BACKEND_URL}/health")
        return response.json()

@app.get("/docs")
async def proxy_docs():
    """Proxy API documentation"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BACKEND_URL}/docs")
        return response.text

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_api(request: Request, path: str):
    """Proxy all API requests"""
    target_url = f"{API_BACKEND_URL}/{path}"
    body = await request.body()
    
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=request.query_params,
                timeout=30.0
            )
            
            return StreamingResponse(
                iter([response.content]),
                status_code=response.status_code,
                headers=dict(response.headers)
            )
            
        except httpx.RequestError as e:
            logger.error(f"Proxy error: {e}")
            raise HTTPException(status_code=502, detail="Backend service unavailable")

@app.get("/proxy/status")
async def proxy_status():
    """Get proxy status"""
    return {
        "status": "running",
        "backend_url": API_BACKEND_URL,
        "timestamp": datetime.now().isoformat(),
        "proxy_version": "1.0.0"
    }

if __name__ == "__main__":
    logger.info(f"Starting proxy on {PROXY_HOST}:{PROXY_PORT}")
    logger.info(f"Backend API: {API_BACKEND_URL}")
    
    uvicorn.run(
        app,
        host=PROXY_HOST,
        port=PROXY_PORT,
        log_level="info"
    )
EOF

# Step 4: Start reverse proxy
echo -e "${BLUE}Step 4: Starting reverse proxy...${NC}"
if check_port $PROXY_PORT; then
    echo -e "${YELLOW}Proxy already running on port $PROXY_PORT${NC}"
    kill_port $PROXY_PORT
fi

cd "$API_DIR"
nohup python reverse_proxy.py > "$LOG_DIR/proxy.log" 2>&1 &
sleep 3

if check_port $PROXY_PORT; then
    echo -e "${GREEN}✓ Reverse proxy started on port $PROXY_PORT${NC}"
else
    echo -e "${RED}✗ Failed to start reverse proxy${NC}"
    exit 1
fi

# Step 5: Create access scripts
echo -e "${BLUE}Step 5: Creating access scripts...${NC}"

# Create user access script
cat > "$API_DIR/access_api.sh" << EOF
#!/bin/bash
# Script for users to access the API

echo "=== Lengau API Access ==="
echo "API is available at: http://$CLUSTER_HOSTNAME:$PROXY_PORT"
echo ""
echo "Quick test:"
curl -s http://$CLUSTER_HOSTNAME:$PROXY_PORT/health | jq .
echo ""
echo "Interactive docs: http://$CLUSTER_HOSTNAME:$PROXY_PORT/docs"
echo ""
echo "Example usage:"
echo "curl http://$CLUSTER_HOSTNAME:$PROXY_PORT/api/v1/cluster/jobs"
EOF

chmod +x "$API_DIR/access_api.sh"

# Create management script
cat > "$API_DIR/manage_api.sh" << EOF
#!/bin/bash
# API management script

case "\$1" in
    start)
        echo "Starting API..."
        cd "$API_DIR"
        nohup python main.py > "$LOG_DIR/api.log" 2>&1 &
        sleep 3
        nohup python reverse_proxy.py > "$LOG_DIR/proxy.log" 2>&1 &
        echo "API started"
        ;;
    stop)
        echo "Stopping API..."
        pkill -f "main.py"
        pkill -f "reverse_proxy.py"
        echo "API stopped"
        ;;
    restart)
        echo "Restarting API..."
        \$0 stop
        sleep 2
        \$0 start
        ;;
    status)
        echo "API Status:"
        if netstat -tlnp 2>/dev/null | grep -q ":$API_PORT "; then
            echo "✓ Backend API: Running on port $API_PORT"
        else
            echo "✗ Backend API: Not running"
        fi
        
        if netstat -tlnp 2>/dev/null | grep -q ":$PROXY_PORT "; then
            echo "✓ Reverse Proxy: Running on port $PROXY_PORT"
        else
            echo "✗ Reverse Proxy: Not running"
        fi
        ;;
    logs)
        echo "API Logs:"
        tail -f "$LOG_DIR/api.log" &
        echo "Proxy Logs:"
        tail -f "$LOG_DIR/proxy.log"
        ;;
    *)
        echo "Usage: \$0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac
EOF

chmod +x "$API_DIR/manage_api.sh"

# Step 6: Create user documentation
echo -e "${BLUE}Step 6: Creating user documentation...${NC}"

cat > "$API_DIR/USER_ACCESS.md" << EOF
# User Access Guide for Lengau API

## Quick Access

The API is now available at: **http://$CLUSTER_HOSTNAME:$PROXY_PORT**

## Testing the API

\`\`\`bash
# Health check
curl http://$CLUSTER_HOSTNAME:$PROXY_PORT/health

# List jobs
curl http://$CLUSTER_HOSTNAME:$PROXY_PORT/api/v1/cluster/jobs

# Interactive documentation
# Open in browser: http://$CLUSTER_HOSTNAME:$PROXY_PORT/docs
\`\`\`

## Python Client Example

\`\`\`python
import requests

# API base URL
BASE_URL = "http://$CLUSTER_HOSTNAME:$PROXY_PORT"

# Submit a job
job_data = {
    "job_name": "test_job",
    "script_content": "#!/bin/bash\\necho 'Hello from API!'\\ndate",
    "queue": "normal",
    "nodes": 1,
    "cores_per_node": 1,
    "memory_per_node": "4GB",
    "walltime": "00:10:00"
}

response = requests.post(f"{BASE_URL}/api/v1/cluster/jobs", json=job_data)
job_id = response.json()["job_id"]
print(f"Submitted job: {job_id}")

# Check status
status = requests.get(f"{BASE_URL}/api/v1/cluster/jobs/{job_id}")
print(f"Job status: {status.json()['status']}")
\`\`\`

## Available Endpoints

- **Health Check**: \`GET /health\`
- **API Info**: \`GET /\`
- **Submit Job**: \`POST /api/v1/cluster/jobs\`
- **List Jobs**: \`GET /api/v1/cluster/jobs\`
- **Job Status**: \`GET /api/v1/cluster/jobs/{job_id}\`
- **Cancel Job**: \`DELETE /api/v1/cluster/jobs/{job_id}\`
- **Job Logs**: \`GET /api/v1/cluster/jobs/{job_id}/logs\`
- **Cluster Info**: \`GET /api/v1/cluster/info\`
- **Queues**: \`GET /api/v1/cluster/queues\`
- **Modules**: \`GET /api/v1/cluster/modules\`

## Interactive Documentation

Visit: http://$CLUSTER_HOSTNAME:$PROXY_PORT/docs

This provides a web interface where you can:
- Test all endpoints interactively
- See request/response examples
- Try different parameters
- View API schemas

## Troubleshooting

If you can't access the API:

1. **Check if API is running**:
   \`\`\`bash
   curl http://$CLUSTER_HOSTNAME:$PROXY_PORT/health
   \`\`\`

2. **Check proxy status**:
   \`\`\`bash
   curl http://$CLUSTER_HOSTNAME:$PROXY_PORT/proxy/status
   \`\`\`

3. **Contact administrator** if issues persist

## Security Notes

- The API is accessible to all users on the cluster
- No authentication is currently implemented
- Use responsibly and don't submit malicious jobs
- Monitor your job submissions and clean up when done
EOF

# Step 7: Final status check
echo -e "${BLUE}Step 7: Final status check...${NC}"
sleep 2

echo -e "${GREEN}=== Setup Complete! ===${NC}"
echo ""
echo -e "${GREEN}✓ API Backend: http://localhost:$API_PORT${NC}"
echo -e "${GREEN}✓ Public Proxy: http://$CLUSTER_HOSTNAME:$PROXY_PORT${NC}"
echo ""
echo -e "${BLUE}Quick test:${NC}"
curl -s http://$CLUSTER_HOSTNAME:$PROXY_PORT/health | jq . 2>/dev/null || echo "API is running (jq not available for JSON formatting)"
echo ""
echo -e "${BLUE}Management commands:${NC}"
echo "  ./manage_api.sh status    # Check status"
echo "  ./manage_api.sh restart   # Restart services"
echo "  ./manage_api.sh logs      # View logs"
echo ""
echo -e "${BLUE}User access:${NC}"
echo "  http://$CLUSTER_HOSTNAME:$PROXY_PORT/docs    # Interactive docs"
echo "  ./access_api.sh           # Quick access script"
echo ""
echo -e "${YELLOW}Note: Users can now access the API at:${NC}"
echo -e "${GREEN}http://$CLUSTER_HOSTNAME:$PROXY_PORT${NC}"
