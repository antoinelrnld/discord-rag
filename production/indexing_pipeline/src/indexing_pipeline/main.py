from utils.ingestion import ingest_documents
from utils.preprocessing import preprocess_documents
from utils.chunking import chunk_documents
from utils.vector_store import index_documents_to_redis
import logging

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def main():
    logger.info("Starting indexing pipeline.")

    logger.info("Ingesting documents.")
    documents = ingest_documents()

    if len(documents) == 0:
        logger.warning("No documents found in the database.")
        return

    logger.info(f"Found {len(documents)} documents in the database.")

    logger.info("Preprocessing documents.")    
    preprocessed_documents = preprocess_documents(documents)
    logger.info("Preprocessing complete.")
    
    logger.info("Chunking documents.")
    chunked_documents = chunk_documents(preprocessed_documents)
    logger.info("Chunking complete.")

    logger.info("Indexing documents to Redis.")
    index_documents_to_redis(chunked_documents)
    logger.info("Indexing complete.")

if __name__ == "__main__":
    main()