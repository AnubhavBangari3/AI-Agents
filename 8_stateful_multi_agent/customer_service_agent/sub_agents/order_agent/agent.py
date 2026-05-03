from datetime import datetime

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext


local_model = LiteLlm(model="ollama_chat/mistral:latest")


def get_current_time() -> dict:
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def refund_course(tool_context: ToolContext) -> dict:
    course_id = "ai_marketing_platform"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    current_purchased_courses = tool_context.state.get("purchased_courses", [])

    course_ids = [
        course["id"]
        for course in current_purchased_courses
        if isinstance(course, dict) and "id" in course
    ]

    if course_id not in course_ids:
        return {
            "status": "error",
            "message": "You do not own this course, so it cannot be refunded.",
        }

    new_purchased_courses = []

    for course in current_purchased_courses:
        if not isinstance(course, dict):
            continue

        if course.get("id") == course_id:
            continue

        new_purchased_courses.append(course)

    tool_context.state["purchased_courses"] = new_purchased_courses

    current_interaction_history = tool_context.state.get("interaction_history", [])
    new_interaction_history = current_interaction_history.copy()

    new_interaction_history.append(
        {
            "action": "refund_course",
            "course_id": course_id,
            "timestamp": current_time,
        }
    )

    tool_context.state["interaction_history"] = new_interaction_history

    return {
        "status": "success",
        "message": "Successfully refunded the AI Marketing Platform course. Your 149 dollars will be returned to your original payment method within 3 to 5 business days.",
        "course_id": course_id,
        "timestamp": current_time,
    }


order_agent = Agent(
    name="order_agent",
    model=local_model,
    description="Order agent for purchase history and refunds",
    instruction="""
You are the order agent.

Your role:
Help users view purchase history and process refunds.

Course:
ai_marketing_platform means Fullstack AI Marketing Platform.
Price is 149 dollars.

Rules:
If user asks about purchase history, explain based on available state.
If user asks for refund, call refund_course.
If refund is successful, confirm clearly.
If user does not own the course, explain clearly.
Mention 30 day money back guarantee when relevant.
If user asks course content questions, direct them to course_support_agent.
If user asks sales questions, direct them to sales_agent.
""",
    tools=[refund_course, get_current_time],
)