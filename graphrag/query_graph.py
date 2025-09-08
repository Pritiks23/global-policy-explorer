import os
from dotenv import load_dotenv

from weaviate import WeaviateClient
from weaviate.auth import AuthApiKey
from weaviate.connect import ConnectionParams

load_dotenv()

# Initialize Weaviate client
client = WeaviateClient(
    connection_params=ConnectionParams.from_url(os.getenv("WEAVIATE_URL")),
    auth_client=AuthApiKey(os.getenv("WEAVIATE_API_KEY"))
)

def fetch_clauses(concept: str, limit: int = 10):
    """
    Query Weaviate for clauses related to a concept.
    Returns a list of dictionaries with treaty_name, country, and clause_text.
    """
    collection = client.collections.get("Clause")
    results = collection.query.near_text(concepts=[concept]).with_limit(limit).fetch_objects(
        properties=["treaty_name", "country", "clause_text"]
    )

    return [
        {
            "treaty_name": obj.properties["treaty_name"],
            "country": obj.properties["country"],
            "clause_text": obj.properties["clause_text"]
        }
        for obj in results.objects
    ]

