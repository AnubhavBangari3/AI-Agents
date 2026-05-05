from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


local_model = LiteLlm(model="ollama_chat/mistral:latest")


system_report_synthesizer = LlmAgent(
    name="SystemReportSynthesizer",
    model=local_model,
    instruction="""
You are a System Report Synthesizer.

Create a concise system health report.

Use available CPU, memory, and disk information from previous agents.

Report format:
Overall Health:
CPU:
Memory:
Disk:
Recommendations:

Keep it clear and professional.
Do not use JSON.
""",
    description="Synthesizes system information into a final report",
)