#!/usr/bin/env python3
"""
Setup script for configuring MCP server with Gemini CLI
"""
import subprocess
import sys
import os
import json
from pathlib import Path

def check_fastmcp_installed():
    """Check if FastMCP is installed"""
    try:
        import fastmcp
        print("✅ FastMCP is installed")
        return True
    except ImportError:
        print("❌ FastMCP is not installed")
        return False

def install_fastmcp():
    """Install FastMCP"""
    print("📦 Installing FastMCP...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "fastmcp>=2.12.3"], check=True)
        print("✅ FastMCP installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install FastMCP: {e}")
        return False

def install_mcp_server():
    """Install MCP server with Gemini CLI"""
    print("🔧 Installing MCP server with Gemini CLI...")
    try:
        # Use fastmcp install command for Gemini CLI
        result = subprocess.run([
            sys.executable, "-m", "fastmcp", "install", "gemini-cli", "gemini_mcp_server.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ MCP server installed with Gemini CLI")
            print(result.stdout)
            return True
        else:
            print(f"❌ Failed to install MCP server: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing MCP server: {e}")
        return False

def create_gemini_config():
    """Create Gemini CLI configuration file"""
    config = {
        "mcpServers": {
            "fastapi-server": {
                "command": "python",
                "args": ["gemini_mcp_server.py"],
                "env": {
                    "API_BASE_URL": "http://localhost:8000"
                }
            }
        }
    }
    
    config_path = Path.home() / ".config" / "gemini" / "mcp_config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Gemini CLI configuration created at {config_path}")
    return True

def test_mcp_server():
    """Test the MCP server"""
    print("🧪 Testing MCP server...")
    try:
        result = subprocess.run([
            sys.executable, "gemini_mcp_server.py"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ MCP server test passed")
            return True
        else:
            print(f"❌ MCP server test failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✅ MCP server started successfully (timeout expected)")
        return True
    except Exception as e:
        print(f"❌ MCP server test error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up MCP server for Gemini CLI")
    print("=" * 50)
    
    # Check if FastMCP is installed
    if not check_fastmcp_installed():
        if not install_fastmcp():
            print("❌ Cannot proceed without FastMCP")
            return False
    
    # Create Gemini CLI configuration
    if not create_gemini_config():
        print("❌ Failed to create Gemini CLI configuration")
        return False
    
    # Test MCP server
    if not test_mcp_server():
        print("❌ MCP server test failed")
        return False
    
    # Try to install with Gemini CLI
    print("\n🔧 Attempting to install MCP server with Gemini CLI...")
    install_mcp_server()
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Make sure your FastAPI server is running: python app.py")
    print("2. In Gemini CLI, you should now see MCP tools available")
    print("3. Try commands like: 'Check the health of my FastAPI server'")
    print("4. Or: 'Create a new user named John with email john@example.com'")
    
    return True

if __name__ == "__main__":
    main()
