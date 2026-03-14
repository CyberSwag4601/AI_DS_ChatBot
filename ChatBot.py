import streamlit as st
import google.generativeai as genai

# ---------- PAGE SETTINGS ----------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------- API KEY ----------
API_KEY = st.secrets["API_KEY"]
genai.configure(api_key=API_KEY)

# ---------- MODEL ----------
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------- SESSION STATES ----------
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- TITLE ----------
st.title("🤖 AI Chatbot")
st.write("Your AI Assistant powered by Google Gemini")

# ---------- CLEAR CHAT BUTTON ----------
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])
    st.rerun()

# ---------- DISPLAY CHAT HISTORY ----------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------- USER INPUT ----------
prompt = st.chat_input("Type your message here...")

if prompt:

    # show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # get AI response
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            reply = response.text
        except Exception:
            reply = "⚠️ Unable to connect to AI service. Please try again."

        st.markdown(reply)

    # save response
    st.session_state.messages.append({"role": "assistant", "content": reply})
