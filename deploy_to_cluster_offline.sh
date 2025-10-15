#!/bin/bash
"""
Offline deployment script for the Lengau Cluster Job Management API.

This script helps deploy the API to the cluster without requiring internet access.
"""

set -e

# Configuration
CLUSTER_HOST="lengau.chpc.ac.za"
CLUSTER_USER="${USER:-$(whoami)}"
API_DIR="/home/${CLUSTER_USER}/lengau-api"
LOCAL_DIR="$(pwd)"
PACKAGES_DIR="${LOCAL_DIR}/packages"

echo "🚀 Deploying Lengau Cluster Job Management API (Offline Mode)"
echo "============================================================="
echo "Cluster: ${CLUSTER_HOST}"
echo "User: ${CLUSTER_USER}"
echo "Local directory: ${LOCAL_DIR}"
echo "Remote directory: ${API_DIR}"
echo ""

# Check if we're on the cluster
if [[ "$(hostname)" == *"lengau"* ]] || [[ "$(hostname)" == *"chpc"* ]]; then
    echo "✅ Already on cluster, setting up API..."
    DEPLOY_LOCAL=true
else
    echo "📡 Deploying to remote cluster..."
    DEPLOY_LOCAL=false
fi

# Function to download packages locally
download_packages() {
    echo "📦 Downloading Python packages locally..."
    mkdir -p "${PACKAGES_DIR}"
    
    # Download all required packages
    pip download -r requirements.txt --dest "${PACKAGES_DIR}"
    
    echo "✅ Packages downloaded to ${PACKAGES_DIR}"
}

# Function to check cluster modules
check_cluster_modules() {
    echo "🔍 Checking available cluster modules..."
    
    ssh "${CLUSTER_USER}@${CLUSTER_HOST}" << 'EOF'
        echo "Available Python modules:"
        module avail python 2>/dev/null || echo "No python modules found"
        
        echo "Available FastAPI modules:"
        module avail fastapi 2>/dev/null || echo "No fastapi modules found"
        
        echo "Available conda environments:"
        conda env list 2>/dev/null || echo "No conda found"
EOF
}

# Function to install dependencies on cluster
install_dependencies() {
    echo "🔧 Installing dependencies on cluster..."
    
    ssh "${CLUSTER_USER}@${CLUSTER_HOST}" << EOF
        cd ${API_DIR}
        
        # Try to use existing modules first
        if module avail python >/dev/null 2>&1; then
            echo "Loading Python module..."
            module load python/3.8.5 2>/dev/null || module load python 2>/dev/null
        fi
        
        # Try to use conda if available
        if command -v conda >/dev/null 2>&1; then
            echo "Using conda to install packages..."
            conda install -y fastapi uvicorn pydantic requests aiofiles python-dotenv || echo "Conda install failed, trying pip"
        fi
        
        # Try to install from local packages
        if [ -d "packages" ]; then
            echo "Installing from local packages..."
            pip install --user --no-index --find-links packages -r requirements.txt
        else
            echo "No local packages found, trying pip install --user"
            pip install --user -r requirements.txt || echo "Pip install failed"
        fi
        
        echo "✅ Dependencies installation attempted"
EOF
}

if [ "$DEPLOY_LOCAL" = false ]; then
    # Check if packages need to be downloaded
    if [ ! -d "${PACKAGES_DIR}" ] || [ -z "$(ls -A ${PACKAGES_DIR} 2>/dev/null)" ]; then
        echo "📦 Packages not found locally. Downloading..."
        download_packages
    else
        echo "✅ Local packages found"
    fi
    
    # Check cluster modules
    check_cluster_modules
    
    # Deploy to remote cluster
    echo "📦 Copying files to cluster..."
    rsync -avz --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' \
        --exclude='logs' --exclude='*.log' \
        "${LOCAL_DIR}/" "${CLUSTER_USER}@${CLUSTER_HOST}:${API_DIR}/"
    
    # Install dependencies
    install_dependencies
    
    echo "🚀 Starting API on cluster..."
    ssh -f "${CLUSTER_USER}@${CLUSTER_HOST}" << EOF
        cd ${API_DIR}
        nohup python start_api.py > api.log 2>&1 &
        echo \$! > api.pid
        echo "✅ API started with PID \$(cat api.pid)"
EOF

    echo "🔗 Setting up SSH tunnel..."
    echo "Run this command to access the API:"
    echo "ssh -L 8000:localhost:8000 ${CLUSTER_USER}@${CLUSTER_HOST}"
    echo ""
    echo "Then access the API at: http://localhost:8000"
    echo "Interactive docs: http://localhost:8000/docs"

else
    # Already on cluster
    echo "🔍 Checking available modules..."
    
    # Try to use existing modules
    if module avail python >/dev/null 2>&1; then
        echo "Loading Python module..."
        module load python/3.8.5 2>/dev/null || module load python 2>/dev/null
    fi
    
    # Try to use conda if available
    if command -v conda >/dev/null 2>&1; then
        echo "Using conda to install packages..."
        conda install -y fastapi uvicorn pydantic requests aiofiles python-dotenv || echo "Conda install failed, trying pip"
    fi
    
    # Try to install from local packages
    if [ -d "packages" ]; then
        echo "Installing from local packages..."
        pip install --user --no-index --find-links packages -r requirements.txt
    else
        echo "No local packages found, trying pip install --user"
        pip install --user -r requirements.txt || echo "Pip install failed"
    fi
    
    echo "🚀 Starting API..."
    python start_api.py
fi

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Access the API at: http://localhost:8000 (via SSH tunnel)"
echo "2. View interactive docs: http://localhost:8000/docs"
echo "3. Test with: curl http://localhost:8000/api/v1/cluster/info"
echo ""
echo "🛠️  Management commands:"
echo "- Stop API: ssh ${CLUSTER_USER}@${CLUSTER_HOST} 'kill \$(cat ${API_DIR}/api.pid)'"
echo "- View logs: ssh ${CLUSTER_USER}@${CLUSTER_HOST} 'tail -f ${API_DIR}/api.log'"
echo "- Restart API: ./deploy_to_cluster_offline.sh"
echo ""
echo "💡 Tips:"
echo "- If packages fail to install, check available modules with: module avail"
echo "- Use conda if available: conda install fastapi uvicorn pydantic"
echo "- The API itself doesn't need internet access once running"


































