"""
Tests for the SocraticAgent class.
"""

import pytest
from app.agent import SocraticAgent


class DummyLLM:
    """
    A dummy LLM for testing SocraticAgent logic without making real API calls.
    Always returns a generic Socratic question.
    """

    def __init__(self, *args, **kwargs):
        pass

    def invoke(self, prompt):
        class Response:
            content = "What makes you ask that?"

        return Response()


@pytest.fixture
def socratic_agent(monkeypatch) -> SocraticAgent:
    """
    Pytest fixture that patches ChatOpenAI in SocraticAgent to use DummyLLM.
    This avoids real API calls and makes tests fast and reliable.
    """
    from app import agent

    monkeypatch.setattr(agent, "ChatOpenAI", lambda *a, **k: DummyLLM())
    return agent.SocraticAgent()


def test_ask_returns_question(socratic_agent: SocraticAgent):
    """
    Test that the agent's response is a question and does not echo the user's input directly.
    """
    response = socratic_agent.ask("What is the meaning of life?")
    assert response.endswith("?")
    assert "meaning of life" not in response.lower()  # Should not answer directly


def test_history_tracks_conversation(socratic_agent: SocraticAgent):
    """
    Test that the conversation history tracks both user and tutor turns.
    """
    socratic_agent.ask("Is knowledge possible?")
    history = socratic_agent.get_history()
    assert len(history) == 2
    assert history[0][0] == "user"
    assert history[1][0] == "tutor"
