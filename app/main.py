"""
Platonic: No easy answers. Just questions.

This is a simple Streamlit app that allows you to chat with a Platonic agent.
"""

import streamlit as st
from app.agent import SocraticAgent
from app.prompts import GOODBYE_MESSAGE
from app.config import USER_MESSAGE_LIMIT

# Initialise the Socratic agent (one per session)
if "agent" not in st.session_state:
    st.session_state.agent = SocraticAgent(session_id="streamlit-session")
# Initialise chat history in session state
if "history" not in st.session_state:
    st.session_state.history = []  # List of (role, content) tuples

st.title("Platonic")
# Add tagline just below the title
st.markdown(
    "<span style='font-size:1.2em; color:gray;'>No easy answers. Just questions.</span>",
    unsafe_allow_html=True,
)

# If conversation is empty, start with a Platonic prompt
if not st.session_state.history:
    st.session_state.history.append(
        ("tutor", "Welcome! What topic or question would you like to explore today?")
    )

# Count user messages in the session
user_message_count = sum(1 for role, _ in st.session_state.history if role == "user")


# Display chat history in a chat-style format (oldest at top, newest at bottom)
st.markdown("#### Conversation")
for role, content in st.session_state.history:
    if role == "user":
        st.markdown(f"**You:** {content}")
    else:
        st.markdown(f"**Platonic:** {content}")

# Place the user input form at the bottom of the conversation
input_disabled = user_message_count >= USER_MESSAGE_LIMIT
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Type your question or topic:", key="user_input", disabled=input_disabled
    )
    submitted = st.form_submit_button("Send", disabled=input_disabled)
    if submitted and user_input.strip() and not input_disabled:
        st.session_state.history.append(("user", user_input))

# After displaying, check if the last message is from the user
if st.session_state.history:
    last_role, last_content = st.session_state.history[-1]
    # If the last message is from the user, generate and stream the agent's response
    if last_role == "user" and user_message_count <= USER_MESSAGE_LIMIT:
        response_placeholder = st.empty()  # Placeholder for streaming response
        response_text = ""
        # Stream the agent's response token by token
        for token in st.session_state.agent.ask_stream(last_content):
            response_text += token
            response_placeholder.markdown(f"**Platonic:** {response_text}")
        # Add the full response to the conversation history
        st.session_state.history.append(("tutor", response_text))
        st.rerun()  # Rerun to update the UI and await next user input
    # If the user has hit the message limit, show the goodbye message
    elif last_role == "user" and user_message_count > USER_MESSAGE_LIMIT:
        st.session_state.history.append(("tutor", GOODBYE_MESSAGE))
        st.rerun()
