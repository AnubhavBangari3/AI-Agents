from datetime import datetime
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.lite_llm import LiteLlm
from google.genai import types


local_model = LiteLlm(model="ollama_chat/mistral:latest")


def before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    state = callback_context.state

    if "request_counter" not in state:
        state["request_counter"] = 1
    else:
        state["request_counter"] += 1

    state["start_time"] = datetime.now()

    print("Agent started")
    print(f"Request number: {state['request_counter']}")

    return None


def after_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    state = callback_context.state

    if "start_time" in state:
        duration = (datetime.now() - state["start_time"]).total_seconds()
        print(f"Agent finished in {duration} seconds")

    return None


root_agent = LlmAgent(
    name="before_after_agent",
    model=local_model,
    instruction="You are a friendly assistant.",
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
)