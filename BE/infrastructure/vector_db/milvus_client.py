from typing import Optional
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility

from core.config import settings

_collection: Optional[Collection] = None


async def init_milvus():
    """Initialize Milvus cloud connection."""
    global _collection

    # Connect to Milvus Cloud using URI and token
    connections.connect(
        alias="default",
        uri=settings.MILVUS_URI,
        token=settings.MILVUS_TOKEN,
    )

    collection_name = settings.MILVUS_COLLECTION_NAME

    if not utility.has_collection(collection_name):
        # Create collection schema
        fields = [
            FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=settings.EMBEDDING_DIMENSION),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="metadata", dtype=DataType.JSON),
        ]
        schema = CollectionSchema(fields=fields, description="Medical knowledge embeddings")
        _collection = Collection(name=collection_name, schema=schema)

        # Create index for vector similarity search
        index_params = {
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128}
        }
        _collection.create_index(field_name="embedding", index_params=index_params)
    else:
        _collection = Collection(name=collection_name)

    _collection.load()


async def close_milvus():
    global _collection
    if _collection:
        _collection.release()
    connections.disconnect(alias="default")


def get_milvus_client() -> Collection:
    if _collection is None:
        raise RuntimeError("Milvus not initialized. Call init_milvus() first.")
    return _collection
