#!/usr/bin/env python3
"""
Start script for the Plant Disease Detector backend
"""
import uvicorn
import os
import sys

def main():
    """Run the FastAPI application"""
    # Add the backend directory to Python path
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, backend_dir)
    
    # Start the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,  # Enable auto-reload for development
        reload_dirs=[backend_dir],
        log_level="info"
    )

if __name__ == "__main__":
    main()
