#!/usr/bin/env python3
"""
Proper test script for MCP server using FastMCP client
"""
import asyncio
import aiohttp
from fastmcp import Client

async def test_fastapi_connection():
    """Test FastAPI server connection"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ FastAPI server is healthy: {data}")
                    return True
                else:
                    print(f"❌ FastAPI server returned status {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Cannot connect to FastAPI server: {e}")
        return False

async def test_mcp_server():
    """Test MCP server using FastMCP client"""
    print("🧪 Testing MCP Server with FastMCP Client...")
    print("=" * 50)
    
    try:
        # Create MCP client
        mcp_client = Client("gemini_mcp_server.py")
        
        async with mcp_client:
            print("✅ MCP client connected successfully")
            
            # Test health check
            print("1. Testing health check...")
            health_result = await mcp_client.call_tool("get_health_status")
            health_data = health_result.data
            print(f"   ✅ Health: {health_data}")
            
            # Test app info
            print("2. Testing app info...")
            info_result = await mcp_client.call_tool("get_app_info")
            info_data = info_result.data
            print(f"   ✅ App info: {info_data.get('message', 'N/A')}")
            
            # Test dice roll
            print("3. Testing dice roll...")
            dice_result = await mcp_client.call_tool("roll_dice", {"sides": 6, "count": 3})
            dice_data = dice_result.data
            print(f"   ✅ Dice roll: {dice_data}")
            
            # Test statistics
            print("4. Testing statistics...")
            stats_result = await mcp_client.call_tool("get_app_statistics")
            stats_data = stats_result.data
            print(f"   ✅ Stats: {stats_data}")
            
            # Test user creation
            print("5. Testing user creation...")
            user_result = await mcp_client.call_tool("create_user", {
                "name": "Test User", 
                "email": "test@example.com", 
                "age": 25
            })
            user_data = user_result.data
            print(f"   ✅ User created: {user_data}")
            
            # Test task creation
            print("6. Testing task creation...")
            task_result = await mcp_client.call_tool("create_task", {
                "title": "Test Task", 
                "description": "This is a test task"
            })
            task_data = task_result.data
            print(f"   ✅ Task created: {task_data}")
            
            print("\n🎉 All MCP tools are working correctly!")
            return True
            
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 MCP Server Connection Test")
    print("=" * 50)
    
    # Test FastAPI server
    if not await test_fastapi_connection():
        print("Please start the FastAPI server with: python app.py")
        return
    
    # Test MCP server
    success = await test_mcp_server()
    
    if success:
        print("\n🎉 MCP Server is ready for Gemini CLI!")
        print("You can now use the /mcp command in Gemini CLI")
        print("\nTry these commands in Gemini CLI:")
        print("- 'Check the health of my FastAPI server'")
        print("- 'Create a new user named John with email john@example.com'")
        print("- 'Roll 3 dice with 6 sides each'")
    else:
        print("\n❌ MCP Server has issues that need to be fixed")

if __name__ == "__main__":
    asyncio.run(main())
