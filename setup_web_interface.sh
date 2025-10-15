#!/bin/bash
# WRF API Web Interface Setup Script
# This script sets up the web dashboard for the WRF API

echo "=========================================="
echo "WRF API Web Interface Setup"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this script from the API root directory."
    exit 1
fi

echo "🔧 Setting up web interface..."

# Create static directory if it doesn't exist
if [ ! -d "static" ]; then
    echo "📁 Creating static directory..."
    mkdir -p static
fi

# Check if dashboard file exists
if [ ! -f "static/wrf_dashboard.html" ]; then
    echo "❌ Error: static/wrf_dashboard.html not found."
    echo "Please ensure the dashboard file exists in the static directory."
    exit 1
fi

echo "✅ Web dashboard file found: static/wrf_dashboard.html"

# Check if API is running
echo "🔍 Checking if API is running..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API is running on port 8000"
else
    echo "⚠️  API is not running. Please start the API first:"
    echo "   python main.py"
    echo ""
    echo "Or in background:"
    echo "   nohup python main.py > api.log 2>&1 &"
    exit 1
fi

# Test web dashboard access
echo "🔍 Testing web dashboard access..."
if curl -s http://localhost:8000/dashboard > /dev/null 2>&1; then
    echo "✅ Web dashboard is accessible"
else
    echo "❌ Web dashboard is not accessible"
    echo "Please restart the API to load the new web interface:"
    echo "   pkill -f 'main.py'"
    echo "   python main.py"
    exit 1
fi

echo ""
echo "🎉 Web interface setup complete!"
echo ""
echo "📚 Web Interface Access:"
echo ""
echo "1. 🌐 Web Dashboard:"
echo "   http://localhost:8000/dashboard"
echo ""
echo "2. 📖 API Documentation (Swagger UI):"
echo "   http://localhost:8000/docs"
echo ""
echo "3. 📖 API Documentation (ReDoc):"
echo "   http://localhost:8000/redoc"
echo ""
echo "4. 🔍 API Health Check:"
echo "   http://localhost:8000/health"
echo ""
echo "🌐 For external access (if on cluster):"
echo "   http://login2.lengau.chpc.ac.za:8000/dashboard"
echo ""
echo "📋 Web Dashboard Features:"
echo "   ✅ System Information - View WRF installation details"
echo "   ✅ Job Submission - Submit WRF jobs through web form"
echo "   ✅ Job Management - Monitor and manage running jobs"
echo "   ✅ Templates - View WRF and WPS namelist templates"
echo "   ✅ API Documentation - Direct links to API docs"
echo ""
echo "🔧 Troubleshooting:"
echo "   - If dashboard doesn't load, restart the API"
echo "   - Check that static/wrf_dashboard.html exists"
echo "   - Ensure the API is running on port 8000"
echo ""
echo "📞 For support, contact: msovara"

































