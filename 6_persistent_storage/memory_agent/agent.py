from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext


# ===================== TOOLS =====================

def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    reminders = tool_context.state.get("reminders", [])
    reminders.append(reminder)
    tool_context.state["reminders"] = reminders

    return {
        "action": "add_reminder",
        "message": f"Added reminder: {reminder}",
    }


def view_reminders(tool_context: ToolContext) -> dict:
    reminders = tool_context.state.get("reminders", [])

    return {
        "action": "view_reminders",
        "reminders": reminders,
        "count": len(reminders),
    }


def update_reminder(index: int, updated_text: str, tool_context: ToolContext) -> dict:
    reminders = tool_context.state.get("reminders", [])

    if index < 1 or index > len(reminders):
        return {
            "action": "update_reminder",
            "status": "error",
            "message": f"No reminder found at position {index}.",
        }

    old = reminders[index - 1]
    reminders[index - 1] = updated_text
    tool_context.state["reminders"] = reminders

    return {
        "action": "update_reminder",
        "message": f"Updated reminder {index} from '{old}' to '{updated_text}'",
    }


def delete_reminder(index: int, tool_context: ToolContext) -> dict:
    reminders = tool_context.state.get("reminders", [])

    if index < 1 or index > len(reminders):
        return {
            "action": "delete_reminder",
            "status": "error",
            "message": f"No reminder found at position {index}.",
        }

    deleted = reminders.pop(index - 1)
    tool_context.state["reminders"] = reminders

    return {
        "action": "delete_reminder",
        "message": f"Deleted reminder: {deleted}",
    }


def update_user_name(name: str, tool_context: ToolContext) -> dict:
    old_name = tool_context.state.get("user_name", "")
    tool_context.state["user_name"] = name

    return {
        "action": "update_user_name",
        "message": f"Updated your name from '{old_name}' to '{name}'",
    }


# ===================== AGENT =====================

root_agent = Agent(
    name="memory_agent",

    # ✅ FREE local model
    model=LiteLlm(model="ollama_chat/mistral:latest"),

    description="A smart reminder agent with persistent memory",

    instruction="""
You are a friendly assistant that helps manage reminders.

User data is stored in session state (name and reminders).
Use tools to manage this data.

Available tools:
- add_reminder
- view_reminders
- update_reminder
- delete_reminder
- update_user_name

Rules:
- If user says "add reminder" → call add_reminder
- If user says "show/view reminders" → call view_reminders
- If user says "update reminder" → call update_reminder
- If user says "delete/remove reminder" → call delete_reminder
- If user tells their name → call update_user_name
- Always respond politely and clearly
""",

    tools=[
        add_reminder,
        view_reminders,
        update_reminder,
        delete_reminder,
        update_user_name,
    ],
)


# For main.py compatibility
memory_agent = root_agent