from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


def get_current_time(city: str) -> str:
    return f"The current time in {city} is approx 10:00 AM (demo)."


root_agent = Agent(
    name="current_time_agent",
    model=LiteLlm(model="ollama_chat/llama3:latest"),
    description="Time tool agent",
    instruction="""
You are a helpful assistant.

IMPORTANT:
- You have ONLY ONE tool: get_current_time
- NEVER call any tool unless the user explicitly asks for current time
- NEVER call tools like 'answer' or 'tool_agent'

Behavior:
- If user asks for time → call get_current_time
- Otherwise → just reply normally in text (DO NOT CALL ANY TOOL)
""",
    tools=[get_current_time],
)