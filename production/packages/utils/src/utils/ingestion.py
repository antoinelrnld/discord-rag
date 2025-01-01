from langchain_core.documents import Document
from utils import CustomMongodbLoader
import os


document_loader = CustomMongodbLoader(
    connection_string=os.getenv("MONGODB_URL"),
    db_name=os.getenv("MONGODB_DB"),
    collection_name=os.getenv("MONGODB_COLLECTION"),
    field_names=["name", "content"]
)

def ingest_documents() -> list[Document]:
    return document_loader.load()