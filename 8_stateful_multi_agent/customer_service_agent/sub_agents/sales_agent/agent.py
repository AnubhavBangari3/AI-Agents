from datetime import datetime

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext


local_model = LiteLlm(model="ollama_chat/mistral:latest")


def purchase_course(tool_context: ToolContext) -> dict:
    course_id = "ai_marketing_platform"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    current_purchased_courses = tool_context.state.get("purchased_courses", [])

    course_ids = [
        course["id"]
        for course in current_purchased_courses
        if isinstance(course, dict) and "id" in course
    ]

    if course_id in course_ids:
        return {
            "status": "error",
            "message": "You already own this course.",
        }

    new_purchased_courses = []

    for course in current_purchased_courses:
        if isinstance(course, dict) and "id" in course:
            new_purchased_courses.append(course)

    new_purchased_courses.append(
        {
            "id": course_id,
            "purchase_date": current_time,
        }
    )

    tool_context.state["purchased_courses"] = new_purchased_courses

    current_interaction_history = tool_context.state.get("interaction_history", [])
    new_interaction_history = current_interaction_history.copy()

    new_interaction_history.append(
        {
            "action": "purchase_course",
            "course_id": course_id,
            "timestamp": current_time,
        }
    )

    tool_context.state["interaction_history"] = new_interaction_history

    return {
        "status": "success",
        "message": "Successfully purchased the AI Marketing Platform course.",
        "course_id": course_id,
        "timestamp": current_time,
    }


sales_agent = Agent(
    name="sales_agent",
    model=local_model,
    description="Sales agent for the AI Marketing Platform course",
    instruction="""
You are a sales agent for the Fullstack AI Marketing Platform course.

Course details:
Name: Fullstack AI Marketing Platform
Price: 149 dollars
Value: Learn to build AI powered marketing automation apps
Includes: 6 weeks of group support and weekly coaching calls

Rules:
If user asks about the course, explain value clearly.
If user wants to buy the course, call purchase_course.
If user already owns the course, tell them they already have access.
If user asks about course content after purchase, direct them to course_support_agent.
Be helpful but not pushy.
""",
    tools=[purchase_course],
)