import asyncio
import aiohttp
import json
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP(name="FastAPI MCP Server")

# Configuration
API_BASE_URL = "http://localhost:8000"

async def make_request(method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
    """Make HTTP request to FastAPI server"""
    url = f"{API_BASE_URL}{endpoint}"
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

@mcp.tool
async def get_health_status() -> Dict[str, Any]:
    """Check the health status of the FastAPI application"""
    return await make_request("GET", "/health")

@mcp.tool
async def get_app_info() -> Dict[str, Any]:
    """Get information about the FastAPI application"""
    return await make_request("GET", "/")

@mcp.tool
async def get_all_users() -> List[Dict[str, Any]]:
    """Get all users from the FastAPI application"""
    return await make_request("GET", "/users")

@mcp.tool
async def create_user(name: str, email: str, age: int) -> Dict[str, Any]:
    """Create a new user in the FastAPI application"""
    data = {"name": name, "email": email, "age": age}
    return await make_request("POST", "/users", data)

@mcp.tool
async def get_user_by_id(user_id: int) -> Dict[str, Any]:
    """Get a specific user by ID from the FastAPI application"""
    return await make_request("GET", f"/users/{user_id}")

@mcp.tool
async def get_all_tasks() -> List[Dict[str, Any]]:
    """Get all tasks from the FastAPI application"""
    return await make_request("GET", "/tasks")

@mcp.tool
async def create_task(title: str, description: str) -> Dict[str, Any]:
    """Create a new task in the FastAPI application"""
    data = {"title": title, "description": description}
    return await make_request("POST", "/tasks", data)

@mcp.tool
async def complete_task(task_id: int) -> Dict[str, Any]:
    """Mark a task as completed in the FastAPI application"""
    return await make_request("PUT", f"/tasks/{task_id}/complete")

@mcp.tool
async def roll_dice(sides: int = 6, count: int = 1) -> Dict[str, Any]:
    """Roll dice using the FastAPI application"""
    return await make_request("GET", f"/dice/roll?sides={sides}&count={count}")

@mcp.tool
async def get_app_statistics() -> Dict[str, Any]:
    """Get application statistics from the FastAPI application"""
    return await make_request("GET", "/stats")

@mcp.tool
async def search_users_by_name(name: str) -> List[Dict[str, Any]]:
    """Search for users by name in the FastAPI application"""
    users = await get_all_users()
    return [user for user in users if name.lower() in user.get("name", "").lower()]

@mcp.tool
async def get_pending_tasks() -> List[Dict[str, Any]]:
    """Get all pending (incomplete) tasks from the FastAPI application"""
    tasks = await get_all_tasks()
    return [task for task in tasks if not task.get("completed", False)]

@mcp.tool
async def get_completed_tasks() -> List[Dict[str, Any]]:
    """Get all completed tasks from the FastAPI application"""
    tasks = await get_all_tasks()
    return [task for task in tasks if task.get("completed", False)]

if __name__ == "__main__":
    mcp.run()
