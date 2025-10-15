#!/bin/bash
"""
Deployment script for the Lengau Cluster Job Management API.

This script helps deploy the API to the Lengau cluster and set up access.
"""

set -e

# Configuration
CLUSTER_HOST="lengau.chpc.ac.za"
CLUSTER_USER="${USER:-$(whoami)}"
API_DIR="/home/${CLUSTER_USER}/lengau-api"
LOCAL_DIR="$(pwd)"

echo "🚀 Deploying Lengau Cluster Job Management API"
echo "=============================================="
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

if [ "$DEPLOY_LOCAL" = false ]; then
    # Deploy to remote cluster
    echo "📦 Copying files to cluster..."
    rsync -avz --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' \
        --exclude='logs' --exclude='*.log' \
        "${LOCAL_DIR}/" "${CLUSTER_USER}@${CLUSTER_HOST}:${API_DIR}/"
    
    echo "🔧 Installing dependencies on cluster..."
    ssh "${CLUSTER_USER}@${CLUSTER_HOST}" << EOF
        cd ${API_DIR}
        pip install --user -r requirements.txt
        echo "✅ Dependencies installed"
EOF

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
    echo "📦 Installing dependencies..."
    pip install --user -r requirements.txt
    
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
echo "- Restart API: ./deploy_to_cluster.sh"



































