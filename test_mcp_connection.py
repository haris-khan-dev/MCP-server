#!/usr/bin/env python3
"""
Test script to verify MCP server connection
"""
import asyncio
import aiohttp
import json
from gemini_mcp_server import mcp

async def test_mcp_tools():
    """Test all MCP tools"""
    print("🧪 Testing MCP Server Tools...")
    print("=" * 50)
    
    try:
        # Test health check
        print("1. Testing health check...")
        health = await mcp.get_health_status()
        print(f"   ✅ Health: {health}")
        
        # Test app info
        print("2. Testing app info...")
        info = await mcp.get_app_info()
        print(f"   ✅ App info: {info.get('message', 'N/A')}")
        
        # Test dice roll
        print("3. Testing dice roll...")
        dice = await mcp.roll_dice(sides=6, count=3)
        print(f"   ✅ Dice roll: {dice}")
        
        # Test statistics
        print("4. Testing statistics...")
        stats = await mcp.get_app_statistics()
        print(f"   ✅ Stats: {stats}")
        
        # Test user creation
        print("5. Testing user creation...")
        user = await mcp.create_user("Test User", "test@example.com", 25)
        print(f"   ✅ User created: {user}")
        
        # Test task creation
        print("6. Testing task creation...")
        task = await mcp.create_task("Test Task", "This is a test task")
        print(f"   ✅ Task created: {task}")
        
        print("\n🎉 All MCP tools are working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP tools: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 MCP Server Connection Test")
    print("=" * 50)
    
    # Test FastAPI server connection
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/health") as response:
                if response.status == 200:
                    print("✅ FastAPI server is running and healthy")
                else:
                    print(f"❌ FastAPI server returned status {response.status}")
                    return
    except Exception as e:
        print(f"❌ Cannot connect to FastAPI server: {e}")
        print("Please start the FastAPI server with: python app.py")
        return
    
    # Test MCP tools
    success = await test_mcp_tools()
    
    if success:
        print("\n🎉 MCP Server is ready for Gemini CLI!")
        print("You can now use the /mcp command in Gemini CLI")
    else:
        print("\n❌ MCP Server has issues that need to be fixed")

if __name__ == "__main__":
    asyncio.run(main())
