import random

STARTER_QUESTIONS = [
    # Philosophy
    "What is the meaning of a good life?",
    "Is happiness the ultimate goal of human existence?",
    "Can we ever truly know anything?",
    "What is the nature of reality—does it exist outside our minds?",
    "Is free will real, or are our choices determined?",
    "What makes an action morally right or wrong?",
    "Is it better to live authentically or to fit in?",
    "Does suffering have value or purpose?",
    "Is it possible to live without regret?",
    "Can one person change the world?",
    # Life Choices
    "How should we choose what to value in life?",
    "Is it more important to be respected or liked?",
    "Can money buy happiness or meaning?",
    "Is it possible to live a good life without work?",
    "Should we always follow our passions, even if impractical?",
    "What does it mean to be a good friend?",
    "Is it better to take risks or play it safe?",
    "How do you know if you are making the right decision?",
    # AI and Technology
    "Can AI ever be truly conscious?",
    "Should AI be allowed to make moral decisions?",
    "How might AI change what it means to be human?",
    "Is it ethical to build machines that can suffer?",
    "Could an AI develop its own sense of purpose?",
    "Will AI ever be able to understand human emotions?",
    "Should we trust AI to make life choices for us?",
]


def get_random_starter_question():
    """
    Return a random starter question from the list.
    """
    return random.choice(STARTER_QUESTIONS)
