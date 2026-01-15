from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

chunker = SemanticChunker(
    embeddings=OpenAIEmbeddings(
        model="text-embedding-3-large"
    ),
    sentence_split_regex=r"<MESSAGE_SEP>",
    add_start_index=False
)
