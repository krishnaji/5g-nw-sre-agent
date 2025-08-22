# telcom_sre_agent/sre_agents/test_agent.py
import json

from google.adk.agents import Agent
from google.adk.tools import ToolContext
from ..tools.network_test_execution_tool import ping_device, traceroute

def run_network_tests(
    test_type: str,
    source_device_id: str,
    target_device_ip: str,
    tool_context: ToolContext,
) -> str:
    """
    Runs network tests based on the specified type.

    Args:
        test_type: The type of test to run (e.g., "ping", "traceroute").
        source_device_id: The ID of the source device.
        target_device_ip: The IP address to test against.

    Returns:
        A JSON string containing the test results.
    """
    if test_type == "ping":
        result = ping_device(source_device_id, target_device_ip)
    elif test_type == "traceroute":
        result = traceroute(source_device_id, target_device_ip)
    else:
        result = json.dumps({"error": f"Unknown test type: {test_type}"})

    return result

test_agent = Agent(
    name="NetworkTestAgent",
    description="Executes network tests like ping and traceroute.",
    instruction="""You are a network testing agent.
- You are given a 'test_type', 'source_device_id', and 'target_device_ip'.
- Use the appropriate tool to perform the requested test: `ping_device` or `traceroute`.
- Return the results of the test to the user.
- when calling ping_device or traceroute, make sure to include all the required arguments that are not marked as optional.
""",
    tools=[ping_device, traceroute],
    model="gemini-2.5-flash",
)