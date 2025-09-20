"""
Debit Card Replacement Service Agent using Google ADK

This agent handles debit card replacement requests by validating user information
and issuing replacement tickets. It uses Google ADK with A2A protocol.
"""

import os
import random
import string
from typing import Dict, Any
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("API key is missing. Please set it in the .env file.")


# Tool for validating card information
def validate_card_details(
    last_four_digits: str,
    cardholder_name: str,
    address: str,
    replacement_reason: str
) -> Dict[str, Any]:
    """
    Validates debit card replacement request details.
    
    Args:
        last_four_digits: Last 4 digits of the card
        cardholder_name: Name on the card
        address: Cardholder's address
        replacement_reason: Reason for replacement (lost, stolen, damaged, expired)
    
    Returns:
        Dict with validation status and details
    """
    # Validation logic
    errors = []
    
    # Validate last 4 digits
    if not last_four_digits or len(last_four_digits) != 4 or not last_four_digits.isdigit():
        errors.append("Last 4 digits must be exactly 4 numeric characters")
    
    # Validate cardholder name
    if not cardholder_name or len(cardholder_name.strip()) < 2:
        errors.append("Cardholder name must be at least 2 characters")
    
    # Validate address
    if not address or len(address.strip()) < 10:
        errors.append("Address must be at least 10 characters")
    
    # Validate replacement reason
    valid_reasons = ["lost", "stolen", "damaged", "expired"]
    if not replacement_reason or replacement_reason.lower() not in valid_reasons:
        errors.append(f"Replacement reason must be one of: {', '.join(valid_reasons)}")
    
    if errors:
        return {
            "valid": False,
            "errors": errors,
            "status": "validation_failed"
        }
    
    return {
        "valid": True,
        "last_four_digits": last_four_digits,
        "cardholder_name": cardholder_name.strip(),
        "address": address.strip(),
        "replacement_reason": replacement_reason.lower(),
        "status": "validated"
    }


def issue_replacement_ticket(
    last_four_digits: str,
    cardholder_name: str,
    address: str,
    replacement_reason: str
) -> Dict[str, Any]:
    """
    Issues a replacement ticket for a validated debit card request.
    
    Args:
        last_four_digits: Last 4 digits of the card
        cardholder_name: Name on the card
        address: Cardholder's address
        replacement_reason: Reason for replacement
    
    Returns:
        Dict with ticket information
    """
    # Generate ticket ID
    ticket_id = "TICKET-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # Estimate processing time based on reason
    processing_days = {
        "lost": 3,
        "stolen": 1,  # Priority processing
        "damaged": 2,
        "expired": 5
    }
    
    days = processing_days.get(replacement_reason.lower(), 3)
    
    return {
        "ticket_id": ticket_id,
        "status": "issued",
        "cardholder_name": cardholder_name,
        "last_four_digits": last_four_digits,
        "replacement_reason": replacement_reason,
        "estimated_processing_days": days,
        "message": f"Replacement ticket {ticket_id} issued successfully. New card will arrive in {days} business days."
    }


# Create function tools
# validate_tool = FunctionTool(validate_card_details)
# ticket_tool = FunctionTool(issue_replacement_ticket)

import os
import random
import string
from typing import Dict, Any
from google.adk import Agent
# from google.adk.core import tool
from google.adk.a2a.utils.agent_to_a2a import to_a2a


# Tool for validating card information
# @tool
def validate_card_details(
    last_four_digits: str,
    cardholder_name: str,
    address: str,
    replacement_reason: str
) -> Dict[str, Any]:
    """
    Validates debit card replacement request details.
    
    Args:
        last_four_digits: Last 4 digits of the card
        cardholder_name: Name on the card
        address: Cardholder's address
        replacement_reason: Reason for replacement (lost, stolen, damaged, expired)
    
    Returns:
        Dict with validation status and details
    """
    # Validation logic
    errors = []
    
    # Validate last 4 digits
    if not last_four_digits or len(last_four_digits) != 4 or not last_four_digits.isdigit():
        errors.append("Last 4 digits must be exactly 4 numeric characters")
    
    # Validate cardholder name
    if not cardholder_name or len(cardholder_name.strip()) < 2:
        errors.append("Cardholder name must be at least 2 characters")
    
    # Validate address
    if not address or len(address.strip()) < 10:
        errors.append("Address must be at least 10 characters")
    
    # Validate replacement reason
    valid_reasons = ["lost", "stolen", "damaged", "expired"]
    if not replacement_reason or replacement_reason.lower() not in valid_reasons:
        errors.append(f"Replacement reason must be one of: {', '.join(valid_reasons)}")
    
    if errors:
        return {
            "valid": False,
            "errors": errors,
            "status": "validation_failed"
        }
    
    return {
        "valid": True,
        "last_four_digits": last_four_digits,
        "cardholder_name": cardholder_name.strip(),
        "address": address.strip(),
        "replacement_reason": replacement_reason.lower(),
        "status": "validated"
    }


# @tool
def issue_replacement_ticket(
    last_four_digits: str,
    cardholder_name: str,
    address: str,
    replacement_reason: str
) -> Dict[str, Any]:
    """
    Issues a replacement ticket for a validated debit card request.
    
    Args:
        last_four_digits: Last 4 digits of the card
        cardholder_name: Name on the card
        address: Cardholder's address
        replacement_reason: Reason for replacement
    
    Returns:
        Dict with ticket information
    """
    # Generate ticket ID
    ticket_id = "TICKET-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # Estimate processing time based on reason
    processing_days = {
        "lost": 3,
        "stolen": 1,  # Priority processing
        "damaged": 2,
        "expired": 5
    }
    
    days = processing_days.get(replacement_reason.lower(), 3)
    
    return {
        "ticket_id": ticket_id,
        "status": "issued",
        "cardholder_name": cardholder_name,
        "last_four_digits": last_four_digits,
        "replacement_reason": replacement_reason,
        "estimated_processing_days": days,
        "message": f"Replacement ticket {ticket_id} issued successfully. New card will arrive in {days} business days."
    }


# Create the service agent - in ADK, tools are passed as functions directly
service_agent = Agent(
    name="debit_card_service_agent",
    model="gemini-2.0-flash",  # Updated model
    description="Debit Card Replacement Service Agent that validates requests and issues replacement tickets",
    instruction="""
    You are a professional debit card replacement service agent. Your role is to:
    
    1. Collect required information for card replacement:
       - Last 4 digits of the card
       - Cardholder's full name
       - Current address
       - Reason for replacement (lost, stolen, damaged, expired)
    
    2. Validate all provided information using the validate_card_details tool
    
    3. If validation passes, issue a replacement ticket using issue_replacement_ticket tool
    
    4. Provide clear confirmation with ticket details
    
    Always be professional, efficient, and helpful. If any information is missing or invalid, 
    clearly explain what is needed.
    """,
    tools=[validate_card_details, issue_replacement_ticket],
    api_key=api_key  # Pass the API key here
)

# Convert to A2A application
service_app = to_a2a(service_agent, port=int(os.getenv('SERVICE_PORT', '8001')))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('SERVICE_PORT', '8001'))
    print(f"Starting Debit Card Service Agent on port {port}")
    uvicorn.run(service_app, host="0.0.0.0", port=port)