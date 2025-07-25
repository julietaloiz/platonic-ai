from langchain_openai import ChatOpenAI
from app.prompts import SUMMARISER_PROMPT


def summarise_convo(messages, model="gpt-4o-mini"):

    transcript = "\n".join(
        f"{role.capitalize()}: {content}" for role, content in messages
    )
    prompt = f"{SUMMARISER_PROMPT}\n\nTranscript: \n {transcript} \n\nSummary:"
    llm = ChatOpenAI(model=model, temperature=0.7)
    response = llm.invoke(prompt)
    return response.content
