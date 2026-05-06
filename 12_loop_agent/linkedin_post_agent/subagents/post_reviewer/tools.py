from typing import Any, Dict

from google.adk.tools.tool_context import ToolContext


def count_characters(text: str, tool_context: ToolContext) -> Dict[str, Any]:

    char_count = len(text)

    MIN_LENGTH = 800
    MAX_LENGTH = 1300

    print(f"\nCharacter Count: {char_count}\n")

    if char_count < MIN_LENGTH:

        tool_context.state["review_status"] = "fail"

        return {
            "result": "fail",
            "message": f"Post too short. Need at least {MIN_LENGTH} characters.",
        }

    elif char_count > MAX_LENGTH:

        tool_context.state["review_status"] = "fail"

        return {
            "result": "fail",
            "message": f"Post too long. Maximum {MAX_LENGTH} characters.",
        }

    else:

        tool_context.state["review_status"] = "pass"

        return {
            "result": "pass",
            "message": "Character count looks good.",
        }


def exit_loop(tool_context: ToolContext) -> Dict[str, Any]:

    print("\nEXITING LOOP\n")

    tool_context.actions.escalate = True

    return {}