from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


local_model = LiteLlm(
    model="ollama_chat/mistral:latest"
)


initial_post_generator = LlmAgent(
    name="InitialPostGenerator",
    model=local_model,
    instruction="""
You are a LinkedIn Post Generator.

Generate a professional LinkedIn post about learning Agent Development Kit (ADK).

Requirements:
- Mention AI agents
- Mention tools
- Mention memory
- Mention multi-agent systems
- Mention parallel and loop agents
- Mention practical AI applications
- Mention @aiwithbrandon
- Professional tone
- No emojis
- No hashtags
- Around 1000 characters

Return ONLY the post.
""",
    output_key="current_post",
)