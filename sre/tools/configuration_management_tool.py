# telcom_sre_agent/tools/configuration_management_tool.py
from google.adk.tools.base_tool import ToolContext
from typing import Any, Dict, Optional
import json

# Sample 5G core network configuration data (simplified)
_sample_configs = {
    "AMF_1": {
        "plmn_id": "310-410",
        "amf_name": "AMF_1",
        "s_nssais": ["010101", "020202"],
    },
    "SMF_1": {
        "s_nssai": "010101",
        "dnn": "internet",
        "pdu_session_types": ["IPv4", "IPv6"],
    },
    "gNB_1": {
        "mcc": "310",
        "mnc": "410",
        "nci": "0x000000010",
        "id_length": 32,
    },
    "UE_1": {"supi": "SUPI-1111111111", "5g_guti": "GUTI-1234567890"},
    "UE_2": {"supi": "SUPI-2222222222", "5g_guti": "GUTI-0987654321"},
}

def get_entity_config(
    entity_id: str, tool_context: Optional[ToolContext] = None
) -> str:
    """
    Retrieves the configuration of a network entity.

    Args:
        entity_id: The ID of the network entity (e.g., "AMF_1", "gNB_1", "UE_1").

    Returns:
        A dictionary containing the entity's configuration formatted as a JSON string,
        or an error message if the entity is not found.
    """
    print(f"get_entity_config called with: entity_id={entity_id}")
    if entity_id in _sample_configs:
        config_data = _sample_configs[entity_id]
        print(f"Config found for {entity_id}: {config_data}")
        return json.dumps(config_data)

    error_message = f"Config not found for entity_id: {entity_id}"
    print(error_message)
    return json.dumps({"error": error_message})

def update_entity_config(
    entity_id: str,
    config_updates: Dict[str, Any],
    tool_context: Optional[ToolContext] = None,
) -> str:
    """
    Updates the configuration of a network entity (not implemented in this example).

    Args:
        entity_id: The ID of the entity to update.
        config_updates: A dictionary containing the configuration updates.

    Returns:
        A message indicating whether the update was successful (not implemented).
    """
    print(
        f"update_entity_config called with: entity_id={entity_id}, config_updates={config_updates}"
    )
    error_message = (
        f"Configuration updates are not supported in this demo for entity_id: {entity_id}"
    )
    print(error_message)
    return json.dumps({"error": error_message})