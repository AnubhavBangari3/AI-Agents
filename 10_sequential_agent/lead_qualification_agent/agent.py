from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

local_model = LiteLlm(model="ollama_chat/mistral:latest")

root_agent = LlmAgent(
    name="lead_pipeline",
    model=local_model,
    instruction="""
You are a lead qualification system.

Steps:
1. Check if lead is valid
2. Score from 1 to 10
3. Suggest next action

Return in plain text like:

Validation: valid
Score: 8
Action: Schedule a demo call
"""
)