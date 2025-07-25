import streamlit as st
import json
import os
from app.prompts import GOODBYE_MESSAGE
from app.agent import SocraticAgent

USER_MESSAGE_LIMIT = 6

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "../assets")


def apply_layout_styles():
    """
    Apply custom CSS to make the title sticky and chat area scrollable with autoscroll.
    """
    st.markdown(
        """
        <style>
        .platonic-title-banner {
            position: sticky;
            top: 0;
            background: #fff;
            z-index: 100;
            padding-bottom: 0.5em;
        }
        .chat-scroll-area {
            max-height: 60vh;
            overflow-y: auto;
            padding-bottom: 1em;
        }
        </style>
        <script>
        // Auto-scroll chat area to bottom on update
        window.addEventListener('load', function() {
            var chatArea = document.getElementById('chat-scroll-area');
            if (chatArea) { chatArea.scrollTop = chatArea.scrollHeight; }
        });
        new MutationObserver(function() {
            var chatArea = document.getElementById('chat-scroll-area');
            if (chatArea) { chatArea.scrollTop = chatArea.scrollHeight; }
        }).observe(document.body, {childList: true, subtree: true});
        </script>
    """,
        unsafe_allow_html=True,
    )


def load_branding(branding_name="minimal"):
    """
    Load branding settings from a JSON file in the assets directory.
    """
    path = os.path.join(ASSETS_DIR, f"{branding_name}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def apply_branding(branding):
    """
    Inject global CSS for colours, fonts, and other branding using the loaded branding dict.
    """
    st.markdown(
        f"""
        <style>
            body, .main, .stApp {{
                font-family: {branding['font_family']};
                background-color: {branding['background_color']};
            }}
            .stButton>button {{
                background-color: {branding['button_color']};
                color: {branding['button_text_color']};
                font-weight: bold;
                border-radius: 6px;
            }}
            .stTextInput>div>input {{
                font-family: {branding['font_family']};
                font-size: 1.1em;
            }}
            .chat-message {{
                border-radius: 12px;
                padding: 0.7em 1em;
                margin-bottom: 0.5em;
                display: inline-block;
                max-width: 90%;
            }}
            .user-message {{
                background: {branding['user_bubble_color']};
                color: {branding['user_text_color']};
                align-self: flex-end;
            }}
            .tutor-message {{
                background: {branding['tutor_bubble_color']};
                color: {branding['tutor_text_color']};
                align-self: flex-start;
            }}
        </style>
    """,
        unsafe_allow_html=True,
    )


def render_welcome_message():
    """Display the welcome message."""
    if not st.session_state.history:
        st.session_state.history.append(
            (
                "tutor",
                "Welcome! What topic or question would you like to explore today?",
            )
        )


def render_title_and_tagline():
    """Display the app title and tagline in a sticky banner."""
    st.markdown(
        """
        <div class='platonic-title-banner'>
            <h1 style='margin-bottom:0.2em;'>Platonic</h1>
            <span style='font-size:1.2em; color:gray;'>No easy answers. Just questions.</span>
        </div>
    """,
        unsafe_allow_html=True,
    )


def render_chat_history(history):
    """
    Display the chat history in a scrollable chat-style format (oldest at top), using custom HTML/CSS classes for chat bubbles.
    """
    st.markdown(
        "<div id='chat-scroll-area' class='chat-scroll-area'>", unsafe_allow_html=True
    )
    st.markdown("#### Conversation")
    for role, content in history:
        if role == "user":
            st.markdown(
                f"<div class='chat-message user-message'>You: {content}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='chat-message tutor-message'>Platonic: {content}</div>",
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)


def get_placeholder_text(user_message_count):
    """
    Return the appropriate placeholder text for the input box.
    You can update this logic to reflect branding or tone.
    """
    return "Type your question or topic:" if user_message_count == 0 else "Your answer"


def user_input_form(input_disabled, placeholder_text):
    """
    Display the user input form and handle submission.
    To style the input, use the placeholder or add custom CSS above.
    """
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Your message",  # Label
            placeholder=placeholder_text,
            key="user_input",
            disabled=input_disabled,
        )
        submitted = st.form_submit_button("Send", disabled=input_disabled)
        if submitted and user_input.strip() and not input_disabled:
            st.session_state.history.append(("user", user_input))


def handle_agent_response(history, user_message_count, input_disabled):
    """
    If the last message is from the user, generate and stream the agent's response.
    If the user has hit the message limit, show the goodbye message and do not reply further.
    This function is UI-agnostic and can be extended for branded responses.
    """
    if history:
        last_role, last_content = history[-1]
        # If the user has hit the message limit, show only the goodbye message and disable input
        if last_role == "user" and user_message_count >= USER_MESSAGE_LIMIT:
            st.session_state.history.append(("tutor", GOODBYE_MESSAGE))
            st.rerun()
        # Otherwise, stream the tutor's response in the chat history area
        elif last_role == "user" and user_message_count < USER_MESSAGE_LIMIT:
            # Stream the tutor's message in place in the chat history
            def stream():
                return st.session_state.agent.ask_stream(last_content)

            # After streaming, add the full response to history
            response_text = "".join(st.session_state.agent.ask_stream(last_content))
            st.session_state.history.append(("tutor", response_text))
            st.rerun()


def add_tutor_message_to_history(agent, user_message):
    """
    Get the full tutor response from the agent and append it to the chat history.
    Args:
        agent: The SocraticAgent instance.
        user_message: The user's message to respond to.
    """
    response_text = agent.ask(user_message)
    st.session_state.history.append(("tutor", response_text))
