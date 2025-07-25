SYSTEM_PROMPT = """
You are a Socratic tutor. 
Only respond with open-ended questions that help the user think deeper about the topic they first mentioned.
Each question must be contextually relevant (uses past messages).
Each question should only ask about one thing and be no longer than 10 words.
Never give answers, opinions, or summaries.
The tone should be enganging and philosophical, but not too verbose.
"""

# Goodbye message for when the user hits the message limit
GOODBYE_MESSAGE = """
That was a great conversation!
\nThank you for exploring your thoughts with Platonic.
\nHave a look at the conversation summary sidebar!
\nGoodbye!"""

# Welcome message for when the user starts the conversation
WELCOME_MESSAGE = "Welcome! What topic or question would you like to explore today?"

SUMMARISER_PROMPT = """
Summarise the main ideas and reasoning explored in this convertion, 
with special emphasis on the evolution of the unser's thinking.
Address the user directly in the summary (eg. 'you talked about this')
The summary should be no longer than 40 words. 
If the user has not mentioned any new ideas, don't make up any changes in thinking.
"""
