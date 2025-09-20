#!/usr/bin/env python3
"""
Simplified ADK+A2A Demo for Autonomous Debit Card Replacement

This demonstrates the core concept: autonomous agent-to-agent communication
for debit card replacement using Google ADK and A2A protocol.
"""

import asyncio
import httpx
import time
from a2a.client import A2AClient, A2ACardResolver


async def demo_autonomous_interaction():
    """
    Demonstrate autonomous interaction between user and service agents.
    """
    print("🎯 AUTONOMOUS DEBIT CARD REPLACEMENT DEMO")
    print("=" * 50)
    print("🤖 Google ADK + A2A Protocol")
    print("🎫 Autonomous Agent-to-Agent Communication")
    print("=" * 50)
    
    # Service agent endpoint
    service_url = "http://localhost:8001"
    
    try:
        print(f"\n🔗 Connecting to service agent at {service_url}...")
        
        # Create httpx client
        async with httpx.AsyncClient() as http_client:
            # Create A2A card resolver
            card_resolver = A2ACardResolver(base_url=service_url, httpx_client=http_client)
            agent_card = await card_resolver.get_agent_card()
            
            print(f"✅ Found agent: {agent_card.name}")
            print(f"📋 Description: {agent_card.description}")
            
            # Create A2A client
            a2a_client = A2AClient(httpx_client=http_client, agent_card=agent_card, url=service_url)
            
            print("✅ Connected to service agent via A2A protocol")
            
            # Autonomous user message with all required details
            user_message = """
            Hello, I need to request a debit card replacement. Here are all my details:
            
            Last 4 digits of card: 4829
            Cardholder name: John Smith
            Address: 123 Main Street, Anytown, NY 12345  
            Reason for replacement: lost
            
            Please process my replacement request immediately.
            """
            
            print("\n🤖 User Agent: Sending autonomous card replacement request...")
            print(f"📤 Message: {user_message}")
            
            # Send message to service agent
            print("\n⏳ Processing with service agent...")
            response = await a2a_client.send_message(user_message)
            
            print(f"\n📥 Service Agent Response:")
            print(f"✅ {response}")
            
            print(f"\n🎉 AUTONOMOUS INTERACTION COMPLETED!")
            print("🎯 Summary:")
            print("  • User agent provided all required details autonomously")
            print("  • Service agent validated and processed the request")  
            print("  • No human intervention was required")
            print("  • Communication used A2A protocol with Google ADK")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("💡 Make sure the service agent is running on port 8001")
        return False


if __name__ == "__main__":
    print("🚀 Starting ADK+A2A Autonomous Demo...")
    
    # Run the autonomous demonstration
    success = asyncio.run(demo_autonomous_interaction())
    
    if success:
        print("\n✅ Demo completed successfully!")
    else:
        print("\n❌ Demo failed. Check the errors above.")