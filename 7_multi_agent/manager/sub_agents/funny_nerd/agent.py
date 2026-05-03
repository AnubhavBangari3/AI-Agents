from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext


local_model = LiteLlm(model="ollama_chat/mistral:latest")


def get_nerd_joke(topic: str, tool_context: ToolContext) -> dict:
    """
    Returns a nerdy joke for the given topic.
    Also saves the last joke topic in session state.
    """

    jokes = {
        "python": "Why do Python programmers prefer snakes? Because they love indentation.",
        "javascript": "Why did the JavaScript developer go broke? Because he used up all his cache.",
        "java": "Why do Java developers wear glasses? Because they cannot C sharp.",
        "programming": "Why do programmers prefer dark mode? Because light attracts bugs.",
        "math": "Why was the equal sign so humble? Because it knew it was not less than or greater than anyone.",
        "physics": "Why did the photon check into a hotel? Because it was travelling light.",
        "chemistry": "Why did the acid go to the gym? To become a buffer solution.",
        "biology": "Why did the cell go to therapy? Because it had too many issues.",
        "default": "Why did the computer go to the doctor? Because it had a virus.",
    }

    selected_topic = topic.lower()
    joke = jokes.get(selected_topic, jokes["default"])

    tool_context.state["last_joke_topic"] = topic

    return {
        "status": "success",
        "topic": topic,
        "joke": joke,
    }


funny_nerd = Agent(
    name="funny_nerd",
    model=local_model,
    description="Agent that tells nerdy jokes.",
    instruction="""
You are a funny nerd agent.

When the user asks for a nerdy joke, use get_nerd_joke.

Supported topics:
python
javascript
java
programming
math
physics
chemistry
biology

If no topic is given, use programming as the topic.

Return the joke clearly.
""",
    tools=[get_nerd_joke],
)