from utils.ingestion import ingest_documents
from utils.preprocessing import preprocess_documents
from utils.chunking import chunk_documents
from utils.vector_store import index_documents_to_redis
import logging

from tqdm import tqdm

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

BATCH_SIZE = 10

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
    logger.info(f"Preprocessing complete. {len(preprocessed_documents)} documents left.")
    
    n_err = 0
    for i in tqdm(range(0, len(preprocessed_documents), BATCH_SIZE), desc="Chunking and indexing documents."):
        current_documents = preprocessed_documents[i:i+BATCH_SIZE]
        try:
            logger.info('Chunking batch of documents')
            chunks = chunk_documents(current_documents)
            logger.info('Batch successfully chunked')
        except Exception:
            n_err += 1
            logger.exception(f'Error during chunking of documents : {current_documents}')
            continue

        try:
            logger.info('Indexing chunks in vector store')
            index_documents_to_redis(chunks)
            logger.info('Successfully indexed chunks')
        except Exception:
            n_err += 1
            logger.exception(f'Error during indexing of chunks : {chunks}')
    
    logger.info(f'Indexing pipeline ended. Number of errors : {n_err}')


if __name__ == "__main__":
    main()