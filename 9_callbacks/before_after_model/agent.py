import copy
from datetime import datetime
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.adk.models.lite_llm import LiteLlm
from google.genai import types


local_model = LiteLlm(model="ollama_chat/mistral:latest")


def before_model_callback(
    callback_context: CallbackContext,
    llm_request: LlmRequest,
) -> Optional[LlmResponse]:
    """
    Runs before the model is called.
    Used for logging, validation, filtering, or blocking a request.
    """

    state = callback_context.state
    agent_name = callback_context.agent_name

    last_user_message = ""

    if llm_request.contents:
        for content in reversed(llm_request.contents):
            if content.role == "user" and content.parts:
                first_part = content.parts[0]
                if hasattr(first_part, "text") and first_part.text:
                    last_user_message = first_part.text
                    break

    print("=== MODEL REQUEST STARTED ===")
    print(f"Agent: {agent_name}")

    if last_user_message:
        print(f"User message: {last_user_message[:100]}")
        state["last_user_message"] = last_user_message
    else:
        print("User message: <empty>")

    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if last_user_message and "sucks" in last_user_message.lower():
        print("=== REQUEST BLOCKED ===")
        print("Blocked because message contains prohibited word: sucks")

        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part(
                        text=(
                            "I cannot respond to messages containing inappropriate language. "
                            "Please rephrase your request politely."
                        )
                    )
                ],
            )
        )

    state["model_start_time"] = datetime.now()
    print("[BEFORE MODEL] Request approved")

    return None


def after_model_callback(
    callback_context: CallbackContext,
    llm_response: LlmResponse,
) -> Optional[LlmResponse]:
    """
    Runs after the model responds.
    Used for logging, formatting, or modifying model output.
    """

    state = callback_context.state

    print("[AFTER MODEL] Processing response")

    if "model_start_time" in state:
        duration = (datetime.now() - state["model_start_time"]).total_seconds()
        print(f"[AFTER MODEL] Model duration: {duration:.2f} seconds")

    if not llm_response or not llm_response.content or not llm_response.content.parts:
        return None

    response_text = ""

    for part in llm_response.content.parts:
        if hasattr(part, "text") and part.text:
            response_text += part.text

    if not response_text:
        return None

    replacements = {
        "problem": "challenge",
        "Problem": "Challenge",
        "difficult": "complex",
        "Difficult": "Complex",
    }

    modified_text = response_text
    modified = False

    for old_word, new_word in replacements.items():
        if old_word in modified_text:
            modified_text = modified_text.replace(old_word, new_word)
            modified = True

    if not modified:
        return None

    print("[AFTER MODEL] Modified response text")

    modified_parts = [copy.deepcopy(part) for part in llm_response.content.parts]

    for part in modified_parts:
        if hasattr(part, "text") and part.text:
            part.text = modified_text

    return LlmResponse(
        content=types.Content(
            role="model",
            parts=modified_parts,
        )
    )


root_agent = LlmAgent(
    name="content_filter_agent",
    model=local_model,
    description="Free Ollama callback agent for content filtering and response modification",
    instruction="""
You are a helpful assistant.

Your job:
- Answer user questions clearly
- Keep responses concise
- Be friendly and respectful
""",
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)