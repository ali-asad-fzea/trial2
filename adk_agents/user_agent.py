"""
Autonomous User Agent using Google ADK

This agent acts as a client that autonomously provides all required information
for debit card replacement without human intervention.
"""

import os
from typing import Dict, Any
from google.adk import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a


# Simulated user profile - in real scenario this could come from a secure database
USER_PROFILE = {
    "cardholder_name": "John Smith",
    "last_four_digits": "4829",
    "address": "123 Main Street, Anytown, NY 12345",
    "replacement_reason": "lost",
    "phone": "(555) 123-4567",
    "email": "john.smith@email.com"
}


def get_card_details() -> Dict[str, str]:
    """
    Retrieves card details for replacement request.
    
    Returns:
        Dict containing card information
    """
    return {
        "last_four_digits": USER_PROFILE["last_four_digits"],
        "cardholder_name": USER_PROFILE["cardholder_name"],
        "address": USER_PROFILE["address"],
        "replacement_reason": USER_PROFILE["replacement_reason"]
    }


def get_contact_info() -> Dict[str, str]:
    """
    Retrieves contact information for the cardholder.
    
    Returns:
        Dict containing contact details
    """
    return {
        "phone": USER_PROFILE["phone"],
        "email": USER_PROFILE["email"]
    }

import os
import asyncio
import httpx
from typing import Dict, Any
from google.adk import Agent
# from google.adk.core import tool
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from a2a.client import A2AClient


# Simulated user profile - in real scenario this could come from a secure database
USER_PROFILE = {
    "cardholder_name": "John Smith",
    "last_four_digits": "4829",
    "address": "123 Main Street, Anytown, NY 12345",
    "replacement_reason": "lost",
    "phone": "(555) 123-4567",
    "email": "john.smith@email.com"
}


# @tool
def get_card_details() -> Dict[str, str]:
    """
    Retrieves card details for replacement request.
    
    Returns:
        Dict containing card information
    """
    return {
        "last_four_digits": USER_PROFILE["last_four_digits"],
        "cardholder_name": USER_PROFILE["cardholder_name"],
        "address": USER_PROFILE["address"],
        "replacement_reason": USER_PROFILE["replacement_reason"]
    }


# @tool
def get_contact_info() -> Dict[str, str]:
    """
    Retrieves contact information for the cardholder.
    
    Returns:
        Dict containing contact details
    """
    return {
        "phone": USER_PROFILE["phone"],
        "email": USER_PROFILE["email"]
    }


# @tool
async def contact_service_agent(service_url: str, message: str) -> Dict[str, Any]:
    """
    Contacts the debit card service agent via A2A protocol.
    
    Args:
        service_url: URL of the service agent
        message: Message to send to the service agent
    
    Returns:
        Response from the service agent
    """
    try:
        async with httpx.AsyncClient() as client:
            a2a_client = await A2AClient.get_client_from_agent_card_url(client, service_url)
            response = await a2a_client.send_message(message)
            
            return {
                "success": True,
                "response": response,
                "status": "message_sent"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "status": "communication_failed"
        }


# Create the user agent - in ADK, tools are passed as functions directly
user_agent = Agent(
    name="autonomous_user_agent",
    model="gemini-2.0-flash", 
    description="Autonomous user agent that handles debit card replacement requests without human intervention",
    instruction="""
    You are an autonomous user agent that needs to request a debit card replacement. Your goal is to:
    
    1. Provide all required information automatically when requested:
       - Last 4 digits of the card: 4829
       - Cardholder's full name: John Smith
       - Current address: 123 Main Street, Anytown, NY 12345
       - Reason for replacement: lost
    
    2. Respond to any follow-up questions or requests for clarification
    
    3. Confirm receipt of the replacement ticket
    
    You have access to tools to get card details and contact information. Use them when needed.
    Always be responsive and provide complete, accurate information.
    
    When the conversation starts, immediately provide all the required details proactively.
    """,
    tools=[get_card_details, get_contact_info]
)

# Convert to A2A application  
user_app = to_a2a(user_agent, port=int(os.getenv('USER_PORT', '8002')))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('USER_PORT', '8002'))
    print(f"Starting Autonomous User Agent on port {port}")
    uvicorn.run(user_app, host="0.0.0.0", port=port)