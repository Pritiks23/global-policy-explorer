# global-policy-explorer

# 🌍 Global Policy Explorer 

This project uses Weaviate, GraphRAG, and Gemini API to explore global treaties and policy clauses.

## Setup
1. Create a `.env` file from `.env.example` and add your Weaviate and Gemini API keys.
2. Run `weaviate_setup/ingest.py` to load sample data.
3. Run `graphrag/build_graph.py` to build the knowledge graph.
4. Start the app with `python nlweb/app.py`.

## Features
- Semantic search of policy clauses via Weaviate
- Graph-based relationship mapping with GraphRAG
- Natural language query interface powered by Gemini
