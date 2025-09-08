import weaviate, json, os
from dotenv import load_dotenv
load_dotenv()

client = weaviate.Client(
    url=os.getenv("WEAVIATE_URL"),
    auth_client_secret=weaviate.AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
    additional_headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")}
)

client.schema.delete_all()
with open("weaviate_setup/schema.json") as f:
    client.schema.create(json.load(f))

with open("data/sample_treaties.json") as f:
    for item in json.load(f):
        client.data_object.create(item, "Clause")

