# Import the core Agent class from Google ADK
# This is the main abstraction that wraps an LLM with behavior/instructions
from google.adk.agents import Agent

# Import LiteLLM wrapper to connect ADK with different LLM providers (like Ollama, OpenAI, etc.)
from google.adk.models.lite_llm import LiteLlm


# Define the root agent (entry point of the application)
root_agent = Agent(
    
    # Unique name of the agent (used internally and in UI)
    name="greeting_agent",
    
    # LLM configuration:
    # Using LiteLLM to connect to a locally running Ollama model
    # "ollama_chat/llama3:latest" means:
    # - ollama_chat → provider (Ollama local runtime)
    # - llama3:latest → model name installed locally
    model=LiteLlm(model="ollama_chat/llama3:latest"),
    
    # Short description of what this agent does (metadata, useful for UI/debugging)
    description="Greeting agent using local Ollama model",
    
    # Instruction = system prompt (MOST IMPORTANT PART)
    # This defines the behavior/personality of the agent
    # The LLM will follow this instruction while generating responses
    instruction="""
You are a helpful assistant that greets the user.
Ask for the user's name and greet them by name.
""",
)