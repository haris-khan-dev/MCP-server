#!/usr/bin/env python3
"""
Test script to verify FastAPI + MCP integration
"""
import asyncio
import aiohttp
import json
from fastmcp import Client

async def test_fastapi_server():
    """Test if FastAPI server is running and responding"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print("✅ FastAPI server is healthy")
                    print(f"   Status: {data.get('status')}")
                    return True
                else:
                    print(f"❌ FastAPI server returned status {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Cannot connect to FastAPI server: {e}")
        return False

async def test_mcp_server():
    """Test if MCP server can connect to FastAPI"""
    try:
        mcp_client = Client("mcp_server.py")
        async with mcp_client:
            # Test a simple tool
            result = await mcp_client.call_tool("get_health_status")
            print("✅ MCP server can connect to FastAPI")
            print(f"   Health check result: {result}")
            return True
    except Exception as e:
        print(f"❌ MCP server error: {e}")
        return False

async def test_mcp_tools():
    """Test various MCP tools"""
    try:
        mcp_client = Client("mcp_server.py")
        async with mcp_client:
            print("🧪 Testing MCP tools...")
            
            # Test health check
            health = await mcp_client.call_tool("get_health_status")
            print(f"   Health: {health}")
            
            # Test app info
            info = await mcp_client.call_tool("get_app_info")
            print(f"   App info: {info.get('message', 'N/A')}")
            
            # Test dice roll
            dice = await mcp_client.call_tool("roll_dice", {"sides": 6, "count": 3})
            print(f"   Dice roll: {dice}")
            
            # Test statistics
            stats = await mcp_client.call_tool("get_app_statistics")
            print(f"   Stats: {stats}")
            
            print("✅ All MCP tools working correctly")
            return True
    except Exception as e:
        print(f"❌ MCP tools test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 Testing FastAPI + MCP Integration")
    print("=" * 40)
    
    # Test FastAPI server
    fastapi_ok = await test_fastapi_server()
    if not fastapi_ok:
        print("\n❌ FastAPI server is not running")
        print("Please start it with: python app.py")
        return
    
    # Test MCP server
    mcp_ok = await test_mcp_server()
    if not mcp_ok:
        print("\n❌ MCP server cannot connect to FastAPI")
        return
    
    # Test MCP tools
    tools_ok = await test_mcp_tools()
    if not tools_ok:
        print("\n❌ MCP tools are not working correctly")
        return
    
    print("\n🎉 All tests passed!")
    print("Your FastAPI + MCP integration is working correctly.")
    print("You can now run the Gemini integration demo.")

if __name__ == "__main__":
    asyncio.run(main())
