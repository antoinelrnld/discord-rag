from functools import lru_cache
from typing import Annotated

from api.agent import Agent
from api.agent.system_prompt import Language
from api.settings import (
    AgentSettings,
    ApiSettings,
    ChromaDBSettings,
    EmbeddingsProvider,
    LLMProvider,
    OpenAIEmbeddingsSettings,
    OpenAILLMSettings,
    VectorStoreProvider,
)
from fastapi import Depends
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.vectorstores import VectorStore


@lru_cache(maxsize=1)
def get_settings() -> ApiSettings:
    return ApiSettings()


SettingsDependency = Annotated[ApiSettings, Depends(get_settings)]


def get_llm(settings: SettingsDependency) -> BaseChatModel:
    if settings.llm.provider == LLMProvider.OPENAI:
        from langchain_openai import ChatOpenAI

        openai_llm_settings: OpenAILLMSettings = settings.llm.openai
        return ChatOpenAI(model=openai_llm_settings.model)


LLMDependency = Annotated[BaseChatModel, Depends(get_llm)]


def get_embeddings(settings: SettingsDependency) -> Embeddings:
    if settings.embeddings.provider == EmbeddingsProvider.OPENAI:
        from langchain_openai import OpenAIEmbeddings

        openai_embeddings_settings: OpenAIEmbeddingsSettings = (
            settings.embeddings.openai
        )
        return OpenAIEmbeddings(model=openai_embeddings_settings.model, chunk_size=50)


EmbeddingsDependency = Annotated[Embeddings, Depends(get_embeddings)]


def get_vector_store(
    settings: SettingsDependency, embeddings: EmbeddingsDependency
) -> VectorStore:
    if settings.vector_store.provider == VectorStoreProvider.CHROMADB:
        from langchain_chroma import Chroma

        chroma_settings: ChromaDBSettings = settings.vector_store.chromadb
        return Chroma(
            collection_name=chroma_settings.collection,
            embedding_function=embeddings,
            host=chroma_settings.host,
        )


VectorStoreDependency = Annotated[VectorStore, Depends(get_vector_store)]


def get_agent(
    llm: LLMDependency,
    vector_store: VectorStoreDependency,
    settings: SettingsDependency,
) -> Agent:
    agent_settings: AgentSettings = settings.agent
    agent_language: Language = agent_settings.language
    return Agent(llm, vector_store, agent_language)


AgentDependency = Annotated[Agent, Depends(get_agent)]
