# telcom_sre_agent/tools/network_topology_tool.py
from google.adk.tools.base_tool import ToolContext
from typing import Any, Dict, Optional
import json

# Sample 5G core network topology (simplified)
_sample_topology = {
    "Region A": {
        "gNB_1": ["AMF_1"],
        "AMF_1": ["gNB_1", "UDM_1", "SMF_1"],
        "UDM_1": ["AMF_1"],
        "SMF_1": ["AMF_1"],
    },
    "Region B": {
        "gNB_2": ["AMF_1"],
        "AMF_1": ["gNB_2", "UDM_1", "SMF_1"],
        "UDM_1": ["AMF_1"],
        "SMF_1": ["AMF_1"],
    },
}

def get_entity_neighbors(
    entity_id: str, tool_context: Optional[ToolContext] = None
) -> str:
    """
    Retrieves the direct neighbors of a network entity in the topology.

    Args:
        entity_id: The ID of the network entity.

    Returns:
        A list of network entity IDs that are direct neighbors, formatted as a JSON string,
        or an error message if the entity is not found in the topology.
    """
    print(f"get_entity_neighbors called with: entity_id={entity_id}")
    neighbors = []
    for region, entities in _sample_topology.items():
        if entity_id in entities:
            neighbors.extend(entities[entity_id])

    if neighbors:
        print(f"Neighbors found for {entity_id}: {neighbors}")
        return json.dumps(neighbors)
    else:
        error_message = f"Network entity not found in topology: {entity_id}"
        print(error_message)
        return json.dumps({"error": error_message})

def get_path_between_entities(
    source_entity_id: str,
    destination_entity_id: str,
    tool_context: Optional[ToolContext] = None,
) -> str:
    """
    Finds a path between two network entities in the topology (simplified).

    Args:
        source_entity_id: The ID of the source network entity.
        destination_entity_id: The ID of the destination network entity.

    Returns:
        A list of network entity IDs representing a path, formatted as a JSON string,
        or an error message if no path is found.
    """
    print(
        f"get_path_between_entities called with: source_entity_id={source_entity_id},"
        f" destination_entity_id={destination_entity_id}"
    )

    if source_entity_id == destination_entity_id:
        return json.dumps([source_entity_id])

    # Very basic pathfinding for demo
    for region, entities in _sample_topology.items():
        if source_entity_id in entities and destination_entity_id in entities:
            if destination_entity_id in entities[source_entity_id]:
                path = [source_entity_id, destination_entity_id]
                print(f"Path found: {path}")
                return json.dumps(path)
            else:
                for intermediate in entities[source_entity_id]:
                    if destination_entity_id in entities.get(intermediate, []):
                        path = [source_entity_id, intermediate, destination_entity_id]
                        print(f"Path found: {path}")
                        return json.dumps(path)

    error_message = (
        f"No path found between {source_entity_id} and {destination_entity_id}"
    )
    print(error_message)
    return json.dumps({"error": error_message})