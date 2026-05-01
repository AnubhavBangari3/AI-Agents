from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from pydantic import BaseModel, Field


# Free local Ollama model
model = LiteLlm(model="ollama_chat/mistral:latest")


class EmailContent(BaseModel):
    subject: str = Field(
        description="The subject line of the email. Should be concise and descriptive."
    )
    body: str = Field(
        description="The main content of the email with greeting, paragraphs, and signature."
    )


root_agent = LlmAgent(
    name="email_agent",
    model=model,
    description="Generates professional emails with structured subject and body using Ollama.",
    instruction="""
You are an Email Generation Assistant.

Generate a professional email based on the user's request.

Rules:
- Return ONLY valid JSON.
- Do not add markdown.
- Do not add explanation.
- Do not wrap JSON in ```json.
- The JSON must match exactly this structure:

{
  "subject": "Subject line here",
  "body": "Email body here"
}

Email guidelines:
- Create a concise subject line.
- Write a professional greeting.
- Write clear and concise email content.
- Add an appropriate closing.
- Use "Anubhav" as the signature.
""",
    output_schema=EmailContent,
    output_key="email",
)