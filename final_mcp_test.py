#!/usr/bin/env python3
"""
Final test to verify MCP server is working correctly
"""
import asyncio
import aiohttp
from fastmcp import Client

async def test_complete_mcp_workflow():
    """Test complete MCP workflow"""
    print("🚀 Final MCP Server Test")
    print("=" * 50)
    
    try:
        # Test FastAPI server
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/health") as response:
                if response.status != 200:
                    print("❌ FastAPI server is not running")
                    return False
                print("✅ FastAPI server is healthy")
        
        # Test MCP server
        mcp_client = Client("gemini_mcp_server.py")
        
        async with mcp_client:
            print("✅ MCP client connected")
            
            # Test all major functions
            print("\n🧪 Testing MCP Tools:")
            
            # 1. Health check
            health = await mcp_client.call_tool("get_health_status")
            print(f"1. Health: {health.data['status']}")
            
            # 2. App info
            info = await mcp_client.call_tool("get_app_info")
            print(f"2. App: {info.data['message']}")
            
            # 3. Dice roll
            dice = await mcp_client.call_tool("roll_dice", {"sides": 6, "count": 3})
            print(f"3. Dice: {dice.data['results']}")
            
            # 4. Create user
            user = await mcp_client.call_tool("create_user", {
                "name": "John Doe", 
                "email": "john@example.com", 
                "age": 30
            })
            print(f"4. User created: {user.data}")
            
            # 5. Create task
            task = await mcp_client.call_tool("create_task", {
                "title": "Learn MCP", 
                "description": "Study Model Context Protocol"
            })
            print(f"5. Task created: {task.data}")
            
            # 6. Get statistics
            stats = await mcp_client.call_tool("get_app_statistics")
            print(f"6. Stats: {stats.data}")
            
            print("\n🎉 All MCP tools working perfectly!")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    """Main function"""
    success = await test_complete_mcp_workflow()
    
    if success:
        print("\n" + "="*60)
        print("🎉 MCP SERVER IS READY FOR GEMINI CLI!")
        print("="*60)
        print("\n📋 INSTRUCTIONS FOR GEMINI CLI:")
        print("1. Make sure FastAPI server is running: python app.py")
        print("2. In Gemini CLI, use the /mcp command to see available tools")
        print("3. Try these natural language commands:")
        print("   • 'Check the health of my FastAPI server'")
        print("   • 'Create a new user named Alice with email alice@example.com and age 25'")
        print("   • 'Create a task called Learn Python with description Study Python programming'")
        print("   • 'Roll 5 dice with 10 sides each'")
        print("   • 'Show me the statistics of my application'")
        print("   • 'Get all users from my system'")
        print("   • 'Get all tasks from my system'")
        print("\n🔧 MCP COMMANDS IN GEMINI CLI:")
        print("• /mcp - Show MCP server status")
        print("• /mcp desc - Show tool descriptions")
        print("• /mcp schema - Show tool schemas")
        print("\n✅ Your FastAPI + MCP + Gemini integration is complete!")
    else:
        print("\n❌ MCP server needs to be fixed")

if __name__ == "__main__":
    asyncio.run(main())
