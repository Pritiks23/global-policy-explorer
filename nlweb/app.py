from flask import Flask, request, render_template_string
import os
from dotenv import load_dotenv
import google.generativeai as genai

from weaviate import WeaviateClient
from weaviate.auth import AuthApiKey
from weaviate.connect import ConnectionParams

load_dotenv()

# Initialize Weaviate v4 client
client = WeaviateClient(
    connection_params=ConnectionParams.from_url(os.getenv("WEAVIATE_URL")),
    auth_client=AuthApiKey(os.getenv("WEAVIATE_API_KEY"))
)

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

app = Flask(__name__)

HTML = """
<!doctype html>
<title>Global Policy Explorer</title>
<h2>Ask a policy question:</h2>
<form method=post>
  <input name=query size=80>
  <input type=submit>
</form>
{% if results %}
  <h3>Results:</h3>
  <ul>
  {% for r in results %}
    <li><b>{{ r['country'] }}</b>: {{ r['clause_text'] }} ({{ r['treaty_name'] }})</li>
  {% endfor %}
  </ul>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        query = request.form["query"]
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
        results = clauses + [{"country": "Summary", "clause_text": summary, "treaty_name": "Gemini"}]

    return render_template_string(HTML, results=results)

if __name__ == "__main__":
    app.run(debug=True)


