"""Study tools the agent can call. Docstrings are the tool descriptions the model sees."""
from google.genai import types
from prompts import EXPLAIN_PROMPT, SUMMARISE_PROMPT, QUESTIONS_PROMPT


def build_tools(client, model, image_bytes, mime_type):
    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

    def _run(instruction, focus):
        response = client.models.generate_content(
            model=model,
            contents=[image_part, f"{instruction}\nStudent's focus: {focus}"],
            config=types.GenerateContentConfig(temperature=0.2),
        )
        return response.text or "The tool returned no text."

    def explain(focus: str) -> str:
        """Explain the concept shown in the study image. Use this for requests such as
        'explain', 'what is this', 'help me understand', or when the request is unclear.
        Args:
            focus: what the student wants explained.
        """
        return _run(EXPLAIN_PROMPT, focus)

    def summarise(focus: str) -> str:
        """Summarise the study image into short key points. Use this when the student asks
        for a summary, key points, or a quick revision note.
        Args:
            focus: what the student wants summarised.
        """
        return _run(SUMMARISE_PROMPT, focus)

    def practice_questions(focus: str) -> str:
        """Write practice questions with answers based on the study image. Use this when the
        student asks for questions, a quiz, or practice.
        Args:
            focus: the topic to write questions about.
        """
        return _run(QUESTIONS_PROMPT, focus)

    return [explain, summarise, practice_questions]
