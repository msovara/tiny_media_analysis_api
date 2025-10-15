#!/bin/bash
# WRF API User Access Setup Script
# This script helps users set up access to the WRF API on Lengau cluster

echo "=========================================="
echo "WRF API User Access Setup"
echo "=========================================="

# Check if user is on the cluster
if [[ "$HOSTNAME" == *"lengau"* ]] || [[ "$HOSTNAME" == *"login"* ]]; then
    echo "✅ You are on the Lengau cluster"
    API_URL="http://localhost:8000"
else
    echo "⚠️  You are not on the Lengau cluster"
    echo "You need to SSH to the cluster first:"
    echo "ssh YOUR_USERNAME@login2.lengau.chpc.ac.za"
    echo ""
    echo "Or create an SSH tunnel:"
    echo "ssh -L 8000:localhost:8000 YOUR_USERNAME@login2.lengau.chpc.ac.za"
    echo ""
    API_URL="http://localhost:8000"
fi

echo ""
echo "🔧 Setting up WRF API access..."

# Check if Python is available
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 is available"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    echo "✅ Python is available"
    PYTHON_CMD="python"
else
    echo "❌ Python is not available"
    exit 1
fi

# Check if requests module is available
if $PYTHON_CMD -c "import requests" 2>/dev/null; then
    echo "✅ requests module is available"
else
    echo "⚠️  requests module not found"
    echo "Installing requests module..."
    pip install requests
fi

# Test API connectivity
echo ""
echo "🔍 Testing API connectivity..."

# Test health endpoint
if curl -s "$API_URL/health" > /dev/null 2>&1; then
    echo "✅ API is accessible"
else
    echo "❌ API is not accessible"
    echo "Make sure the API is running on the cluster"
    echo "Contact the API administrator (msovara) if needed"
    exit 1
fi

# Test WRF info endpoint
if curl -s "$API_URL/api/v1/wrf/info" > /dev/null 2>&1; then
    echo "✅ WRF API endpoints are working"
else
    echo "❌ WRF API endpoints are not working"
    echo "The API might not be running with WRF support"
    exit 1
fi

echo ""
echo "🎉 Setup complete! You can now use the WRF API"
echo ""
echo "📚 Quick Start Examples:"
echo ""
echo "1. Get WRF information:"
echo "   curl $API_URL/api/v1/wrf/info"
echo ""
echo "2. List WRF jobs:"
echo "   curl $API_URL/api/v1/wrf/jobs"
echo ""
echo "3. Get example configurations:"
echo "   curl $API_URL/api/v1/wrf/examples"
echo ""
echo "4. Run the Python client:"
echo "   $PYTHON_CMD examples/wrf_client.py"
echo ""
echo "📖 For detailed usage, see: USER_ACCESS_GUIDE.md"
echo "📖 For API documentation: $API_URL/docs"
echo ""
echo "🔗 Useful commands:"
echo "   - Submit job: POST $API_URL/api/v1/wrf/jobs"
echo "   - Get job status: GET $API_URL/api/v1/wrf/jobs/{job_id}"
echo "   - Cancel job: DELETE $API_URL/api/v1/wrf/jobs/{job_id}"
echo "   - Get job logs: GET $API_URL/api/v1/wrf/jobs/{job_id}/logs"
echo ""
echo "📞 For support, contact: msovara"

































