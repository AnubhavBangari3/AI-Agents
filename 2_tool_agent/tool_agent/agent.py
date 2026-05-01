from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


def get_current_time(city: str) -> str:
    """
    Get current time for a city.
    """
    return f"The current time in {city} is 10:00 AM. This is a demo response."


root_agent = Agent(
    name="current_time_agent",
    model=LiteLlm(model="ollama_chat/mistral:latest"),
    description="A simple time tool agent using Ollama.",
    instruction="""
You are a helpful assistant.

You have only one tool:
get_current_time(city)

Rules:
- Call get_current_time only when the user asks for current time.
- Do not call any other tool.
- Do not call answer.
- Do not call current_time_agent.
- For normal questions, reply directly in plain text.
- After using the tool once, stop and give the final answer.
""",
    tools=[get_current_time],
)