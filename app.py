import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Gemma Viva Drill", page_icon="🎯", layout="centered")

st.title("🎯 Gemma Concept & Viva Drill")
st.caption("Built for a friend who needs rapid, interactive interview and conceptual viva practice.")

# Secure API configuration
api_key = st.sidebar.text_input("Enter Gemini/Gemma API Key", type="password")
st.sidebar.markdown("[Get free API Key from Google AI Studio](https://aistudio.google.com/)")

if not api_key:
    st.info("👈 Please enter your API key in the sidebar to start your viva session.")
    st.stop()

client = genai.Client(api_key=api_key)

# Topic selector
subject = st.sidebar.selectbox(
    "Select Examination Domain:",
    ["Computer Networks & Security", "Data Structures & Algorithms", "Operating Systems", "General Computer Science"]
)

# Chat state
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Answer the question or type 'Start' to begin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    sys_instruction = f"""
    You are an expert oral exam and viva examiner specializing in '{subject}'.
    Your objective is to test conceptual clarity one question at a time.
    Rules:
    1. If the user begins or says 'Start', ask the first crisp conceptual question.
    2. When the user responds:
       - Give an immediate verdict: [Correct / Partially Correct / Incorrect].
       - If flawed, provide a concise 1-2 sentence explanation.
       - Immediately pose the NEXT logical question.
    3. Keep responses tight, fast-paced, and encouraging (under 4-5 sentences).
    """

    history = [m["content"] for m in st.session_state.messages]

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=history,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction,
                temperature=0.6,
            )
        )
        reply = response.text
    except Exception as e:
        reply = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
