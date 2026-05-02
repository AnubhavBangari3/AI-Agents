from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


root_agent = Agent(
    name="question_ans_agent",
    model=LiteLlm(model="ollama_chat/mistral:latest"),
    description="Question answering agent using local Ollama",
    instruction="""
You are a helpful assistant that answers questions about the user's preferences.

Here is some information about the user:

Name:
Anubhav Bangari

Preferences:
I like Python, React, Django, GenAI, and AI agents.
I am learning Google ADK using free local Ollama models.
I want to build job-ready AI projects.
""",
)