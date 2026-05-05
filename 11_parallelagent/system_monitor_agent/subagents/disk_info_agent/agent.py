from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from .tools import get_disk_info


local_model = LiteLlm(model="ollama_chat/mistral:latest")


disk_info_agent = LlmAgent(
    name="DiskInfoAgent",
    model=local_model,
    instruction="""
You are a Disk Information Agent.

Use get_disk_info to collect disk usage data.

Return a short disk report:
Partitions
Total space
Used space
Overall usage
High usage warning if any partition is above 85 percent

Do not make up data.
""",
    description="Gathers and analyzes disk information",
    tools=[get_disk_info],
    output_key="disk_info",
)