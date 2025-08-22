# telcom_sre_agent/tools/ticketing_system_interface_tool.py
import json
import uuid
from typing import Any, Dict, Optional
import datetime
from google.adk.tools.base_tool import ToolContext

# Sample data (replace with real data or integration in a real implementation)
_sample_tickets = []

def create_ticket(
    issue_type: str,
    description: str,
    device_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> str:
    """
    Creates a trouble ticket in the ticketing system.

    Args:
        issue_type: The type of the issue (e.g., "device_down", "high_latency").
        description: A detailed description of the issue.
        device_id: The ID of the affected device, if applicable.

    Returns:
        A dictionary containing the created ticket ID formatted as a JSON string.
    """
    print(
        f"create_ticket called with: issue_type={issue_type}, description={description}, device_id={device_id}"
    )
    ticket_id = str(uuid.uuid4())
    ticket = {
        "ticket_id": ticket_id,
        "issue_type": issue_type,
        "description": description,
        "device_id": device_id,
        "status": "open",
        "created_at": datetime.datetime.now().isoformat(),
    }
    _sample_tickets.append(ticket)
    print(f"Ticket created: {ticket}")
    return json.dumps({"ticket_id": ticket_id})

def escalate_ticket(
    ticket_id: str,
    oncall_engineer: str,
    tool_context: Optional[ToolContext] = None,
) -> str:
    """
    Escalates a ticket to an on-call engineer.

    Args:
        ticket_id: The ID of the ticket to escalate.
        oncall_engineer: The name or ID of the on-call engineer.

    Returns:
        A message indicating the ticket has been escalated.
    """
    print(
        f"escalate_ticket called with: ticket_id={ticket_id}, oncall_engineer={oncall_engineer}"
    )
    for ticket in _sample_tickets:
        if ticket["ticket_id"] == ticket_id:
            ticket["status"] = "escalated"
            ticket["assigned_to"] = oncall_engineer
            print(f"Ticket {ticket_id} escalated to {oncall_engineer}")
            return f"Ticket {ticket_id} escalated to {oncall_engineer}"
    print(f"Ticket not found: {ticket_id}")
    return "Ticket not found"