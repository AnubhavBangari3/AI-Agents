from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

local_model = LiteLlm(model="ollama_chat/mistral:latest")

lead_scorer_agent = LlmAgent(
    name="LeadScorerAgent",
    model=local_model,
    description="Scores lead from 1 to 10",
    instruction="""
You are a Lead Scoring AI.

Score the lead from 1 to 10 based on:
budget
urgency
clarity
intent

Return only one number.
Do not use JSON.
Do not explain.
""",
    output_key="lead_score",
)