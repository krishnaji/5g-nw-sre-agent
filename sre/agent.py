import logging
import os
import json
from dotenv import load_dotenv
from google.genai import types
import asyncio

from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from .sre_agents.triage_agent import triage_agent
from .sre_agents.pinpoint_agent import pinpoint_agent
from .sre_agents.test_agent import test_agent

from graphviz import Digraph

 


# for Pub/Sub
from google.cloud import pubsub_v1
from google.api_core.exceptions import NotFound

# Load environment variables
load_dotenv()

# Configure logging
# logging.basicConfig(level=logging.INFO)
# add color to logging
import coloredlogs, logging

coloredlogs.install(level=logging.INFO)

# Initialize session service using the framework's InMemorySessionService
session_service = InMemorySessionService()

artifact_service = InMemoryArtifactService()

# Initialize root agent
root_agent = Agent(
    name="RootAgent",
    description="Orchestrates the SRE agents.",
    instruction="You are a 5G Network SRE Agent",
    model="gemini-2.5-flash",
    sub_agents=[triage_agent,pinpoint_agent, test_agent],
)