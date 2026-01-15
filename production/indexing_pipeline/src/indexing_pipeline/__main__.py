import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from langchain_core.documents import Document
from indexing_pipeline.ingestion import document_loader
from indexing_pipeline.chunking import chunker
from indexing_pipeline.vector_store import vector_store

BATCH_SIZE = 10
DOCUMENTS_MERGE_SIZE = 50

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def merge_documents(documents):
    """Merge a list of Document objects into a single Document with concatenated content and shared metadata."""
    if not documents:
        return None
    merged_content = "\n<MESSAGE_SEP>".join(doc.page_content for doc in documents)
    metadata = {
        'timestamp': documents[0].metadata.get('timestamp'),
        'url': documents[0].metadata.get('url'),
        'final': True if len(documents) == DOCUMENTS_MERGE_SIZE else False
    }
    return Document(page_content=merged_content, metadata=metadata)

async def mark_documents_processed(ids):
    """Mark documents as processed in MongoDB by their IDs."""
    if not ids:
        return
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    db = client[os.getenv("MONGODB_DB")]
    collection = db[os.getenv("MONGODB_COLLECTION")]
    logger.info(f"Marking {len(ids)} documents as processed in MongoDB.")
    await collection.update_many({"_id": {"$in": ids}}, {"$set": {"processed": True}})

async def process_batch(batch):
    """Process a batch: split, add to vector store, and mark as processed."""
    if not batch:
        return
    logger.info(f"Indexing batch of {len(batch)} merged documents.")
    chunks = chunker.split_documents([item['merged_document'] for item in batch])
    vector_store.add_documents(chunks)
    await mark_documents_processed([doc_id for item in batch for doc_id in item['ids'] if len(item['ids']) == DOCUMENTS_MERGE_SIZE])
    batch.clear()

async def main():
    """Main entry point for the indexing pipeline."""
    logger.info("Starting indexing pipeline.")
    logger.info("Ingesting documents.")
    
    # retrieve documents with final=False from vector store and delete them
    not_final = vector_store.get(where={"final": False})
    if len(not_final['documents']) > 0:
        vector_store.delete(ids=not_final['ids'])

    batch = []
    documents = []

    async for document in document_loader.alazy_load():
        if not document.page_content.strip():
            continue
        document.page_content = document.page_content.replace(' ', ': ', 1)
        documents.append(document)
        if len(documents) == DOCUMENTS_MERGE_SIZE:
            logger.info(f"Merging {len(documents)} documents.")
            merged_doc = merge_documents(documents)
            batch.append({'merged_document': merged_doc, 'ids': [doc.metadata.get('_id') for doc in documents]})
            documents.clear()
        if len(batch) == BATCH_SIZE:
            await process_batch(batch)

    if documents:
        logger.info(f"Merging remaining {len(documents)} documents.")
        merged_doc = merge_documents(documents)
        batch.append({'merged_document': merged_doc, 'ids': [doc.metadata.get('_id') for doc in documents]})
        
    if batch:
        await process_batch(batch)
        

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())