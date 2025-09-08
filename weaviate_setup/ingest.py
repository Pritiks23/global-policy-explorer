import os
import json
from dotenv import load_dotenv

from weaviate import WeaviateClient
from weaviate.auth import AuthApiKey
from weaviate.connect import ConnectionParams
from weaviate.classes.config import Property, DataType, Configure

load_dotenv()

# Initialize Weaviate v4 client (no OpenAI header)
client = WeaviateClient(
    connection_params=ConnectionParams.from_url(os.getenv("WEAVIATE_URL")),
    auth_client=AuthApiKey(os.getenv("WEAVIATE_API_KEY"))
)

# Delete all existing collections
client.collections.delete_all()

# Create Clause collection based on schema
client.collections.create(
    name="Clause",
    description="Policy clauses from global treaties",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(),
    properties=[
        Property(name="treaty_name", data_type=DataType.TEXT),
        Property(name="country", data_type=DataType.TEXT),
        Property(name="clause_text", data_type=DataType.TEXT)
    ]
)

# Load and ingest data
with open("data/sample_treaties.json") as f:
    for item in json.load(f):
        client.collections.get("Clause").data.insert(properties=item)

