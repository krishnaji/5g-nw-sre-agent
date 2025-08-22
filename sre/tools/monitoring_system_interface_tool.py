# telcom_sre_agent/tools/monitoring_system_interface_tool.py
from google.adk.tools.base_tool import ToolContext
from google.genai import types
from typing import Any, Dict, Optional
import json

# Sample 5G core network data (replace with real data or integration)
_sample_events = [
    {
        "timestamp": "2024-02-29T10:00:00.000Z",
        "source": "gNB_1",
        "destination": "AMF_1",
        "message_type": "NAS_Registration_Request",
        "transaction_id": "1001",
        "device_id": "SUPI-1111111111",
        "message_content": {
            "registration_type": "initial_registration",
            "capability": "5G_capable_device",
        },
        "result_code": "pending",
    },
    {
        "timestamp": "2024-02-29T10:00:00.050Z",
        "source": "AMF_1",
        "destination": "UDM_1",
        "message_type": "Authentication_Request",
        "transaction_id": "1001",
        "device_id": "SUPI-1111111111",
        "message_content": {"auth_type": "5G_AKA"},
        "result_code": "pending",
    },
    {
        "timestamp": "2024-02-29T10:00:00.100Z",
        "source": "UDM_1",
        "destination": "AMF_1",
        "message_type": "Authentication_Response",
        "transaction_id": "1001",
        "device_id": "SUPI-1111111111",
        "message_content": {"auth_vector": "random_auth_vector_data"},
        "result_code": "success",
    },
    {
        "timestamp": "2024-02-29T10:00:00.500Z",
        "source": "gNB_2",
        "destination": "AMF_1",
        "message_type": "NAS_Registration_Request",
        "transaction_id": "1002",
        "device_id": "SUPI-2222222222",
        "message_content": {
            "registration_type": "initial_registration",
            "capability": "5G_capable_device",
        },
        "result_code": "pending",
    },
    {
        "timestamp": "2024-02-29T10:00:00.600Z",
        "source": "AMF_1",
        "destination": "UE_2",
        "message_type": "NAS_Authentication_Reject",
        "transaction_id": "1002",
        "device_id": "SUPI-2222222222",
        "result_code": "authentication_failure",
        "reason": "Invalid credentials",
    },
]

_sample_network_entities = {
    "gNB_1": {"type": "gNodeB", "status": "up", "location": "Region A"},
    "AMF_1": {"type": "AMF", "status": "up", "location": "Core Network"},
    "UDM_1": {"type": "UDM", "status": "up", "location": "Core Network"},
    "SMF_1": {"type": "SMF", "status": "up", "location": "Core Network"},
    "UE_1": {"type": "UE", "status": "registered", "device_id": "SUPI-1111111111"},
    "UE_2": {"type": "UE", "status": "authentication_failed", "device_id": "SUPI-2222222222"},
}

def get_events(
    message_type: Optional[str] = None,
    result_code: Optional[str] = None,
    transaction_id: Optional[str] = None,
    device_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> str:
    """
    Retrieves events from the monitoring system based on different criteria.

    Args:
        message_type: The type of message to filter by (e.g., "NAS_Registration_Request", "Authentication_Response").
        result_code: The result code to filter by (e.g., "success", "pending", "authentication_failure").
        transaction_id: The transaction ID to filter by.
        device_id: The device ID (SUPI or network entity ID) to filter by.

    Returns:
        A list of event dictionaries formatted as a JSON string.
    """
    print(
        f"get_events called with: message_type={message_type}, result_code={result_code},"
        f" transaction_id={transaction_id}, device_id={device_id}"
    )
    filtered_events = _sample_events

    if message_type:
        filtered_events = [
            event
            for event in filtered_events
            if event["message_type"] == message_type
        ]

    if result_code:
        filtered_events = [
            event
            for event in filtered_events
            if event.get("result_code") == result_code
        ]

    if transaction_id:
        filtered_events = [
            event
            for event in filtered_events
            if event["transaction_id"] == transaction_id
        ]

    if device_id:
        filtered_events = [
            event for event in filtered_events if event["device_id"] == device_id
        ]

    print(f"Filtered events: {filtered_events}")
    return json.dumps(filtered_events)

def get_network_entity_status(
    entity_id: str, tool_context: Optional[ToolContext] = None
) -> str:
    """
    Retrieves the status of a network entity (UE, gNB, AMF, etc.).

    Args:
        entity_id: The ID of the network entity (e.g., "UE_1", "AMF_1", "gNB_2").

    Returns:
        A dictionary containing the network entity's status information formatted as a JSON string,
        or an error message if the entity is not found.
    """
    print(f"get_network_entity_status called with entity_id: {entity_id}")

    if entity_id in _sample_network_entities:
        entity_data = _sample_network_entities[entity_id]
        print(f"Network entity found: {entity_data}")
        return json.dumps(entity_data)
    
    # check if entity_id is a SUPI
    for event in _sample_events:
        if event["device_id"] == entity_id:
            print(f"Device found using SUPI: {event}")
            return json.dumps(event)

    error_message = f"Network entity not found for entity_id: {entity_id}"
    print(error_message)
    return json.dumps({"error": error_message})