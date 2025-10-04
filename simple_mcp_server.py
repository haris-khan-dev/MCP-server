"""
Simple MCP Server implementation without fastmcp dependency
This provides the same functionality as the original mcp_server.py
"""
import asyncio
import aiohttp
import json
from typing import List, Dict, Any, Optional

class SimpleMCPServer:
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.tools = {
            "get_health_status": self.get_health_status,
            "get_app_info": self.get_app_info,
            "get_all_users": self.get_all_users,
            "create_user": self.create_user,
            "get_user_by_id": self.get_user_by_id,
            "get_all_tasks": self.get_all_tasks,
            "create_task": self.create_task,
            "complete_task": self.complete_task,
            "roll_dice": self.roll_dice,
            "get_app_statistics": self.get_app_statistics,
            "search_users_by_name": self.search_users_by_name,
            "get_pending_tasks": self.get_pending_tasks,
            "get_completed_tasks": self.get_completed_tasks,
        }

    async def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to FastAPI server"""
        url = f"{self.api_base_url}{endpoint}"
        async with aiohttp.ClientSession() as session:
            if method.upper() == "GET":
                async with session.get(url) as response:
                    return await response.json()
            elif method.upper() == "POST":
                async with session.post(url, json=data) as response:
                    return await response.json()
            elif method.upper() == "PUT":
                async with session.put(url, json=data) as response:
                    return await response.json()

    async def get_health_status(self) -> Dict[str, Any]:
        """Check the health status of the FastAPI application"""
        return await self.make_request("GET", "/health")

    async def get_app_info(self) -> Dict[str, Any]:
        """Get information about the FastAPI application"""
        return await self.make_request("GET", "/")

    async def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users from the FastAPI application"""
        return await self.make_request("GET", "/users")

    async def create_user(self, name: str, email: str, age: int) -> Dict[str, Any]:
        """Create a new user in the FastAPI application"""
        data = {"name": name, "email": email, "age": age}
        return await self.make_request("POST", "/users", data)

    async def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """Get a specific user by ID from the FastAPI application"""
        return await self.make_request("GET", f"/users/{user_id}")

    async def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks from the FastAPI application"""
        return await self.make_request("GET", "/tasks")

    async def create_task(self, title: str, description: str) -> Dict[str, Any]:
        """Create a new task in the FastAPI application"""
        data = {"title": title, "description": description}
        return await self.make_request("POST", "/tasks", data)

    async def complete_task(self, task_id: int) -> Dict[str, Any]:
        """Mark a task as completed in the FastAPI application"""
        return await self.make_request("PUT", f"/tasks/{task_id}/complete")

    async def roll_dice(self, sides: int = 6, count: int = 1) -> Dict[str, Any]:
        """Roll dice using the FastAPI application"""
        return await self.make_request("GET", f"/dice/roll?sides={sides}&count={count}")

    async def get_app_statistics(self) -> Dict[str, Any]:
        """Get application statistics from the FastAPI application"""
        return await self.make_request("GET", "/stats")

    async def search_users_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search for users by name in the FastAPI application"""
        users = await self.get_all_users()
        return [user for user in users if name.lower() in user.get("name", "").lower()]

    async def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Get all pending (incomplete) tasks from the FastAPI application"""
        tasks = await self.get_all_tasks()
        return [task for task in tasks if not task.get("completed", False)]

    async def get_completed_tasks(self) -> List[Dict[str, Any]]:
        """Get all completed tasks from the FastAPI application"""
        tasks = await self.get_all_tasks()
        return [task for task in tasks if task.get("completed", False)]

    async def call_tool(self, tool_name: str, **kwargs) -> Any:
        """Call a tool by name with arguments"""
        if tool_name in self.tools:
            return await self.tools[tool_name](**kwargs)
        else:
            raise ValueError(f"Tool '{tool_name}' not found")

    def list_tools(self) -> List[str]:
        """List all available tools"""
        return list(self.tools.keys())

# Global server instance
mcp_server = SimpleMCPServer()

if __name__ == "__main__":
    # Simple test runner
    async def test_server():
        print("🧪 Testing Simple MCP Server...")
        
        # Test health check
        try:
            health = await mcp_server.get_health_status()
            print(f"✅ Health check: {health}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return
        
        # Test app info
        try:
            info = await mcp_server.get_app_info()
            print(f"✅ App info: {info.get('message', 'N/A')}")
        except Exception as e:
            print(f"❌ App info failed: {e}")
        
        # Test dice roll
        try:
            dice = await mcp_server.roll_dice(sides=6, count=3)
            print(f"✅ Dice roll: {dice}")
        except Exception as e:
            print(f"❌ Dice roll failed: {e}")
        
        print("🎉 Simple MCP Server test completed!")

    asyncio.run(test_server())
