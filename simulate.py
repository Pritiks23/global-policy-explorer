import os
from dotenv import load_dotenv
import google.generativeai as genai
from weaviate import WeaviateClient
from weaviate.auth import AuthApiKey
from weaviate.connect import ConnectionParams

os.environ["WEAVIATE_URL"] = "http://localhost:8080"
os.environ["WEAVIATE_API_KEY"] = ""
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-pro")

client = WeaviateClient(
    connection_params=ConnectionParams.from_url(os.environ["WEAVIATE_URL"]),
    auth_client=AuthApiKey(os.environ["WEAVIATE_API_KEY"])
)

client.schema.create_class({
    "class": "Clause",
    "vectorizer": "none",
    "properties": [
        {"name": "treaty_name", "dataType": ["text"]},
        {"name": "country", "dataType": ["text"]},
        {"name": "clause_text", "dataType": ["text"]}
    ]
})

client.data_object.create({
    "treaty_name": "Paris Agreement",
    "country": "France",
    "clause_text": "France agrees to reduce carbon emissions by 40% by 2030."
}, class_name="Clause", vector=[0.1]*768)

query = "What is the Paris Agreement?"
response = client.query.get(
    class_name="Clause",
    properties=["treaty_name", "country", "clause_text"]
).with_near_text({"concepts": [query]}).with_limit(5).do()

clauses = response["data"]["Get"]["Clause"]
prompt = "Summarize and compare the following policy clauses:\n"
for clause in clauses:
    prompt += f"- {clause['country']} ({clause['treaty_name']}): {clause['clause_text']}\n"

gemini_response = model.generate_content(prompt)
summary = gemini_response.text

print("--- Clauses ---")
for clause in clauses:
    print(f"{clause['country']} ({clause['treaty_name']}): {clause['clause_text']}")
print("\n--- Gemini Summary ---")
print(summary)
