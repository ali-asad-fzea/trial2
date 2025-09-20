#!/usr/bin/env python3
"""
Simple Working Demo - ADK+A2A Autonomous Debit Card Replacement

This demonstrates the complete autonomous workflow using HTTP requests directly
to the A2A agent endpoints.
"""

import asyncio
import httpx
import json


async def demo_autonomous_workflow():
    """
    Demonstrate autonomous agent workflow using direct HTTP to A2A endpoints.
    """
    print("🎯 AUTONOMOUS DEBIT CARD REPLACEMENT SYSTEM")
    print("=" * 60)
    print("🤖 Google ADK + A2A Protocol Demo")
    print("🎫 Direct HTTP A2A Communication")
    print("=" * 60)
    
    service_url = "http://localhost:8001"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Step 1: Get agent card to verify service is running
            print(f"\n🔗 Checking service agent at {service_url}...")
            
            card_response = await client.get(f"{service_url}/.well-known/agent-card.json")
            card_data = card_response.json()
            
            print(f"✅ Found agent: {card_data['name']}")
            print(f"📋 Description: {card_data['description']}")
            
            # Step 2: Send autonomous card replacement request via A2A
            print("\n🤖 User Agent: Sending autonomous card replacement request...")
            
            # Autonomous message with all required details
            message_payload = {
                "jsonrpc": "2.0",
                "id": "autonomous-request-1",
                "method": "message/send",
                "params": {
                    "id": "card-replacement-001",
                    "message": {
                        "messageId": "msg-001",
                        "role": "user",
                        "parts": [
                            {
                                "type": "text",
                                "text": """Hello! I need to request a debit card replacement. Here are all my details:

Last 4 digits of card: 4829
Cardholder name: John Smith
Address: 123 Main Street, Anytown, NY 12345
Reason for replacement: lost

Please process my replacement request and issue a ticket. Thank you!"""
                            }
                        ]
                    }
                }
            }
            
            print("📤 Sending A2A JSON-RPC message...")
            print(f"💬 Message: 'Card replacement request with all details provided'")
            
            # Send A2A message
            response = await client.post(
                service_url,  # Post to root, not /a2a
                json=message_payload,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"\n⏳ Processing with ADK service agent...")
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n📥 Service Agent Response:")
                print(f"✅ Status: {result.get('result', {}).get('status', 'Unknown')}")
                
                # Extract the actual response content
                if 'result' in result and 'artifacts' in result['result']:
                    artifacts = result['result']['artifacts']
                    if artifacts:
                        for artifact in artifacts:
                            if 'parts' in artifact:
                                for part in artifact['parts']:
                                    if part.get('type') == 'text':
                                        print(f"💬 Agent says: {part['text']}")
                
                print(f"\n🎉 AUTONOMOUS INTERACTION COMPLETED!")
                print("🎯 Summary:")
                print("  • User provided all required card details autonomously")
                print("  • Service agent processed the request using Google ADK")
                print("  • Communication used A2A JSON-RPC protocol")
                print("  • No human intervention was required during the process")
                print("  • The entire workflow was automated end-to-end")
                
                return True
            else:
                print(f"❌ Request failed with status: {response.status_code}")
                print(f"💬 Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("💡 Make sure the service agent is running on port 8001")
        return False


if __name__ == "__main__":
    print("🚀 Starting Simple ADK+A2A Autonomous Demo...")
    
    # Run the autonomous demonstration
    success = asyncio.run(demo_autonomous_workflow())
    
    if success:
        print("\n✅ DEMO COMPLETED SUCCESSFULLY!")
        print("🎯 The autonomous debit card replacement system demonstrated:")
        print("  • Google ADK agent with custom tools")
        print("  • A2A protocol communication") 
        print("  • Autonomous multi-agent interaction")
        print("  • Complete workflow without human intervention")
    else:
        print("\n❌ Demo failed. Check the errors above.")


