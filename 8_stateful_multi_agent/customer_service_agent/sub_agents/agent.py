from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# Import all sub agents
from .sub_agents.course_support_agent.agent import course_support_agent
from .sub_agents.order_agent.agent import order_agent
from .sub_agents.policy_agent.agent import policy_agent
from .sub_agents.sales_agent.agent import sales_agent


# Use FREE local Ollama model
local_model = LiteLlm(model="ollama_chat/mistral:latest")


# Root Customer Service Agent
root_agent = Agent(
    name="customer_service",
    model=local_model,
    description="Customer service agent for AI Developer Accelerator",
    instruction="""
You are the main customer service agent.

Your job is to understand the user query and route it to the correct agent.

Available agents:

1. policy_agent
Handles:
- refund policy
- community rules
- privacy policy
- course access rules

2. sales_agent
Handles:
- buying course
- course price
- course details

3. course_support_agent
Handles:
- course content
- sections
- technical learning help

4. order_agent
Handles:
- purchase history
- refunds
- order related queries

Routing rules:

- If user asks about refund policy → policy_agent
- If user asks about buying or pricing → sales_agent
- If user asks about course content → course_support_agent
- If user asks about refund or purchase history → order_agent

If not clear:
Ask one simple clarification question.

Important:
Do not answer everything yourself.
Delegate to correct agent.
""",
    sub_agents=[
        policy_agent,
        sales_agent,
        course_support_agent,
        order_agent,
    ],
)

# Required for ADK
customer_service_agent = root_agent