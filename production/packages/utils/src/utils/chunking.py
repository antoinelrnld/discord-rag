from langchain_experimental.text_splitter import SemanticChunker
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

chunker = SemanticChunker(
    embeddings=OpenAIEmbeddings(
        model="text-embedding-3-large"
    )
)

def chunk_documents(documents: list[Document]) -> list[Document]:
    return chunker.split_documents(documents)