from indexing_pipeline.ingestion import document_loader
from indexing_pipeline.chunking import chunker
from indexing_pipeline.vector_store import vector_store
import logging
from langchain_core.documents import Document

from tqdm import tqdm

import hashlib

from motor.motor_asyncio import AsyncIOMotorClient
import os

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

BATCH_SIZE = 10
DOCUMENTS_MERGE_SIZE = 50

async def main():
    logger.info("Starting indexing pipeline.")
    logger.info("Ingesting documents.")
    
    batch = {
        'merged_documents': [],
        'ids': []
    }
    documents = []

    async for document in document_loader.alazy_load():
        

        if document.page_content.strip():
            document.page_content = document.page_content.replace(' ', ': ', 1)
            documents.append(document)
            if len(documents) == DOCUMENTS_MERGE_SIZE:
                logger.info(f"Merging {len(documents)} documents.")
                merged_doc_page_content = []

                for doc in documents:
                    merged_doc_page_content.append(doc.page_content)
                    mongodb_id = doc.metadata.get('_id')
                    batch['ids'].append(mongodb_id)
                
                merged_doc = Document(
                    page_content="\n<MESSAGE_SEP>".join(merged_doc_page_content),
                    metadata={
                        'timestamp': documents[0].metadata['timestamp'],
                        'url': documents[0].metadata['url']
                    }
                )

                batch['merged_documents'].append(merged_doc)
                documents = []

        if len(batch['merged_documents']) == BATCH_SIZE:
            logger.info(f"Indexing batch of {len(batch['merged_documents'])} merged documents.")
            chunks = chunker.split_documents(batch['merged_documents'])
            vector_store.add_documents(chunks)

            client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
            db = client[os.getenv("MONGODB_DB")]
            collection = db[os.getenv("MONGODB_COLLECTION")]

            logger.info(f"Marking {len(batch['ids'])} documents as processed in MongoDB.")
            await collection.update_many(
                {"_id": {"$in": batch['ids']}},
                {"$set": {"processed": True}}
            )
            batch['merged_documents'] = []
            batch['ids'] = []

    if documents:
        logger.info(f"Merging remaining {len(documents)} documents.")
        merged_doc = Document(
            page_content="\n<MESSAGE_SEP>".join(doc.page_content for doc in documents),
            metadata={
                'timestamp': documents[0].metadata['timestamp'],
                'url': documents[0].metadata['url']
            }
        )
        batch['merged_documents'].append(merged_doc)

    if batch['merged_documents']:
        logger.info(f"Indexing remaining {len(batch['merged_documents'])} merged documents.")
        chunks = chunker.split_documents(batch['merged_documents'])
        for chunk in chunks:
            chunk_hash = hashlib.sha256(chunk.page_content.encode('utf-8')).hexdigest()
            chunk.id = chunk_hash
        vector_store.add_documents(chunks)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())