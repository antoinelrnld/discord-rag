from functools import lru_cache

from indexing_pipeline.settings import (
    ChromaDBSettings,
    ChunkingStrategy,
    DocumentLoaderProvider,
    EmbeddingsProvider,
    MongoDBSettings,
    OpenAIEmbeddingsSettings,
    VectorStoreProvider,
    settings,
)
from langchain_community.document_loaders.base import BaseLoader
from langchain_core.documents import BaseDocumentTransformer
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore


@lru_cache(maxsize=1)
def get_embeddings() -> Embeddings:
    if settings.embeddings.provider == EmbeddingsProvider.OPENAI:
        from langchain_openai import OpenAIEmbeddings

        openai_embeddings_settings: OpenAIEmbeddingsSettings = (
            settings.embeddings.openai
        )
        return OpenAIEmbeddings(model=openai_embeddings_settings.model, chunk_size=50)


@lru_cache(maxsize=1)
def get_vector_store() -> VectorStore:
    embeddings = get_embeddings()
    if settings.vector_store.provider == VectorStoreProvider.CHROMADB:
        from langchain_chroma import Chroma

        chroma_settings: ChromaDBSettings = settings.vector_store.chromadb
        return Chroma(
            collection_name=chroma_settings.collection,
            embedding_function=embeddings,
            host=chroma_settings.host,
        )


@lru_cache(maxsize=1)
def get_document_loader() -> BaseLoader:
    if settings.document_loader.provider == DocumentLoaderProvider.MONGODB:
        from indexing_pipeline.CustomMongodbLoader import CustomMongodbLoader

        mongodb_settings: MongoDBSettings = settings.document_loader.mongodb
        return CustomMongodbLoader(
            connection_string=mongodb_settings.host,
            db_name=mongodb_settings.database,
            collection_name=mongodb_settings.collection,
            field_names=["author.username", "content"],
            metadata_names=["timestamp", "url", "_id"],
            include_db_collection_in_metadata=False,
            filter_criteria={"processed": False},
        )


@lru_cache(maxsize=1)
def get_chunker() -> BaseDocumentTransformer:
    if settings.chunking.strategy == ChunkingStrategy.SEMANTIC:
        from langchain_experimental.text_splitter import SemanticChunker

        embeddings: Embeddings = get_embeddings()
        return SemanticChunker(
            embeddings=embeddings,
            sentence_split_regex=r"<MESSAGE_SEP>",
            add_start_index=False,
        )
