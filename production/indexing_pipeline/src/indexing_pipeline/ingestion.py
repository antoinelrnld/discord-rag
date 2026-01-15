from langchain_core.documents import Document
from indexing_pipeline.CustomMongodbLoader import CustomMongodbLoader
import os


document_loader = CustomMongodbLoader(
    connection_string=os.getenv("MONGODB_URL"),
    db_name=os.getenv("MONGODB_DB"),
    collection_name=os.getenv("MONGODB_COLLECTION"),
    field_names=["author.username", "content"],
    metadata_names=["timestamp", "url", "_id"],
    include_db_collection_in_metadata=False,
    filter_criteria={"processed": False}
)

def ingest_documents() -> list[Document]:
    return document_loader.load()