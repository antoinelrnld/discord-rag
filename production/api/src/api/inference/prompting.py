from langchain_core.prompts import PromptTemplate

TEMPLATE = """Utilise les éléments de contexte suivants pour répondre à la question à la fin.
Les phrases suivantes sont des messages issus d'une conversation sur Discord.
Il y a plusieurs intervenants, et les messages sont dans l'ordre chronologique.


{context}

Question : {question}

Réponse :"""

def get_prompt_template():
    return PromptTemplate.from_template(TEMPLATE)