from enum import Enum

from api.agent.system_prompt import Language
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


##### Vector Store Settings #####
class VectorStoreProvider(str, Enum):
    CHROMADB = "chromadb"


class ChromaDBSettings(BaseModel):
    host: str = "discord_rag_chroma"
    collection: str = "discord_rag_vector_store_collection"


class VectorStoreSettings(BaseModel):
    provider: VectorStoreProvider = VectorStoreProvider.CHROMADB
    chromadb: ChromaDBSettings = ChromaDBSettings()


##### Embeddings Settings #####
class EmbeddingsProvider(str, Enum):
    OPENAI = "openai"


class OpenAIEmbeddingsSettings(BaseModel):
    model: str = "text-embedding-3-large"


class EmbeddingsSettings(BaseModel):
    provider: EmbeddingsProvider = EmbeddingsProvider.OPENAI
    openai: OpenAIEmbeddingsSettings = OpenAIEmbeddingsSettings()


##### LLM Settings #####
class LLMProvider(str, Enum):
    OPENAI = "openai"


class OpenAILLMSettings(BaseModel):
    model: str = "gpt-4o-mini"


class LLMSettings(BaseModel):
    provider: LLMProvider = LLMProvider.OPENAI
    openai: OpenAILLMSettings = OpenAILLMSettings()


##### Agent Settings #####
class AgentSettings(BaseModel):
    language: Language = Language.ENGLISH


##### Main API Settings #####
class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    vector_store: VectorStoreSettings = VectorStoreSettings()
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    llm: LLMSettings = LLMSettings()
    agent: AgentSettings = AgentSettings()
