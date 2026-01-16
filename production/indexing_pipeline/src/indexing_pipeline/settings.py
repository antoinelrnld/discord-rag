from enum import Enum

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


##### Document Loader Settings #####
class DocumentLoaderProvider(str, Enum):
    MONGODB = "mongodb"


class MongoDBSettings(BaseModel):
    host: str = "mongodb://discord_rag_mongo:27017"
    database: str = "discord_rag"
    collection: str = "messages"


class DocumentLoaderSettings(BaseModel):
    provider: DocumentLoaderProvider = DocumentLoaderProvider.MONGODB
    mongodb: MongoDBSettings = MongoDBSettings()


##### Vector Store Settings #####
class VectorStoreProvider(str, Enum):
    CHROMADB = "chromadb"


class ChromaDBSettings(BaseModel):
    host: str = "discord_rag_chroma"
    collection: str = "discord_rag_chroma_collection"


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


##### Chunking Settings #####
class ChunkingStrategy(str, Enum):
    SEMANTIC = "semantic"


class ChunkingSettings(BaseModel):
    strategy: ChunkingStrategy = ChunkingStrategy.SEMANTIC


##### Main Indexing Pipeline Settings #####
class IndexingPipelineSettings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    document_loader: DocumentLoaderSettings = DocumentLoaderSettings()
    vector_store: VectorStoreSettings = VectorStoreSettings()
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    chunking: ChunkingSettings = ChunkingSettings()


settings = IndexingPipelineSettings()
