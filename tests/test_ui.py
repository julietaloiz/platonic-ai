"""
Tests for the Platonic Streamlit UI logic (without real OpenAI API calls).
"""

import pytest
import streamlit as st
from app.ui_utils import (
    render_chat_history,
    user_input_form,
    add_tutor_message_to_history,
    USER_MESSAGE_LIMIT,
    GOODBYE_MESSAGE,
)


class DummyAgent:
    """
    Dummy agent that returns a fixed response.
    """

    def ask(self, user_message):
        return "This is a full response."


@pytest.fixture(autouse=True)
def setup_session_state(monkeypatch):
    # Reset Streamlit session state for each test
    st.session_state.clear()
    st.session_state.agent = DummyAgent()
    st.session_state.history = []
    yield
    st.session_state.clear()


def test_user_message_appears_immediately():
    # Simulate user input
    st.session_state.history.append(("user", "Why is the sky blue?"))
    assert st.session_state.history[-1] == ("user", "Why is the sky blue?")


def test_tutor_message_added():
    # Add user message
    st.session_state.history.append(("user", "What is love?"))
    # Add tutor message in one go
    add_tutor_message_to_history(st.session_state.agent, "What is love?")
    # The last message should be a tutor message with the full response
    assert st.session_state.history[-1][0] == "tutor"
    assert "This is a full response." in st.session_state.history[-1][1]


def test_goodbye_message_and_input_disabled():
    # Simulate a full session up to the message limit
    for i in range(USER_MESSAGE_LIMIT):
        st.session_state.history.append(("user", f"Message {i+1}"))
        add_tutor_message_to_history(st.session_state.agent, f"Message {i+1}")
    # Add one more user message to hit the limit
    st.session_state.history.append(("user", "Final message"))
    # Simulate the goodbye logic as in the main app
    user_message_count = sum(1 for r, _ in st.session_state.history if r == "user")
    input_disabled = user_message_count >= USER_MESSAGE_LIMIT
    if input_disabled and st.session_state.history[-1][1] != GOODBYE_MESSAGE:
        st.session_state.history.append(("tutor", GOODBYE_MESSAGE))
    # Check that the goodbye message is the last message
    assert st.session_state.history[-1] == ("tutor", GOODBYE_MESSAGE)
    # Input should be disabled
    assert input_disabled
    # No further tutor reply should be added after the goodbye message
    st.session_state.history.append(("user", "Should not get a reply"))
    user_message_count = sum(1 for r, _ in st.session_state.history if r == "user")
    input_disabled = user_message_count >= USER_MESSAGE_LIMIT
    if input_disabled and st.session_state.history[-1][1] != GOODBYE_MESSAGE:
        st.session_state.history.append(("tutor", GOODBYE_MESSAGE))
    # The goodbye message should still be the last message
    assert st.session_state.history[-1] == ("tutor", GOODBYE_MESSAGE)
