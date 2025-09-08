from flask import Flask, request, render_template_string
import weaviate, os
from dotenv import load_dotenv
load_dotenv()

client = weaviate.Client(
    url=os.getenv("WEAVIATE_URL"),
    auth_client_secret=weaviate.AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
    additional_headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")}
)

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
        response = client.query.get("Clause", ["treaty_name", "country", "clause_text"])\
            .with_near_text({"concepts": [query]}).with_limit(5).do()
        results = response["data"]["Get"]["Clause"]
    return render_template_string(HTML, results=results)

if __name__ == "__main__":
    app.run(debug=True)

