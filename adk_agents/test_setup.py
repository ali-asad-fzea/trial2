"""
Simple test to verify Google ADK and A2A setup
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# Load environment variables from .env file
load_dotenv()


def get_card_info() -> str:
    """Get card information for testing."""
    return "Card 4829 - John Smith - 123 Main St - Lost"


# Check API key before creating agent
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is required. Please set it in the .env file.")

# Simple test agent
test_agent = Agent(
    name="test_agent",
    model="gemini-2.5-flash-lite",
    description="Test agent for ADK setup verification",
    instruction="You are a test agent. When asked about card info, use the get_card_info tool.",
    tools=[get_card_info]
)

async def test_agent_basic():
    """Test basic agent functionality."""
    print("🧪 Testing Google ADK Agent...")
    
    try:
        # Test the A2A conversion
        a2a_app = to_a2a(test_agent, port=8099)
        print(f"✅ A2A conversion successful: {type(a2a_app)}")
        return True
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Set minimal environment with a valid API key
    os.environ['GOOGLE_API_KEY'] = 'AIzaSyAnj6KhxAsBLXD4YFU97CqZVqu0AfwhMYQ'
    
    print("🔧 Testing ADK Setup...")
    result = asyncio.run(test_agent_basic())
    
    if result:
        print("✅ ADK setup verified!")
    else:
        print("❌ ADK setup issues detected")