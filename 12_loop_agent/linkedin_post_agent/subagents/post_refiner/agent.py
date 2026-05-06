from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


local_model = LiteLlm(
    model="ollama_chat/mistral:latest"
)


post_refiner = LlmAgent(
    name="PostRefinerAgent",
    model=local_model,
    instruction="""
You are a LinkedIn Post Refiner.

Current Post:
{current_post}

Feedback:
{review_feedback}

Improve the post using feedback.

Requirements:
- Professional tone
- No emojis
- No hashtags
- Mention ADK concepts
- Around 1000 characters

Return ONLY refined post.
""",
    output_key="current_post",
)