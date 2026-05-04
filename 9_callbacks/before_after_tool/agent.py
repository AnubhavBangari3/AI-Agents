import copy
from typing import Optional, Dict, Any

from google.adk.agents import LlmAgent
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.adk.models.lite_llm import LiteLlm


local_model = LiteLlm(model="ollama_chat/mistral:latest")


def get_capital_city(country: str) -> dict:
    data = {
        "india": "New Delhi",
        "usa": "Washington DC",
        "france": "Paris",
    }
    return {"result": data.get(country.lower(), "Not found")}


def before_tool_callback(tool: BaseTool, args: Dict[str, Any], ctx: ToolContext):
    print("Before tool:", tool.name, args)

    if args.get("country", "").lower() == "merica":
        args["country"] = "usa"

    return None


def after_tool_callback(tool: BaseTool, args: Dict[str, Any], ctx: ToolContext, res: Dict):
    print("After tool:", res)

    if "washington" in res.get("result", "").lower():
        new_res = copy.deepcopy(res)
        new_res["result"] += " (USA capital)"
        return new_res

    return None


root_agent = LlmAgent(
    name="tool_callback_agent",
    model=local_model,
    instruction="Find capital using tool.",
    tools=[get_capital_city],
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)