from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from .tools import get_memory_info


local_model = LiteLlm(model="ollama_chat/mistral:latest")


memory_info_agent = LlmAgent(
    name="MemoryInfoAgent",
    model=local_model,
    instruction="""
You are a Memory Information Agent.

Use get_memory_info to collect RAM and swap data.

Return a short memory report:
Total memory
Available memory
Used memory
Swap usage
High usage warning if memory usage is above 80 percent

Do not make up data.
""",
    description="Gathers and analyzes memory information",
    tools=[get_memory_info],
    output_key="memory_info",
)