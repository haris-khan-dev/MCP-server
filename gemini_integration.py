import asyncio
import os
from dotenv import load_dotenv
from fastmcp import Client
import google.generativeai as genai

# Load environment variables
load_dotenv()

async def main():
    """Main function to demonstrate Gemini integration with FastMCP"""
    
    # Initialize Gemini client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable")
        return
    
    genai.configure(api_key=api_key)
    
    # Initialize FastMCP client
    mcp_client = Client("mcp_server.py")
    
    print("🚀 Starting Gemini + FastMCP integration demo...")
    print("=" * 50)
    
    try:
        async with mcp_client:
            # Initialize Gemini model
            model = genai.GenerativeModel(
                "gemini-2.0-flash",
                tools=[mcp_client.session]
            )
            
            # Demo conversations
            demo_queries = [
                "Check the health status of the FastAPI application",
                "Create a new user named 'John Doe' with email 'john@example.com' and age 30",
                "Create a task called 'Learn FastMCP' with description 'Study FastMCP integration'",
                "Roll 3 dice with 6 sides each",
                "Get all users and show me the statistics",
                "Mark the first task as completed",
                "Show me all pending tasks"
            ]
            
            for i, query in enumerate(demo_queries, 1):
                print(f"\n🔍 Query {i}: {query}")
                print("-" * 40)
                
                try:
                    response = await model.agenerate_content_async(query)
                    print(f"🤖 Gemini Response: {response.text}")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                
                print()
                
    except Exception as e:
        print(f"❌ Error connecting to MCP server: {str(e)}")
        print("Make sure the FastAPI server is running on http://localhost:8000")

async def interactive_mode():
    """Interactive mode for testing queries"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable")
        return
    
    genai.configure(api_key=api_key)
    mcp_client = Client("mcp_server.py")
    
    print("🚀 Interactive Gemini + FastMCP mode")
    print("Type 'quit' to exit")
    print("=" * 50)
    
    try:
        async with mcp_client:
            model = genai.GenerativeModel(
                "gemini-2.0-flash",
                tools=[mcp_client.session]
            )
            
            while True:
                query = input("\n💬 Enter your query: ").strip()
                if query.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not query:
                    continue
                
                try:
                    response = await model.agenerate_content_async(query)
                    print(f"🤖 Response: {response.text}")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        asyncio.run(interactive_mode())
    else:
        asyncio.run(main())
