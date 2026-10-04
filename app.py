import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="Gemma Viva Drill", page_icon="🎯", layout="centered")

st.title("🎯 Gemma Concept & Viva Drill")
st.caption("Built for a friend who needs rapid, interactive interview and conceptual viva practice.")

# Fetch API key directly from environment (Render)
api_key = os.environ.get("GEMINI_API_KEY")

# Fallback to sidebar if environment variable is not configured
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini/Gemma API Key", type="password")

if not api_key:
    st.info("👈 Please configure GEMINI_API_KEY or enter your key in the sidebar.")
    st.stop()

genai.configure(api_key=api_key)

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
    You are an expert technical viva examiner specializing in '{subject}'.
    Your objective is to test conceptual clarity one question at a time.
    Rules:
    1. If the user begins or says 'Start' or 'hi', ask the first crisp conceptual question.
    2. When the user responds:
       - Give an immediate verdict: [Correct / Partially Correct / Incorrect].
       - If flawed, provide a concise 1-2 sentence explanation.
       - Immediately pose the NEXT logical question.
    3. Keep responses tight, fast-paced, and encouraging (under 4-5 sentences).
    """

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=sys_instruction
    )

    # Format history
    history_payload = []
    for m in st.session_state.messages[:-1]:
        role = "user" if m["role"] == "user" else "model"
        history_payload.append({"role": role, "parts": [m["content"]]})

    try:
        chat = model.start_chat(history=history_payload)
        response = chat.send_message(prompt)
        reply = response.text
    except Exception as e:
        reply = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
