"""
Simple POC for a Socratic tutor.
"""

import os
import getpass
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

#   LOAD API KEY
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    openai_api_key = getpass.getpass("Enter your OpenAI API key: ")
    os.environ["OPENAI_API_KEY"] = openai_api_key

model = ChatOpenAI(model="gpt-4o-mini")

# SETUP PROMPT, LLM, AND MEMORY - CHAIN
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a Socratic tutor. Only respond with open-ended questions that help the user think deeper about the topic they first mentioned. Never give answers or opinions.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | model


# 5. Set up message history (in-memory for this session)
def get_session_history(session_id: str):
    # For a simple script, just use a new ConversationBufferMemory per session
    return InMemoryChatMessageHistory()


with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages",
)

# MAIN INTERACTION LOOP
print("Welcome to Platonic! Type 'exit' to quit.")
session_id = "local-session"  # In a web app, this would be per user/session
messages = []

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    # Add the user's message
    messages.append(HumanMessage(content=user_input))

    # Get the Socratic question from the agent
    response = with_message_history.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config={"configurable": {"session_id": session_id}},
    )
    socratic_question = response.content

    # Add the AI's message to the history
    messages.append(AIMessage(content=socratic_question))

    print("Tutor:", socratic_question)
