# FastAPI + MCP + Gemini Integration

This project demonstrates how to integrate a FastAPI application with Google's Gemini AI using a simplified MCP (Model Context Protocol) server implementation.

## 🏗️ Architecture

- **FastAPI App** (`app.py`): A sample REST API with user management, task management, and dice rolling
- **Simple MCP Server** (`simple_mcp_server.py`): Simplified MCP server that exposes FastAPI endpoints as tools
- **Gemini Integration** (`simple_gemini_integration.py`): Connects Gemini AI with the MCP server

## 🚀 Features

### FastAPI Application
- User management (CRUD operations)
- Task management with completion tracking
- Dice rolling functionality
- Health checks and statistics
- RESTful API endpoints

### MCP Server Tools
- `get_health_status()`: Check application health
- `get_app_info()`: Get application information
- `get_all_users()`: Retrieve all users
- `create_user()`: Create new users
- `get_user_by_id()`: Get specific user
- `get_all_tasks()`: Retrieve all tasks
- `create_task()`: Create new tasks
- `complete_task()`: Mark tasks as completed
- `roll_dice()`: Roll dice with custom parameters
- `get_app_statistics()`: Get application statistics
- `search_users_by_name()`: Search users by name
- `get_pending_tasks()`: Get incomplete tasks
- `get_completed_tasks()`: Get completed tasks

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API key (optional - demo works in simulation mode)
- Basic Python packages (fastapi, uvicorn, aiohttp, google-generativeai)

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn aiohttp google-generativeai python-dotenv requests
   ```

3. **Set up environment variables (optional):**
   Create a `.env` file and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
   Note: The demo works without an API key in simulation mode.

4. **Get a Gemini API key:**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

## 🎯 Usage

### 1. Start the FastAPI Server

```bash
python app.py
```

The FastAPI server will run on `http://localhost:8000`

### 2. Test the FastAPI Endpoints

You can test the API directly:

```bash
# Health check
curl http://localhost:8000/health

# Get app info
curl http://localhost:8000/

# Create a user
curl -X POST "http://localhost:8000/users?name=John&email=john@example.com&age=30"

# Create a task
curl -X POST "http://localhost:8000/tasks?title=Learn%20FastMCP&description=Study%20FastMCP%20integration"

# Roll dice
curl "http://localhost:8000/dice/roll?sides=6&count=3"
```

### 3. Run the Gemini Integration

#### Demo Mode (Predefined Queries)
```bash
python simple_gemini_integration.py
```

#### Interactive Mode
```bash
python simple_gemini_integration.py --interactive
```

#### Automated Demo
```bash
python start_simple_demo.py
```

### 4. Example Gemini Queries

In interactive mode, you can ask questions like:

- "Check the health status of the FastAPI application"
- "Create a new user named 'Alice' with email 'alice@example.com' and age 25"
- "Create a task called 'Learn Python' with description 'Study Python programming'"
- "Roll 5 dice with 10 sides each"
- "Show me all users and get the application statistics"
- "Mark the first task as completed"
- "Show me all pending tasks"

## 🔧 Configuration

### FastAPI Server
- Default port: 8000
- Host: 0.0.0.0 (accessible from all interfaces)
- Modify `app.py` to change these settings

### MCP Server
- Connects to FastAPI server at `http://localhost:8000`
- Modify `API_BASE_URL` in `mcp_server.py` if needed

### Gemini Integration
- Uses Gemini 2.0 Flash model
- Configure API key via environment variable
- Modify model settings in `gemini_integration.py`

## 📁 Project Structure

```
.
├── app.py                        # FastAPI application
├── simple_mcp_server.py         # Simplified MCP server with tools
├── simple_gemini_integration.py # Gemini + MCP integration
├── start_simple_demo.py         # Automated startup script
├── test_simple_integration.py   # Integration testing
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore file
└── README.md                    # This file
```

## 🧪 Testing

### Test FastAPI Endpoints
```bash
# Start the server
python app.py

# In another terminal, test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/users
curl http://localhost:8000/tasks
```

### Test MCP Server
```bash
python simple_mcp_server.py
```

### Test Gemini Integration
```bash
# Make sure FastAPI server is running
python app.py

# In another terminal, run integration
python simple_gemini_integration.py
```

### Test Everything
```bash
python test_simple_integration.py
```

## 🔍 Troubleshooting

### Common Issues

1. **"Please set GEMINI_API_KEY environment variable"**
   - Make sure you have a `.env` file with your API key
   - Check that the API key is valid

2. **"Error connecting to MCP server"**
   - Ensure the FastAPI server is running on port 8000
   - Check that all dependencies are installed

3. **"ModuleNotFoundError"**
   - Run `pip install -r requirements.txt`
   - Make sure you're using Python 3.8+

### Debug Mode

To see more detailed error messages, you can modify the integration script to include more logging.

## 🚀 Next Steps

- Add more FastAPI endpoints
- Create additional MCP tools
- Implement authentication
- Add database persistence
- Create a web interface
- Deploy to cloud platforms

## 📚 Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastMCP Documentation](https://fastmcp.dev/)
- [Google Gemini API](https://ai.google.dev/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.
