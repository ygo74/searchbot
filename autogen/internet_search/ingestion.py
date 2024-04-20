from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


# Init client
client = QdrantClient(url="http://localhost:6333")


# Create collection
client.create_collection(
    collection_name="test_collection",
    vectors_config=VectorParams(size=4, distance=Distance.DOT),
)