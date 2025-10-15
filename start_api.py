#!/usr/bin/env python3
"""
Startup script for the Lengau Cluster Job Management API.

This script provides an easy way to start the API server with proper configuration
and logging setup.
"""

import uvicorn
import logging
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config import get_api_config, get_logging_config, get_security_config

def setup_logging():
    """Setup logging configuration."""
    log_config = get_logging_config()
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_config["level"]),
        format=log_config["format"],
        handlers=[
            logging.FileHandler(log_dir / log_config["file"]),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_dependencies():
    """Check if required dependencies are available."""
    try:
        import fastapi
        import uvicorn
        import pydantic
        print("✅ All required dependencies are available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        sys.exit(1)

def check_cluster_access():
    """Check if cluster commands are available."""
    import subprocess
    
    commands_to_check = ["qsub", "qstat", "qdel"]
    missing_commands = []
    
    for cmd in commands_to_check:
        try:
            result = subprocess.run([cmd, "--version"], 
                                  capture_output=True, 
                                  timeout=5)
            if result.returncode != 0:
                missing_commands.append(cmd)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            missing_commands.append(cmd)
    
    if missing_commands:
        print(f"⚠️  Warning: Some cluster commands not found: {missing_commands}")
        print("   The API will work but job operations may fail.")
        print("   Make sure you're running this on the Lengau cluster.")
    else:
        print("✅ Cluster commands are available")

def main():
    """Main function to start the API server."""
    print("🚀 Starting Lengau Cluster Job Management API")
    print("=" * 50)
    
    # Check dependencies
    check_dependencies()
    
    # Setup logging
    setup_logging()
    
    # Check cluster access
    check_cluster_access()
    
    # Get configuration
    api_config = get_api_config()
    
    print(f"📋 API Configuration:")
    print(f"   Title: {api_config['title']}")
    print(f"   Version: {api_config['version']}")
    print(f"   Host: {api_config['host']}")
    print(f"   Port: {api_config['port']}")
    print(f"   Debug: {api_config['debug']}")
    
    print("\n🌐 Starting server...")
    print(f"   API will be available at: http://{api_config['host']}:{api_config['port']}")
    print(f"   Interactive docs: http://{api_config['host']}:{api_config['port']}/docs")
    print(f"   Health check: http://{api_config['host']}:{api_config['port']}/health")
    
    print("\n" + "=" * 50)
    
    try:
        # Start the server
        uvicorn.run(
            "src.main:app",
            host=api_config["host"],
            port=api_config["port"],
            reload=api_config["debug"],
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()



































