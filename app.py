"""Multimodal Study Agent - Streamlit interface. Run: streamlit run app.py"""
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

from agent import run_agent
from image_utils import prepare_image, ImageError

load_dotenv()
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

st.set_page_config(page_title="Multimodal Study Agent", page_icon="📚", layout="centered")
st.title("📚 Multimodal Study Agent")
st.caption("Upload an image of your study material, ask for help, and the agent picks the right study tool.")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY is missing. Copy .env.example to .env and add your key.")
    st.stop()

uploaded = st.file_uploader("Upload a photo or screenshot (PNG, JPG, WEBP)", type=["png", "jpg", "jpeg", "webp"])
request = st.text_input("What do you need?", placeholder="e.g. Explain this diagram / Give me practice questions")

image_ready = None
if uploaded is not None:
    try:
        jpeg_bytes, mime, pil_img = prepare_image(uploaded.getvalue())
        st.image(pil_img, caption="Image that will be sent to the model", use_container_width=True)
        image_ready = (jpeg_bytes, mime)
    except ImageError as e:
        st.warning(str(e))

if st.button("Ask the agent", type="primary"):
    if image_ready is None:
        st.warning("Please upload a valid image first.")
    elif not request.strip():
        st.warning("Please type what you need.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            with st.spinner("The agent is reading the image..."):
                answer, tools_used = run_agent(client, MODEL, image_ready[0], image_ready[1], request.strip())
            st.subheader("Response")
            st.markdown(answer)
            st.info("Tool used by the agent: " + (", ".join(tools_used) if tools_used else "none (answered directly)"))
        except Exception as e:
            st.error(f"The model service returned an error. Please try again. Details: {e}")

st.divider()
st.caption("AI answers can contain mistakes. Check important facts against your textbook or notes.")
