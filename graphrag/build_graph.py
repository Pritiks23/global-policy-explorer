import os
import networkx as nx
from dotenv import load_dotenv

from weaviate import WeaviateClient
from weaviate.auth import AuthApiKey
from weaviate.connect import ConnectionParams

load_dotenv()

# Initialize Weaviate v4 client
client = WeaviateClient(
    connection_params=ConnectionParams.from_url(os.getenv("WEAVIATE_URL")),
    auth_client=AuthApiKey(os.getenv("WEAVIATE_API_KEY"))
)

# Query Clause collection
collection = client.collections.get("Clause")
results = collection.query.fetch_objects(
    properties=["treaty_name", "country", "clause_text"],
    limit=1000  # Adjust as needed
)

# Build graph
G = nx.Graph()
for obj in results.objects:
    clause_text = obj.properties["clause_text"]
    treaty_name = obj.properties["treaty_name"]
    country = obj.properties["country"]

    G.add_node(clause_text, treaty=treaty_name, country=country)
    G.add_edge(country, clause_text)

# Save graph to GML
nx.write_gml(G, "graphrag/policy_graph.gml")
