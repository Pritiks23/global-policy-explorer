import json
import networkx as nx
import matplotlib.pyplot as plt
from graphrag.build_graph import build_graph_from_json

# Load sample data
with open("data/sample_treaties.json", "r") as f:
    data = json.load(f)

# Build graph using GraphRAG
#G = build_graph_from_json(data)
# Filter out malformed entries
clean_data = []
for item in data:
    if all(k in item for k in ("country", "treaty", "clause", "outcome")):
        clean_data.append(item)
    else:
        print(f"Skipping malformed entry: {item}")

G = build_graph_from_json(clean_data)


# Color nodes by type
color_map = {
    "country": "skyblue",
    "treaty": "lightgreen",
    "clause": "gold",
    "outcome": "salmon"
}
node_colors = [color_map.get(G.nodes[n].get("type", "treaty"), "gray") for n in G.nodes]

# Draw graph
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1500, font_size=8, arrows=True)
edge_labels = nx.get_edge_attributes(G, "label")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

plt.title("GraphRAG Knowledge Graph")
plt.tight_layout()
plt.savefig("graphrag_visual.png")
