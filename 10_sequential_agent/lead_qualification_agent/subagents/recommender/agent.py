from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

local_model = LiteLlm(model="ollama_chat/mistral:latest")

action_recommender_agent = LlmAgent(
    name="ActionRecommenderAgent",
    model=local_model,
    description="Recommends next actions",
    instruction="""
You are a sales assistant.

Give one short next-action recommendation.

Rules:
If the lead looks incomplete, ask for missing details.
If the lead looks weak, suggest nurturing.
If the lead looks medium, suggest a discovery call.
If the lead looks strong, suggest scheduling a demo.

Return plain text only.
Do not use JSON.
Do not use bullet points.
""",
    output_key="action_recommendation",
)