"""Agent controller: the model chooses a tool, the SDK runs it and returns the result."""
from google.genai import types
from prompts import SYSTEM_INSTRUCTION
from tools import build_tools


def run_agent(client, model, image_bytes, mime_type, request):
    """Return (answer_text, list_of_tool_names_used)."""
    tools = build_tools(client, model, image_bytes, mime_type)
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=tools,                 # automatic function calling is on by default
        temperature=0.2,
    )
    response = client.models.generate_content(
        model=model,
        contents=[types.Part.from_bytes(data=image_bytes, mime_type=mime_type), request],
        config=config,
    )
    used = []
    history = getattr(response, "automatic_function_calling_history", None) or []
    for content in history:
        for part in (content.parts or []):
            call = getattr(part, "function_call", None)
            if call and call.name and call.name not in used:
                used.append(call.name)
    return (response.text or "No answer was returned."), used
