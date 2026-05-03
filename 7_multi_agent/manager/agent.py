from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.funny_nerd.agent import funny_nerd
from .sub_agents.news_analyst.agent import news_analyst
from .sub_agents.stock_analyst.agent import stock_analyst
from .tools.tools import get_current_time


local_model = LiteLlm(model="ollama_chat/mistral:latest")


root_agent = Agent(
    name="manager",
    model=local_model,
    description="Manager agent that delegates tasks to specialist agents.",
    instruction="""
You are a manager agent.

Your job is to understand the user's request and delegate it to the correct specialist.

Available specialists:
stock_analyst handles stock price questions.
funny_nerd handles nerdy joke questions.
news_analyst handles news questions.

Available direct tool:
get_current_time gives current date and time for a city.

Rules:
For stock questions, delegate to stock_analyst.
For joke questions, delegate to funny_nerd.
For news questions, use news_analyst.
For time questions, use get_current_time.
For general questions, answer directly.
""",
    sub_agents=[
        stock_analyst,
        funny_nerd,
    ],
    tools=[
        AgentTool(news_analyst),
        get_current_time,
    ],
)