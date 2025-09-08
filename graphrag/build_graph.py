import networkx as nx
import weaviate, os
from dotenv import load_dotenv
load_dotenv()

client = weaviate.Client(
    url=os.getenv("WEAVIATE_URL"),
    auth_client_secret=weaviate.AuthApiKey(os.getenv("WEAVIATE_API_KEY"))
)

G = nx.Graph()
results = client.query.get("Clause", ["treaty_name", "country", "clause_text"]).do()

for clause in results["data"]["Get"]["Clause"]:
    G.add_node(clause["clause_text"], treaty=clause["treaty_name"], country=clause["country"])
    G.add_edge(clause["country"], clause["clause_text"])

nx.write_gml(G, "graphrag/policy_graph.gml")

