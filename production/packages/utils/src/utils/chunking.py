from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

chunker = SemanticChunker(
    embeddings=OpenAIEmbeddings(
        model="text-embedding-3-large"
    )
)

def chunk_documents(documents_str: str) -> list[str]:
    return chunker.create_documents([documents_str])