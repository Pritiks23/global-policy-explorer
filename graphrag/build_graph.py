import os
import json
import networkx as nx
from dotenv import load_dotenv

from weaviate import WeaviateClient
from weaviate.auth import AuthApiKey
from weaviate.connect import ConnectionParams

load_dotenv()

# --- Weaviate-based graph construction ---
def build_graph_from_weaviate():
    client = WeaviateClient(
        connection_params=ConnectionParams.from_url(
            os.getenv("WEAVIATE_URL"),
            grpc_port=50051  # Required for v4
        ),
        auth_client=AuthApiKey(os.getenv("WEAVIATE_API_KEY"))
    )

    collection = client.collections.get("Clause")
    results = collection.query.fetch_objects(
        properties=["treaty_name", "country", "clause_text"],
        limit=1000
    )

    G = nx.Graph()
    for obj in results.objects:
        clause_text = obj.properties["clause_text"]
        treaty_name = obj.properties["treaty_name"]
        country = obj.properties["country"]

        G.add_node(clause_text, treaty=treaty_name, country=country, type="clause")
        G.add_node(country, type="country")
        G.add_node(treaty_name, type="treaty")

        G.add_edge(country, treaty_name, label="participates_in")
        G.add_edge(treaty_name, clause_text, label="commits_to")

    nx.write_gml(G, "graphrag/policy_graph.gml")
    return G

# --- JSON-based graph construction for visualization ---
def build_graph_from_json(data):
    G = nx.DiGraph()
    for item in data:
        country = item["country"]
        treaty = item["treaty"]
        clause = item["clause"]
        outcome = item["outcome"]

        G.add_node(country, type="country")
        G.add_node(treaty, type="treaty")
        G.add_node(clause, type="clause")
        G.add_node(outcome, type="outcome")

        G.add_edge(country, treaty, label="participates_in")
        G.add_edge(treaty, clause, label="commits_to")
        G.add_edge(clause, outcome, label="results_in")
    return G

