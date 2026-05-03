from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from .sub_agents.course_support_agent.agent import course_support_agent
from .sub_agents.order_agent.agent import order_agent
from .sub_agents.policy_agent.agent import policy_agent
from .sub_agents.sales_agent.agent import sales_agent


local_model = LiteLlm(model="ollama_chat/mistral:latest")


root_agent = Agent(
    name="customer_service",
    model=local_model,
    description="Customer service agent for AI Developer Accelerator community",
    instruction="""
You are the primary customer service agent.

Your job is to understand the user request and route it to the correct specialist agent.

Specialist agents:
policy_agent handles policy, refund policy, community rules, privacy, and code usage questions.
sales_agent handles course purchase questions and buying the AI Marketing Platform course.
course_support_agent handles course content questions.
order_agent handles purchase history and refund requests.

Routing rules:
If user asks about policies, rules, refund policy, privacy, or code usage, route to policy_agent.
If user wants to buy the course or asks about price, route to sales_agent.
If user asks about course sections, course content, or learning help, route to course_support_agent.
If user asks about purchase history, owned courses, or refund processing, route to order_agent.
If unsure, ask one short clarification question.

Keep responses professional and helpful.
""",
    sub_agents=[
        policy_agent,
        sales_agent,
        course_support_agent,
        order_agent,
    ],
)

customer_service_agent = root_agent