import os

from indexing_pipeline.CustomMongodbLoader import CustomMongodbLoader

document_loader: CustomMongodbLoader = CustomMongodbLoader(
    connection_string=os.getenv("MONGODB_URL"),
    db_name=os.getenv("MONGODB_DB"),
    collection_name=os.getenv("MONGODB_COLLECTION"),
    field_names=["author.username", "content"],
    metadata_names=["timestamp", "url", "_id"],
    include_db_collection_in_metadata=False,
    filter_criteria={"processed": False},
)
