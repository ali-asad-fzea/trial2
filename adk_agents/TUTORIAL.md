# Autonomous Multi-Agent System Tutorial
## Google ADK + A2A Protocol for Debit Card Replacement

This tutorial walks you through building a complete autonomous multi-agent system using Google's Agent Development Kit (ADK) and Agent-to-Agent (A2A) protocol for automated debit card replacement requests.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [System Architecture](#system-architecture)
4. [Setup Instructions](#setup-instructions)
5. [Understanding the Components](#understanding-the-components)
6. [Running the System](#running-the-system)
7. [How It Works](#how-it-works)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Concepts](#advanced-concepts)

## 🎯 Overview

This project demonstrates a **fully autonomous multi-agent system** where:
- A **User Agent** automatically provides all required information
- A **Service Agent** processes the request using Google ADK
- Communication happens via **A2A protocol** (JSON-RPC over HTTP)
- **No human intervention** is required during the entire workflow

### What You'll Learn
- How to use Google ADK to build intelligent agents
- How to implement A2A protocol for agent communication
- How to create autonomous workflows between agents
- How to handle API key management securely
- How to build tools and functions for agents

## 🛠️ Prerequisites

- Python 3.8+
- Google Cloud API key for Gemini models
- Basic understanding of:
  - Python programming
  - HTTP requests and JSON-RPC
  - Asynchronous programming (async/await)

## 🏗️ System Architecture

```
┌─────────────────┐    A2A Protocol     ┌─────────────────┐
│   User Agent    │ ──────────────────► │  Service Agent  │
│  (Simulated)    │   JSON-RPC/HTTP     │   (Google ADK)  │
└─────────────────┘                     └─────────────────┘
        │                                        │
        │ Provides:                              │ Uses:
        │ • Card last 4 digits                  │ • validate_card_details
        │ • Cardholder name                     │ • issue_replacement_ticket
        │ • Address                             │ • Gemini-2.5-flash-lite
        │ • Replacement reason                  │
        └────────────────────────────────────────┘
```

## 🚀 Setup Instructions

### Step 1: Install Dependencies

```bash
# Install required packages
pip install google-adk python-dotenv httpx uvicorn
```

### Step 2: Set Up API Key

1. Get a Google API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Create a `.env` file in your project root:

```bash
# .env file
GOOGLE_API_KEY=your_actual_api_key_here
```

### Step 3: Project Structure

Your project should look like this:

```
adk_agents/
├── service_agent.py      # ADK-based service agent
├── final_demo.py         # Autonomous workflow demo
├── test_setup.py         # Setup verification
├── a2a_client.py         # A2A communication utilities
├── user_agent.py         # User agent simulation
├── demo_client.py        # Alternative demo client
├── run_demo.py          # Demo runner script
├── README.md            # Project documentation
└── TUTORIAL.md          # This tutorial
```

## 🧩 Understanding the Components

### 1. Service Agent (`service_agent.py`)

This is the core Google ADK agent that processes debit card replacement requests.

**Key Features:**
- Uses Google's Gemini-2.5-flash-lite model
- Has custom tools for validation and ticket issuance
- Converts to A2A protocol using `to_a2a()` utility
- Runs as HTTP server on port 8001

**Tools Available:**
```python
def validate_card_details(last_four_digits, cardholder_name, address, replacement_reason):
    # Validates all provided information
    # Returns validation status and cleaned data

def issue_replacement_ticket(last_four_digits, cardholder_name, address, replacement_reason):
    # Creates replacement ticket with unique ID
    # Estimates processing time based on reason
```

### 2. Demo Client (`final_demo.py`)

This simulates a user agent that autonomously provides all required information.

**Autonomous Workflow:**
1. Discovers service agent via agent card
2. Constructs A2A JSON-RPC message with all details
3. Sends HTTP request to service agent
4. Processes response and displays results

### 3. Environment Configuration

Uses `python-dotenv` for secure API key management:

```python
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
```

## 🏃 Running the System

### Method 1: Full Autonomous Demo

1. **Start the Service Agent:**
```bash
cd adk_agents
python service_agent.py
```

2. **In another terminal, run the demo:**
```bash
cd adk_agents
python final_demo.py
```

### Method 2: Test Setup Verification

```bash
cd adk_agents
python test_setup.py
```

### Expected Output

```
🎯 AUTONOMOUS DEBIT CARD REPLACEMENT SYSTEM
============================================================
🤖 Google ADK + A2A Protocol Demo
🎫 Direct HTTP A2A Communication
============================================================

🔗 Checking service agent at http://localhost:8001...
✅ Found agent: debit_card_service_agent
📋 Description: Debit Card Replacement Service Agent...

🤖 User Agent: Sending autonomous card replacement request...
📤 Sending A2A JSON-RPC message...
💬 Message: 'Card replacement request with all details provided'

⏳ Processing with ADK service agent...

📥 Service Agent Response:
✅ Status: success
💬 Agent says: Replacement ticket TICKET-ABC12345 issued successfully...

🎉 AUTONOMOUS INTERACTION COMPLETED!
```

## ⚙️ How It Works

### 1. Agent Creation (Google ADK)

```python
service_agent = Agent(
    name="debit_card_service_agent",
    model="gemini-2.5-flash-lite",
    description="Debit Card Replacement Service Agent...",
    instruction="You are a professional debit card replacement service agent...",
    tools=[validate_card_details, issue_replacement_ticket],
    api_key=api_key
)
```

### 2. A2A Conversion

```python
service_app = to_a2a(service_agent, port=8001)
```

This converts the ADK agent into an A2A-compatible HTTP server that:
- Exposes agent card at `/.well-known/agent-card.json`
- Accepts JSON-RPC messages at the root endpoint
- Handles message routing and tool execution

### 3. Autonomous Communication

The user agent sends a structured JSON-RPC message:

```python
message_payload = {
    "jsonrpc": "2.0",
    "id": "autonomous-request-1",
    "method": "message/send",
    "params": {
        "id": "card-replacement-001",
        "message": {
            "messageId": "msg-001",
            "role": "user",
            "parts": [{
                "type": "text",
                "text": "Hello! I need to request a debit card replacement..."
            }]
        }
    }
}
```

### 4. Tool Execution

The service agent:
1. Receives the message
2. Extracts card details from the text
3. Calls `validate_card_details` tool
4. If valid, calls `issue_replacement_ticket` tool
5. Returns structured response

## 🔧 Troubleshooting

### Common Issues

1. **API Key Error:**
```
400 INVALID_ARGUMENT. API key not valid
```
**Solution:** Check your `.env` file and ensure the API key is correct.

2. **Connection Refused:**
```
Connection refused to localhost:8001
```
**Solution:** Make sure `service_agent.py` is running first.

3. **Import Errors:**
```
ModuleNotFoundError: No module named 'google.adk'
```
**Solution:** Install Google ADK: `pip install google-adk`

4. **Experimental Warnings:**
```
[EXPERIMENTAL] to_a2a: ADK Implementation for A2A support...
```
**Solution:** These are expected warnings for experimental features.

### Debug Mode

Add debug logging to see detailed communication:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Advanced Concepts

### 1. Custom Tools

You can create custom tools for your agents:

```python
def custom_tool(param1: str, param2: int) -> dict:
    """
    Custom tool description for the agent.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2
    
    Returns:
        Dict with results
    """
    # Your custom logic here
    return {"result": "success"}

# Add to agent
agent = Agent(
    name="custom_agent",
    tools=[custom_tool],
    # ... other parameters
)
```

### 2. Multiple Agents

You can run multiple agents on different ports:

```python
# Agent 1
agent1 = to_a2a(service_agent, port=8001)

# Agent 2
agent2 = to_a2a(another_agent, port=8002)
```

### 3. Complex Workflows

Chain multiple agent interactions:

```python
async def complex_workflow():
    # Step 1: Agent A processes initial request
    response1 = await call_agent_a(data)
    
    # Step 2: Agent B processes Agent A's output
    response2 = await call_agent_b(response1)
    
    # Step 3: Final processing
    return process_final_result(response2)
```

### 4. Error Handling

Implement robust error handling:

```python
try:
    response = await client.post(service_url, json=payload)
    if response.status_code == 200:
        result = response.json()
        # Process success
    else:
        # Handle HTTP errors
        print(f"HTTP Error: {response.status_code}")
except Exception as e:
    # Handle network/other errors
    print(f"Error: {e}")
```

## 🎯 Next Steps

1. **Extend the System:**
   - Add more validation rules
   - Implement different card types
   - Add email notifications

2. **Production Deployment:**
   - Add authentication
   - Implement rate limiting
   - Add monitoring and logging

3. **Scale the Architecture:**
   - Multiple service agents
   - Load balancing
   - Database integration

4. **Security Enhancements:**
   - Encrypt sensitive data
   - Add audit trails
   - Implement role-based access

## 📚 Resources

- [Google ADK Documentation](https://github.com/google-ai-edge/adk)
- [A2A Protocol Specification](https://github.com/google/agent-to-agent)
- [Gemini API Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)

## 🤝 Contributing

Feel free to extend this tutorial with:
- Additional use cases
- Performance optimizations
- Security improvements
- Testing strategies

---

**Happy coding! 🚀**

This tutorial demonstrates the power of combining Google ADK with A2A protocol to create truly autonomous multi-agent systems. The possibilities are endless!