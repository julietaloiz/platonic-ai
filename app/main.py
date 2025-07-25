"""
Platonic: No easy answers. Just questions.

This is a simple Streamlit app that allows you to chat with a Platonic agent.

Example usage:

```
streamlit run app/main.py
```
"""

import streamlit as st
from app.agent import SocraticAgent
from app.ui_utils import (
    render_title_and_tagline,
    render_chat_history,
    render_welcome_message,
    get_placeholder_text,
    user_input_form,
    handle_agent_response,
    USER_MESSAGE_LIMIT,
    load_branding,
    apply_branding,
    apply_layout_styles,
    add_tutor_message_to_history,
)
from app.prompts import GOODBYE_MESSAGE, WELCOME_MESSAGE

# SETUP UI
apply_layout_styles()
apply_branding(load_branding("minimal"))
render_title_and_tagline()

# SETUP AGENT
if "agent" not in st.session_state:
    st.session_state.agent = SocraticAgent(session_id="streamlit-session")
if "history" not in st.session_state:
    st.session_state.history = []
if "pending_tutor_reply" not in st.session_state:
    st.session_state.pending_tutor_reply = False

# Ensure the conversation starts with a Platonic prompt
if not st.session_state.history:
    st.session_state.history.append(("tutor", WELCOME_MESSAGE))

user_message_count = sum(1 for role, _ in st.session_state.history if role == "user")
input_disabled = user_message_count >= USER_MESSAGE_LIMIT
placeholder_text = (
    "Type your question or topic:" if user_message_count == 0 else "Your answer"
)

# Always render chat history first (so it appears above the input box)
render_chat_history(st.session_state.history)

# Show input form only if under the message limit and not waiting for a tutor reply
if not input_disabled and not st.session_state.pending_tutor_reply:
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Your message",
            placeholder=placeholder_text,
            key="user_input",
            disabled=input_disabled,
        )
        submitted = st.form_submit_button("Send", disabled=input_disabled)
        if submitted and user_input.strip():
            st.session_state.history.append(("user", user_input))
            st.session_state.pending_tutor_reply = True
            st.rerun()
    # Add a placeholder Surprise Me button below the input form
    if st.button("Surprise Me", disabled=input_disabled):
        # Placeholder: add a fixed surprise question (replace with random later)
        st.session_state.history.append(
            ("user", "What is the meaning of life? (Surprise Me)")
        )
        st.session_state.pending_tutor_reply = True
        st.rerun()

# Tutor reply logic (runs after user message is added)
if st.session_state.pending_tutor_reply:
    if user_message_count < USER_MESSAGE_LIMIT:
        add_tutor_message_to_history(
            st.session_state.agent, st.session_state.history[-1][1]
        )
        st.session_state.pending_tutor_reply = False
        st.rerun()
    elif user_message_count == USER_MESSAGE_LIMIT:
        if st.session_state.history[-1][1] != GOODBYE_MESSAGE:
            st.session_state.history.append(("tutor", GOODBYE_MESSAGE))
        st.session_state.pending_tutor_reply = False
        st.rerun()
