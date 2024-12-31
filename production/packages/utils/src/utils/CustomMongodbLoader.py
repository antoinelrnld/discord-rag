from langchain_community.document_loaders.mongodb import MongodbLoader
from langchain_core.documents import Document
import logging

logger = logging.getLogger(__name__)

# CustomMongodbLoader is a subclass of MongodbLoader that overrides the `aload` method.
# We need to override this method to ensure that the documents are loaded in the correct order.
# The order is important because we are handling conversations.
class CustomMongodbLoader(MongodbLoader):
    async def aload(self):
        """Asynchronously loads data into Document objects."""
        result = []
        total_docs = await self.collection.count_documents(self.filter_criteria)

        projection = self._construct_projection()

        async for doc in self.collection.find(self.filter_criteria, projection).sort([("timestamp", 1), ("channel.id", 1)]):
            metadata = self._extract_fields(doc, self.metadata_names, default="")

            # Optionally add database and collection names to metadata
            if self.include_db_collection_in_metadata:
                metadata.update(
                    {"database": self.db_name, "collection": self.collection_name}
                )

            # Extract text content from filtered fields or use the entire document
            if self.field_names is not None:
                fields = self._extract_fields(doc, self.field_names, default="")
                texts = [str(value) for value in fields.values()]
                text = " ".join(texts)
            else:
                text = str(doc)

            result.append(Document(page_content=text, metadata=metadata))

        if len(result) != total_docs:
            logger.warning(
                f"Only partial collection of documents returned. "
                f"Loaded {len(result)} docs, expected {total_docs}."
            )

        return result