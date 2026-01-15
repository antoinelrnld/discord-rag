from enum import Enum
from typing import Dict


class Language(str, Enum):
    ENGLISH = "en"
    FRENCH = "fr"


SYSTEM_PROMPT: Dict[Language, str] = {
    Language.FRENCH: """Utilise les éléments de contexte suivants pour répondre à la question à la fin.
Les phrases suivantes sont des messages issus d'une conversation sur Discord.
Il y a plusieurs intervenants, et les messages du contexte sont dans l'ordre chronologique.
Répond en utilisant les éléments de contexte les plus récents si cela est pertinent.


Contexte : {context}

Question : {question}

Réponse :""",
    Language.ENGLISH: """Use the following context to answer the question at the end.
The following sentences are messages from a conversation on Discord.
There are multiple participants, and the context messages are in chronological order.
Answer using the most recent context elements if relevant.


Context: {context}

Question: {question}

Answer:""",
}
