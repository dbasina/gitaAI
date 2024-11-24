from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import openai
import os

# Flask setup
app = Flask(__name__, static_folder="app/.next")
CORS(app)  # Enable CORS for frontend integration

#  Database keys and index
ELASTIC_CLOUD_ID = "My_deployment:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDA2NzRmYzY4NTBmNjRjNzBhZDgyNjI0MTVmMzYxM2I5JGE0ODIyZTVkYTVlMjRmNTliYTQyODVlZWI1YjJlNzIz"
ELASTIC_API_KEY = "R1FGdlZwTUJtLV9GRml5dlR4bmQ6cmxQSWVSUTBTUHF0QldmRjRYbk91Zw=="
openai.api_key= ""
index = "gita_english_semantic"

es = Elasticsearch(cloud_id=ELASTIC_CLOUD_ID, api_key=ELASTIC_API_KEY)
model = SentenceTransformer("all-MiniLM-L6-v2")
index = "gita_english_semantic"

def generate_embedding(text):
    """Generate embeddings using the SentenceTransformer model."""
    return model.encode(text, convert_to_numpy=True).tolist()

def vector_search(es, index, query, top_k=5):
    """Perform a vector search in Elasticsearch."""
    embedding = generate_embedding(query)
    search_query = {
        "size": top_k,
        "_source": ["authorName", "verseNumber", "description"],
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": embedding}
                }
            }
        }
    }
    response = es.search(index=index, body=search_query)
    return response["hits"]["hits"]

def format_results_for_gpt(results):
    """Format Elasticsearch results for GPT."""
    formatted = "Relevant verses from the Gita:\n\n"
    for i, result in enumerate(results, start=1):
        source = result["_source"]
        formatted += f"{i}. {source['authorName']}:\n"
        formatted += f"   \"{source['description']}\"\n\n"
    return formatted

def send_to_gpt(prompt):
    """Send formatted results to OpenAI's GPT for summarization."""
    system_prompt =f"""You are a motivational speaker that offers spiritual guidance.
                      - You are given a spiritual leader's insights from the Gita.
                      - assume that the verses given to you were generated by yourself after reading the Gita
                      - The user came to you to seek spiritual guidance
                      - determine the verses that are highly relevant to the user's scenario
                      - using these verses as inspiration, interpret them and write an inspiring message to the user about what gita has to say about their situation,
                      """
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error with GPT API: {e}")
        return None

# Serve React static files
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    # If the file exists in the React build folder, serve it
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        # Otherwise, serve the main React index.html file
        return send_from_directory(app.static_folder, "index.html")

# Flask route
@app.route("/api/gita", methods=["POST"])
def gita_response():
    data = request.json
    query = data.get("query")
    

    if not query:
        return jsonify({"error": "Query is required"}), 400

    try:
        # Step 1: Perform Semantic Search
        search_results = vector_search(es, index, query, top_k=5)

        # Step 2: Format Results for GPT
        formatted_results = format_results_for_gpt(search_results)

        # Step 3: Send to GPT
        gpt_response = send_to_gpt(formatted_results)

        return jsonify({"response": gpt_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)