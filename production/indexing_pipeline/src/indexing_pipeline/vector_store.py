import os
from langchain_openai import OpenAIEmbeddings

from langchain_chroma import Chroma


vector_store = Chroma(
    collection_name="discord_rag_chroma_collection",
    embedding_function=OpenAIEmbeddings(
        model="text-embedding-3-large",
        chunk_size=50
    ),
    host=os.getenv("CHROMA_URL", "localhost")
)
