from langchain_core.documents import Document

def remove_empty_documents(documents: list[Document]) -> list[Document]:
    return [doc for doc in documents if doc.page_content]

def add_separator_between_author_and_text(documents: list[Document]) -> list[str]:
    return [doc.page_content.replace(" ", ": ", 1) for doc in documents]

def join_documents_to_str(documents: list[str]) -> str:
    return "\n".join(documents)

def preprocess_documents(documents: list[Document]) -> str:
    documents = remove_empty_documents(documents)
    documents = add_separator_between_author_and_text(documents)
    return join_documents_to_str(documents)