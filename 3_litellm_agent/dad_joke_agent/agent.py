import random

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


# FREE LOCAL MODEL (Ollama)
model = LiteLlm(
    model="ollama_chat/mistral:latest"
)


# TOOL
def get_dad_joke():
    """
    Returns a random dad joke.
    """
    jokes = [
        "Why did the chicken cross the road? To get to the other side!",
        "What do you call a belt made of watches? A waist of time.",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
    ]
    return random.choice(jokes)


# AGENT
root_agent = Agent(
    name="dad_joke_agent",
    model=model,
    description="Dad joke agent using local Ollama",
    instruction="""
You are a funny assistant.

IMPORTANT:
- You have ONE tool: get_dad_joke
- When user asks for a joke, call get_dad_joke
- Do NOT write your own joke
- Do NOT call any other tool
- For non-joke questions, answer normally
""",
    tools=[get_dad_joke],
)