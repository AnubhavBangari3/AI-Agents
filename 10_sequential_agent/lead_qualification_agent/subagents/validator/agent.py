from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

local_model = LiteLlm(model="ollama_chat/mistral:latest")

lead_validator_agent = LlmAgent(
    name="LeadValidatorAgent",
    model=local_model,
    description="Validates lead information",
    instruction="""
You are a Lead Validation AI.

Check if the lead has:
name
email or phone
need or intent

Return only one short plain text line.

Allowed outputs:
valid
invalid: missing contact information
invalid: missing name
invalid: missing need
""",
    output_key="validation_status",
)