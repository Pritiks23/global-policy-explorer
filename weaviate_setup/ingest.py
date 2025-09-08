import os
import json
from dotenv import load_dotenv

from weaviate import WeaviateClient
from weaviate.auth import AuthApiKey
from weaviate.connect import ConnectionParams
from weaviate.classes.config import Configure, Property, DataType

load_dotenv()

# Initialize Weaviate v4 client
client = WeaviateClient(
    connection_params=ConnectionParams.from_url(os.getenv("WEAVIATE_URL")),
    auth_client=AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
    additional_headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")}
)

# Delete all existing collections
client.collections.delete_all()

# Load and create schema from JSON
with open("weaviate_setup/schema.json") as f:
    schema = json.load(f)
    for class_def in schema["classes"]:
        class_name = class_def["class"]
        properties = [
            Property(name=prop["name"], data_type=DataType(prop["dataType"][0]))
            for prop in class_def["properties"]
        ]
        client.collections.create(
            name=class_name,
            properties=properties,
            vector_index_config=Configure.VectorIndex.hnsw()
        )

# Load and ingest data
with open("data/sample_treaties.json") as f:
    for item in json.load(f):
        client.collections.get("Clause").data.insert(properties=item)

