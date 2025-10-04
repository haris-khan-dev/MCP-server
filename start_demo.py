#!/usr/bin/env python3
"""
Startup script for FastAPI + FastMCP + Gemini demo
"""
import subprocess
import sys
import time
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import fastmcp
        import google.generativeai
        import aiohttp
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env():
    """Check if environment variables are set"""
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY environment variable not set")
        print("Please create a .env file with your Gemini API key")
        return False
    print("✅ Environment variables are set")
    return True

def start_fastapi():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    try:
        subprocess.Popen([
            sys.executable, "app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ FastAPI server started on http://localhost:8000")
        return True
    except Exception as e:
        print(f"❌ Failed to start FastAPI server: {e}")
        return False

def wait_for_server():
    """Wait for the server to be ready"""
    import requests
    max_attempts = 30
    for i in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/health", timeout=1)
            if response.status_code == 200:
                print("✅ FastAPI server is ready")
                return True
        except:
            pass
        time.sleep(1)
        print(f"⏳ Waiting for server... ({i+1}/{max_attempts})")
    
    print("❌ Server failed to start within 30 seconds")
    return False

def run_gemini_demo():
    """Run the Gemini integration demo"""
    print("🤖 Starting Gemini integration demo...")
    try:
        subprocess.run([sys.executable, "gemini_integration.py"])
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Error running demo: {e}")

def main():
    """Main function"""
    print("🎯 FastAPI + FastMCP + Gemini Demo")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        return
    
    # Check environment
    if not check_env():
        return
    
    # Start FastAPI server
    if not start_fastapi():
        return
    
    # Wait for server to be ready
    if not wait_for_server():
        return
    
    print("\n🎉 Everything is ready!")
    print("You can now:")
    print("1. Visit http://localhost:8000 to see the FastAPI docs")
    print("2. Test the API endpoints")
    print("3. Run the Gemini integration demo")
    print("\nPress Ctrl+C to stop the demo")
    
    try:
        # Run the Gemini demo
        run_gemini_demo()
    except KeyboardInterrupt:
        print("\n👋 Demo stopped")
    finally:
        print("🛑 Stopping FastAPI server...")
        # Note: In a real implementation, you'd want to properly stop the server
        print("Demo completed!")

if __name__ == "__main__":
    main()
