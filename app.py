from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import random
import datetime
import json

app = FastAPI(title="Sample FastAPI App", version="1.0.0")

# Data models
class User(BaseModel):
    id: int
    name: str
    email: str
    age: int

class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: str

class DiceRoll(BaseModel):
    sides: int
    count: int
    results: List[int]

# In-memory storage (for demo purposes)
users_db = []
tasks_db = []
user_counter = 1
task_counter = 1

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Sample FastAPI App",
        "version": "1.0.0",
        "endpoints": {
            "users": "/users",
            "tasks": "/tasks",
            "dice": "/dice/roll",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}

# User endpoints
@app.get("/users", response_model=List[User])
async def get_users():
    """Get all users"""
    return users_db

@app.post("/users", response_model=User)
async def create_user(name: str, email: str, age: int):
    """Create a new user"""
    global user_counter
    user = User(id=user_counter, name=name, email=email, age=age)
    users_db.append(user)
    user_counter += 1
    return user

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get a specific user by ID"""
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Task endpoints
@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Get all tasks"""
    return tasks_db

@app.post("/tasks", response_model=Task)
async def create_task(title: str, description: str):
    """Create a new task"""
    global task_counter
    task = Task(
        id=task_counter,
        title=title,
        description=description,
        completed=False,
        created_at=datetime.datetime.now().isoformat()
    )
    tasks_db.append(task)
    task_counter += 1
    return task

@app.put("/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    """Mark a task as completed"""
    for task in tasks_db:
        if task.id == task_id:
            task.completed = True
            return {"message": f"Task '{task.title}' marked as completed"}
    raise HTTPException(status_code=404, detail="Task not found")

# Dice rolling endpoint
@app.get("/dice/roll")
async def roll_dice(sides: int = 6, count: int = 1):
    """Roll dice with specified sides and count"""
    if sides < 2 or count < 1:
        raise HTTPException(status_code=400, detail="Invalid dice parameters")
    
    results = [random.randint(1, sides) for _ in range(count)]
    return DiceRoll(sides=sides, count=count, results=results)

# Statistics endpoint
@app.get("/stats")
async def get_stats():
    """Get application statistics"""
    return {
        "total_users": len(users_db),
        "total_tasks": len(tasks_db),
        "completed_tasks": len([t for t in tasks_db if t.completed]),
        "pending_tasks": len([t for t in tasks_db if not t.completed])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
