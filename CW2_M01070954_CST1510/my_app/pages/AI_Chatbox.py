import streamlit as st
from google import genai

# Initialize Gemini client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.subheader("Gemini Chatbox Test")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "parts": [{"text": "You are a cybersecurity expert."}]}]

# Display previous messages
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    role = "assistant" if message["role"] == "model" else message["role"]
    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])

# Chat input
prompt = st.chat_input("Say something")

if prompt:
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append({"role": "user", "parts": [{"text": prompt}]})

    # Generate response from Gemini
    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=st.session_state.messages
    )

    full_reply = response.text if hasattr(response, "text") else ""

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(full_reply)

    # Save assistant message
    st.session_state.messages.append({"role": "model", "parts": [{"text": full_reply}]})

    st.rerun()
