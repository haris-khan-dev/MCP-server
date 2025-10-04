"""
Simplified Gemini integration without fastmcp dependency
This provides the same functionality as the original gemini_integration.py
"""
import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
from simple_mcp_server import mcp_server

# Load environment variables
load_dotenv()

async def call_mcp_tool(tool_name: str, **kwargs):
    """Call MCP tool and return result"""
    try:
        result = await mcp_server.call_tool(tool_name, **kwargs)
        return result
    except Exception as e:
        return f"Error calling {tool_name}: {str(e)}"

async def simulate_gemini_with_tools():
    """Simulate Gemini-like behavior with MCP tools"""
    
    print("🤖 Gemini + MCP Integration Demo (Simplified)")
    print("=" * 60)
    
    # Demo queries with their corresponding MCP tool calls
    demo_scenarios = [
        {
            "query": "Check the health status of the FastAPI application",
            "tool": "get_health_status",
            "args": {}
        },
        {
            "query": "Get information about the FastAPI application",
            "tool": "get_app_info", 
            "args": {}
        },
        {
            "query": "Create a new user named 'John Doe' with email 'john@example.com' and age 30",
            "tool": "create_user",
            "args": {"name": "John Doe", "email": "john@example.com", "age": 30}
        },
        {
            "query": "Create a task called 'Learn FastMCP' with description 'Study FastMCP integration'",
            "tool": "create_task",
            "args": {"title": "Learn FastMCP", "description": "Study FastMCP integration"}
        },
        {
            "query": "Roll 3 dice with 6 sides each",
            "tool": "roll_dice",
            "args": {"sides": 6, "count": 3}
        },
        {
            "query": "Get all users and show me the statistics",
            "tool": "get_all_users",
            "args": {}
        },
        {
            "query": "Get application statistics",
            "tool": "get_app_statistics",
            "args": {}
        },
        {
            "query": "Show me all pending tasks",
            "tool": "get_pending_tasks",
            "args": {}
        }
    ]
    
    for i, scenario in enumerate(demo_scenarios, 1):
        print(f"\n🔍 Query {i}: {scenario['query']}")
        print("-" * 50)
        
        try:
            # Call the MCP tool
            result = await call_mcp_tool(scenario['tool'], **scenario['args'])
            
            # Simulate Gemini's response
            if scenario['tool'] == 'get_health_status':
                print(f"🤖 Gemini Response: The FastAPI application is {result.get('status', 'unknown')} at {result.get('timestamp', 'unknown time')}")
            elif scenario['tool'] == 'get_app_info':
                print(f"🤖 Gemini Response: {result.get('message', 'Welcome')} - Version {result.get('version', '1.0.0')}")
            elif scenario['tool'] == 'create_user':
                print(f"🤖 Gemini Response: Successfully created user '{result.get('name', 'Unknown')}' with ID {result.get('id', 'N/A')}")
            elif scenario['tool'] == 'create_task':
                print(f"🤖 Gemini Response: Created task '{result.get('title', 'Unknown')}' with ID {result.get('id', 'N/A')}")
            elif scenario['tool'] == 'roll_dice':
                results = result.get('results', [])
                print(f"🤖 Gemini Response: Rolled {result.get('count', 0)} dice with {result.get('sides', 6)} sides each. Results: {results}")
            elif scenario['tool'] == 'get_all_users':
                users = result if isinstance(result, list) else []
                print(f"🤖 Gemini Response: Found {len(users)} users in the system")
                for user in users:
                    print(f"   - {user.get('name', 'Unknown')} (ID: {user.get('id', 'N/A')}, Email: {user.get('email', 'N/A')})")
            elif scenario['tool'] == 'get_app_statistics':
                print(f"🤖 Gemini Response: Application Statistics:")
                print(f"   - Total Users: {result.get('total_users', 0)}")
                print(f"   - Total Tasks: {result.get('total_tasks', 0)}")
                print(f"   - Completed Tasks: {result.get('completed_tasks', 0)}")
                print(f"   - Pending Tasks: {result.get('pending_tasks', 0)}")
            elif scenario['tool'] == 'get_pending_tasks':
                tasks = result if isinstance(result, list) else []
                print(f"🤖 Gemini Response: Found {len(tasks)} pending tasks:")
                for task in tasks:
                    print(f"   - {task.get('title', 'Unknown')} (ID: {task.get('id', 'N/A')})")
            else:
                print(f"🤖 Gemini Response: {result}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print()

async def interactive_mode():
    """Interactive mode for testing queries"""
    print("🚀 Interactive Gemini + MCP mode (Simplified)")
    print("Type 'quit' to exit")
    print("=" * 50)
    
    # Available commands mapping
    commands = {
        "health": ("get_health_status", {}),
        "info": ("get_app_info", {}),
        "users": ("get_all_users", {}),
        "stats": ("get_app_statistics", {}),
        "tasks": ("get_pending_tasks", {}),
        "dice": ("roll_dice", {"sides": 6, "count": 1}),
    }
    
    while True:
        query = input("\n💬 Enter your query (or 'help' for commands): ").strip()
        if query.lower() in ['quit', 'exit', 'q']:
            break
        
        if query.lower() == 'help':
            print("Available commands:")
            for cmd, (tool, args) in commands.items():
                print(f"  - {cmd}: {tool}")
            continue
        
        if not query:
            continue
        
        # Try to match query to a command
        matched = False
        for cmd, (tool, args) in commands.items():
            if cmd in query.lower():
                try:
                    result = await call_mcp_tool(tool, **args)
                    print(f"🤖 Response: {result}")
                    matched = True
                    break
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    matched = True
                    break
        
        if not matched:
            print("❌ Command not recognized. Type 'help' for available commands.")

async def main():
    """Main function to demonstrate the integration"""
    
    # Check if API key is set
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  GEMINI_API_KEY not set, running in simulation mode")
        print("   (This is a simplified demo without actual Gemini API calls)")
    else:
        print("✅ GEMINI_API_KEY found")
    
    print("\n🎯 FastAPI + MCP Integration Demo")
    print("=" * 40)
    
    try:
        # Test MCP server connection first
        print("🔍 Testing MCP server connection...")
        health = await mcp_server.get_health_status()
        print(f"✅ FastAPI server is healthy")
        
        # Run the demo
        await simulate_gemini_with_tools()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Make sure the FastAPI server is running on http://localhost:8000")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        asyncio.run(interactive_mode())
    else:
        asyncio.run(main())
