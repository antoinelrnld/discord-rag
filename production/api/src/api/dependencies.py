import os
from typing import Annotated

from api.agent import Agent
from api.agent.system_prompt import Language
from fastapi import Depends
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.vectorstores import VectorStore


def get_llm() -> BaseChatModel:
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(model="gpt-4o-mini")


LLMDependency = Annotated[BaseChatModel, Depends(get_llm)]


def get_embeddings() -> Embeddings:
    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(model="text-embedding-3-large", chunk_size=50)


EmbeddingsDependency = Annotated[Embeddings, Depends(get_embeddings)]


def get_vector_store(embeddings: EmbeddingsDependency) -> VectorStore:
    from langchain_chroma import Chroma

    return Chroma(
        collection_name="discord_rag_chroma_collection",
        embedding_function=embeddings,
        host=os.getenv("CHROMA_URL", "localhost"),
    )


VectorStoreDependency = Annotated[VectorStore, Depends(get_vector_store)]


def get_agent(llm: LLMDependency, vector_store: VectorStoreDependency) -> Agent:
    agent_language: str = os.getenv("AGENT_LANGUAGE", "en").lower()
    language: Language = Language(agent_language)
    return Agent(llm, vector_store, language)


AgentDependency = Annotated[Agent, Depends(get_agent)]
