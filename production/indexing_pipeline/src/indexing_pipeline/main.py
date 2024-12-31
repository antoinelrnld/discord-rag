from utils.ingestion import ingest_documents
from utils.preprocessing import preprocess_documents
from utils.chunking import chunk_documents
from utils.vector_store import index_documents_to_redis
import logging

logger = logging.getLogger(__name__)

def main():
    documents = ingest_documents()

    if len(documents) == 0:
        logger.warning("No documents found in the database.")
        return
    
    preprocessed_documents = preprocess_documents(documents)
    
    chunked_documents = chunk_documents(preprocessed_documents)

    index_documents_to_redis(chunked_documents)

if __name__ == "__main__":
    main()