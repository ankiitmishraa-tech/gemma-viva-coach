import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Gemma Viva Partner", page_icon="🎓", layout="centered")

st.title("🎓 Gemma Concept & Viva Drill")
st.caption("A rapid-fire technical viva partner powered by Google's open-weight Gemma model.")

# Sidebar API key
api_key = st.sidebar.text_input("Enter Gemini/Gemma API Key", type="password")
st.sidebar.markdown("[Get free API Key from Google AI Studio](https://aistudio.google.com/)")

if not api_key:
    st.info("👈 Please enter your API key in the sidebar to start practicing.")
    st.stop()

client = genai.Client(api_key=api_key)

# Topic selector
topic = st.sidebar.selectbox(
    "Choose Subject:",
    ["Computer Networks & Security", "Data Structures & Algorithms", "Operating Systems", "Aptitude & General Studies"]
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Answer here or type 'Start' to begin the viva..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    sys_instruction = f"""
    You are a strict yet helpful technical viva examiner specializing in '{topic}'.
    Your goal is to test the student's conceptual clarity one question at a time.
    Rules:
    1. If the user says 'Start', ask the first crisp conceptual question.
    2. When the user answers, evaluate immediately:
       - State whether it is Correct, Partially Correct, or Needs Work.
       - Give a 1-2 sentence concise correction if needed.
       - Immediately ask the NEXT sequential follow-up question.
    3. Keep responses compact and rapid-fire (under 4-5 sentences).
    """

    history = [m["content"] for m in st.session_state.messages]

    try:
        response = client.models.generate_content(
            model="gemma-2-9b-it",
            contents=history,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction,
                temperature=0.7,
            )
        )
        reply = response.text
    except Exception as e:
        reply = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
