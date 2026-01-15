import os

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

vector_store: Chroma = Chroma(
    collection_name="discord_rag_chroma_collection",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-large", chunk_size=50),
    host=os.getenv("CHROMA_URL", "localhost"),
)
