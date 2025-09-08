import os
import networkx as nx
import matplotlib.pyplot as plt
from graphrag.build_graph import build_graph_from_json

# Ensure output folder exists
os.makedirs("graphrag", exist_ok=True)

# Hardcoded treaty data
data = [
    {
        "country": "France",
        "treaty": "Paris Agreement",
        "clause": "Each country shall submit nationally determined contributions to reduce emissions.",
        "outcome": "Countries submit climate action plans"
    },
    {
        "country": "Germany",
        "treaty": "EU Green Deal",
        "clause": "Member states commit to carbon neutrality by 2050.",
        "outcome": "EU-wide carbon neutrality target"
    },
    {
        "country": "Japan",
        "treaty": "Kyoto Protocol",
        "clause": "Annex I countries shall reduce greenhouse gas emissions by an average of 5% below 1990 levels.",
        "outcome": "Binding emission reduction targets"
    },
    {
        "country": "Nigeria",
        "treaty": "African Continental Free Trade Area",
        "clause": "Member states shall eliminate tariffs on 90% of goods over a five-year period.",
        "outcome": "Boosted intra-African trade"
    },
    {
        "country": "United States",
        "treaty": "USMCA",
        "clause": "Parties shall ensure fair labor practices and prohibit forced labor in supply chains.",
        "outcome": "Improved labor standards enforcement"
    },
    {
        "country": "Belgium",
        "treaty": "Digital Services Act",
        "clause": "Platforms must remove illegal content promptly and provide transparency reports.",
        "outcome": "Safer digital environment"
    },
    {
        "country": "Indonesia",
        "treaty": "ASEAN Agreement on Disaster Management",
        "clause": "Member states shall cooperate in disaster risk reduction and emergency response.",
        "outcome": "Regional disaster coordination"
    },
    {
        "country": "Brazil",
        "treaty": "Convention on the Rights of the Child",
        "clause": "States shall ensure that children are protected from economic exploitation.",
        "outcome": "Stronger child labor protections"
    },
    {
        "country": "Chile",
        "treaty": "Escazú Agreement",
        "clause": "Parties shall guarantee access to environmental information and public participation.",
        "outcome": "Enhanced environmental transparency"
    },
    {
        "country": "Canada",
        "treaty": "Global Compact for Migration",
        "clause": "States shall facilitate safe, orderly, and regular migration through international cooperation.",
        "outcome": "Improved global migration governance"
    }
]

# Build graph using GraphRAG
G = build_graph_from_json(data)

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

# Save image
plt.title("GraphRAG Knowledge Graph")
plt.savefig("graphrag/graphrag_visual.png")

