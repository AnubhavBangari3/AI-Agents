from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from .tools import get_cpu_info


local_model = LiteLlm(model="ollama_chat/mistral:latest")


cpu_info_agent = LlmAgent(
    name="CpuInfoAgent",
    model=local_model,
    instruction="""
You are a CPU Information Agent.

Use get_cpu_info to collect CPU data.

Return a short CPU report:
CPU cores
Average CPU usage
High usage warning if usage is above 80 percent

Do not make up data.
""",
    description="Gathers and analyzes CPU information",
    tools=[get_cpu_info],
    output_key="cpu_info",
)