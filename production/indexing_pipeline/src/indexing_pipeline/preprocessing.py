from langchain_core.documents import Document

def remove_empty_documents(documents: list[Document]) -> list[Document]:
    return [doc for doc in documents if doc.page_content]

def add_separator_between_author_and_text(documents: list[Document]) -> list[Document]:
    for doc in documents:
        doc.page_content = doc.page_content.replace(" ", ": ", 1)
    return documents

def merge_documents_into_groups_of_size_n(documents: list[Document], n: int = 50) -> list[Document]:
    return [
        Document(
            page_content="\n<MESSAGE_SEP>".join(document.page_content for document in documents[i:i+n]),
            metadata={'timestamp': documents[i].metadata['timestamp'], 'url': documents[i].metadata['url']}
        ) for i in range(0, len(documents), n)
    ]

def preprocess_documents(documents: list[Document]) -> list[Document]:
    documents = remove_empty_documents(documents)
    documents = add_separator_between_author_and_text(documents)
    return merge_documents_into_groups_of_size_n(documents, 50)