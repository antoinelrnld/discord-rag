import os
from typing import Annotated

from fastapi import Depends
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.vectorstores import VectorStore
from langchain_core.embeddings import Embeddings
from api.agent import Agent


def get_llm() -> BaseChatModel:
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model="gpt-4o-mini")


LLMDependency = Annotated[BaseChatModel, Depends(get_llm)]


def get_embeddings() -> Embeddings:
    from langchain_openai import OpenAIEmbeddings
    return OpenAIEmbeddings(
        model="text-embedding-3-large",
        chunk_size=50
    )


EmbeddingsDependency = Annotated[Embeddings, Depends(get_embeddings)]


def get_vector_store(embeddings: EmbeddingsDependency) -> VectorStore:
    from langchain_redis import RedisConfig, RedisVectorStore

    redis_config = RedisConfig(
        index_name="discord_rag_semantic_index",
        redis_url=os.getenv("REDIS_URL"),
        metadata_schema=[
            {"name": "timestamp", "type": "numeric"},
            {"name": "url", "type": "text"}
        ]
    
    )

    return RedisVectorStore(
        embeddings=embeddings,
        config=redis_config
    )


VectorStoreDependency = Annotated[VectorStore, Depends(get_vector_store)]


def get_agent(llm: LLMDependency, vector_store: VectorStoreDependency):
    return Agent(llm, vector_store)


AgentDependency = Annotated[Agent, Depends(get_agent)]
