import logging
import os
from typing import Any, Dict, List

from indexing_pipeline.chunking import chunker
from indexing_pipeline.ingestion import document_loader
from indexing_pipeline.vector_store import vector_store
from langchain_core.documents import Document
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from pydantic import BaseModel

BATCH_SIZE = 10
DOCUMENTS_MERGE_SIZE = 50

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BatchItem(BaseModel):
    merged_document: Document
    ids: List[str]


class DocumentMetadata(BaseModel):
    timestamp: float
    url: str
    final: bool


def merge_documents(documents: List[Document]) -> Document | None:
    """Merge a list of Document objects into a single Document with concatenated content and shared metadata."""
    if not documents:
        return None
    merged_content: str = "\n<MESSAGE_SEP>".join(doc.page_content for doc in documents)
    metadata: DocumentMetadata = DocumentMetadata(
        timestamp=documents[0].metadata.get("timestamp"),
        url=documents[0].metadata.get("url"),
        final=True if len(documents) == DOCUMENTS_MERGE_SIZE else False,
    )
    return Document(page_content=merged_content, metadata=metadata.model_dump())


async def mark_documents_processed(ids: List[str]) -> None:
    """Mark documents as processed in MongoDB by their IDs."""
    if not ids:
        return
    client: AsyncIOMotorClient = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    db: AsyncIOMotorDatabase = client[os.getenv("MONGODB_DB")]
    collection: AsyncIOMotorCollection = db[os.getenv("MONGODB_COLLECTION")]
    logger.info(f"Marking {len(ids)} documents as processed in MongoDB.")
    await collection.update_many({"_id": {"$in": ids}}, {"$set": {"processed": True}})


async def process_batch(batch: List[BatchItem]) -> None:
    """Process a batch: split, add to vector store, and mark as processed."""
    if not batch:
        return
    logger.info(f"Indexing batch of {len(batch)} merged documents.")
    chunks: List[Document] = chunker.split_documents(
        [item.merged_document for item in batch]
    )
    vector_store.add_documents(chunks)
    await mark_documents_processed(
        [
            doc_id
            for item in batch
            for doc_id in item.ids
            if len(item.ids) == DOCUMENTS_MERGE_SIZE
        ]
    )


async def main() -> None:
    """Main entry point for the indexing pipeline."""
    logger.info("Starting indexing pipeline.")
    logger.info("Ingesting documents.")

    # retrieve documents with final=False from vector store and delete them
    not_final: Dict[str, Any] = vector_store.get(where={"final": False})
    if len(not_final["documents"]) > 0:
        vector_store.delete(ids=not_final["ids"])

    batch: List[BatchItem] = []
    documents: List[Document] = []

    async for document in document_loader.alazy_load():
        if not document.page_content.strip():
            continue
        document.page_content = document.page_content.replace(" ", ": ", 1)
        documents.append(document)
        if len(documents) == DOCUMENTS_MERGE_SIZE:
            logger.info(f"Merging {len(documents)} documents.")
            merged_doc: Document = merge_documents(documents)
            batch.append(
                BatchItem(
                    merged_document=merged_doc,
                    ids=[doc.metadata.get("_id") for doc in documents],
                )
            )
            documents.clear()
        if len(batch) == BATCH_SIZE:
            await process_batch(batch)
            batch.clear()

    if documents:
        logger.info(f"Merging remaining {len(documents)} documents.")
        merged_doc: Document = merge_documents(documents)
        batch.append(
            BatchItem(
                merged_document=merged_doc,
                ids=[doc.metadata.get("_id") for doc in documents],
            )
        )

    if batch:
        await process_batch(batch)
        batch.clear()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
