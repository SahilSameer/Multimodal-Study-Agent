# Multimodal Study Agent

A Python application that accepts an image of study material and a request. A multimodal
model reads the image and an agent chooses one of three tools: **explain**, **summarise**
or **practice_questions**.

## Setup
1. `python -m venv venv` then activate it (Windows: `venv\Scripts\activate`)
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and put your Gemini API key in it (never commit `.env`).
4. `streamlit run app.py`

## Files
- `app.py` – Streamlit interface
- `agent.py` – agent controller (model chooses and calls tools)
- `tools.py` – the three study tools
- `image_utils.py` – image validation and resizing
- `prompts.py` – system instruction and tool prompts

## Limitations
Answers depend on the model and the image quality and can contain mistakes.
This is a learning project, not a production system.
