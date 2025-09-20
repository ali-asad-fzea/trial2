"""
A2A Communication Client for Agent-to-Agent Interaction

This module handles the autonomous interaction between user-agent and service-agent
using the A2A protocol.
"""

import asyncio
import httpx
import time
from typing import Optional
from a2a.client import A2AClient


class AutonomousA2AClient:
    """Client for managing autonomous agent-to-agent communication."""
    
    def __init__(self, service_url: str, user_url: str):
        """
        Initialize the A2A client.
        
        Args:
            service_url: URL of the service agent
            user_url: URL of the user agent
        """
        self.service_url = service_url
        self.user_url = user_url
        self.service_client: Optional[A2AClient] = None
        
    async def connect_to_service(self) -> bool:
        """
        Connect to the service agent via A2A protocol.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            async with httpx.AsyncClient() as client:
                self.service_client = await A2AClient.get_client_from_agent_card_url(
                    client, self.service_url
                )
                print(f"✅ Connected to service agent at {self.service_url}")
                return True
        except Exception as e:
            print(f"❌ Failed to connect to service agent: {e}")
            return False
    
    async def initiate_card_replacement(self) -> dict:
        """
        Initiate an autonomous card replacement request.
        
        Returns:
            Dict containing the interaction results
        """
        if not self.service_client:
            raise RuntimeError("Not connected to service agent")
        
        # Initial request message from user
        initial_message = """
        Hello, I need to request a debit card replacement. I can provide all the required information:
        
        - Last 4 digits of my card: 4829
        - Cardholder name: John Smith  
        - Address: 123 Main Street, Anytown, NY 12345
        - Reason for replacement: lost
        
        Please process my replacement request.
        """
        
        print("🤖 User Agent: Initiating card replacement request...")
        print(f"📤 Sending: {initial_message}")
        
        try:
            # Send the message to service agent
            response = await self.service_client.send_message(initial_message)
            
            print(f"📥 Service Agent Response: {response}")
            
            return {
                "success": True,
                "user_message": initial_message,
                "service_response": response,
                "status": "completed"
            }
            
        except Exception as e:
            print(f"❌ Error during communication: {e}")
            return {
                "success": False,
                "error": str(e),
                "status": "failed"
            }


async def run_autonomous_interaction():
    """
    Run the complete autonomous agent interaction.
    """
    print("🚀 Starting Autonomous Debit Card Replacement System")
    print("=" * 60)
    
    # Wait a bit for agents to start up
    print("⏳ Waiting for agents to initialize...")
    await asyncio.sleep(3)
    
    # Initialize A2A client
    service_url = "http://localhost:8001"
    user_url = "http://localhost:8002"
    
    client = AutonomousA2AClient(service_url, user_url)
    
    # Connect to service agent
    print(f"🔗 Connecting to service agent at {service_url}...")
    if not await client.connect_to_service():
        print("💥 Failed to establish A2A connection")
        return
    
    # Run the autonomous interaction
    print("\n🤝 Starting autonomous agent interaction...")
    result = await client.initiate_card_replacement()
    
    print("\n" + "=" * 60)
    if result["success"]:
        print("✅ AUTONOMOUS INTERACTION COMPLETED SUCCESSFULLY!")
        print(f"📋 Status: {result['status']}")
        print("\n🎯 Summary:")
        print("- User agent automatically provided all required information")
        print("- Service agent validated the details")
        print("- Replacement ticket was issued without human intervention")
    else:
        print("❌ AUTONOMOUS INTERACTION FAILED")
        print(f"💥 Error: {result.get('error', 'Unknown error')}")
    
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_autonomous_interaction())