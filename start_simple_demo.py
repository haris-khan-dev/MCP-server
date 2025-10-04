#!/usr/bin/env python3
"""
Simplified startup script for FastAPI + MCP + Gemini demo
Works without fastmcp dependency
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
        import aiohttp
        import google.generativeai
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install fastapi uvicorn aiohttp google-generativeai python-dotenv requests")
        return False

def check_env():
    """Check if environment variables are set"""
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  GEMINI_API_KEY environment variable not set")
        print("   The demo will run in simulation mode")
        return True  # Allow demo to run without API key
    print("✅ Environment variables are set")
    return True

def start_fastapi():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    try:
        # Start FastAPI server in background
        process = subprocess.Popen([
            sys.executable, "app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ FastAPI server started on http://localhost:8000")
        return process
    except Exception as e:
        print(f"❌ Failed to start FastAPI server: {e}")
        return None

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

def run_simple_demo():
    """Run the simplified Gemini integration demo"""
    print("🤖 Starting simplified Gemini integration demo...")
    try:
        subprocess.run([sys.executable, "simple_gemini_integration.py"])
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Error running demo: {e}")

def test_mcp_server():
    """Test the MCP server"""
    print("🧪 Testing MCP server...")
    try:
        subprocess.run([sys.executable, "simple_mcp_server.py"])
        return True
    except Exception as e:
        print(f"❌ MCP server test failed: {e}")
        return False

def main():
    """Main function"""
    print("🎯 FastAPI + MCP + Gemini Demo (Simplified)")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return
    
    # Check environment
    if not check_env():
        return
    
    # Test MCP server
    print("\n🧪 Testing MCP server...")
    if not test_mcp_server():
        print("❌ MCP server test failed")
        return
    
    # Start FastAPI server
    print("\n🚀 Starting FastAPI server...")
    fastapi_process = start_fastapi()
    if not fastapi_process:
        return
    
    # Wait for server to be ready
    if not wait_for_server():
        print("❌ Server failed to start")
        return
    
    print("\n🎉 Everything is ready!")
    print("You can now:")
    print("1. Visit http://localhost:8000 to see the FastAPI docs")
    print("2. Test the API endpoints")
    print("3. Run the simplified Gemini integration demo")
    print("\nPress Ctrl+C to stop the demo")
    
    try:
        # Run the simplified demo
        run_simple_demo()
    except KeyboardInterrupt:
        print("\n👋 Demo stopped")
    finally:
        print("🛑 Stopping FastAPI server...")
        if fastapi_process:
            fastapi_process.terminate()
        print("Demo completed!")

if __name__ == "__main__":
    main()
