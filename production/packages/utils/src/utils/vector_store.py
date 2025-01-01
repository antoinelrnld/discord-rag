from langchain_redis import RedisConfig, RedisVectorStore
from langchain_openai import OpenAIEmbeddings
import os


redis_config = RedisConfig(
    index_name="discord_rag_semantic_index",
    redis_url=os.getenv("REDIS_URL")
)

vector_store = RedisVectorStore(
    embeddings=OpenAIEmbeddings(
        model="text-embedding-3-large"
    ),
    config=redis_config
)

def index_documents_to_redis(documents: list[str]):
    vector_store.add_documents(documents)

def get_vector_store():
    return vector_store