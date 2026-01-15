from langchain_community.document_loaders.mongodb import MongodbLoader
from langchain_core.documents import Document
import logging

from typing import AsyncIterator
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

# CustomMongodbLoader is a subclass of MongodbLoader that overrides the `alazy_load` method.
# We need to override this method to ensure that the documents are loaded in the correct order.
# The order is important because we are handling conversations.
#
# Original code from langchain_community.document_loaders.mongodb.MongodbLoader
class CustomMongodbLoader(MongodbLoader):
    """Custom MongoDB loader to process documents as needed."""

    async def alazy_load(self) -> AsyncIterator[Document]:
        """Asynchronously yields Document objects one at a time.

        Yields:
            Document: A document from the MongoDB collection.
        """
        projection = self._construct_projection()

        async for doc in self.collection.find(self.filter_criteria, projection).sort([("channel.id", 1), ("timestamp", 1)]):
            yield self._process_document(doc)
