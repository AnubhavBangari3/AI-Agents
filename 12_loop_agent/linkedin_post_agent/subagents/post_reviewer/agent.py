from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from .tools import count_characters, exit_loop


local_model = LiteLlm(
    model="ollama_chat/mistral:latest"
)


post_reviewer = LlmAgent(
    name="PostReviewer",
    model=local_model,
    instruction="""
You are a LinkedIn Post Reviewer.

Review this post:

{current_post}

Steps:
1. Use count_characters tool
2. Check professional tone
3. Check no emojis
4. Check no hashtags
5. Check ADK concepts included

If post is bad:
Return improvement feedback.

If post is good:
Call exit_loop
Return:
Post approved.
""",
    tools=[
        count_characters,
        exit_loop,
    ],
    output_key="review_feedback",
)