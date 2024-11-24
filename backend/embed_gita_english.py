from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch, helpers
import json
from tqdm import tqdm

# Load the SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text):
    """
    Generate embeddings for a given text using the SentenceTransformer model.
    """
    try:
        embedding = model.encode(text, convert_to_numpy=True).tolist()
        return embedding
    except Exception as e:
        print(f"Error generating embedding for text '{text[:30]}...': {e}")
        return None

def add_embeddings_and_upload_to_elasticsearch(input_file, es, index_name):
    """
    Add embeddings to Gita English JSON data and upload to Elasticsearch.
    """
    with open(input_file, "r", encoding="utf-8") as infile:
        data = json.load(infile)  # Load the original Gita English data

    # Prepare Elasticsearch index mapping
    if not es.indices.exists(index=index_name):
        mapping = {
            "mappings": {
                "properties": {
                    "authorName": {"type": "text"},
                    "description": {"type": "text"},
                    "id": {"type": "integer"},
                    "lang": {"type": "keyword"},
                    "language_id": {"type": "integer"},
                    "verseNumber": {"type": "integer"},
                    "verse_id": {"type": "integer"},
                    "embedding": {
                        "type": "dense_vector",
                        "dims": 384  # Update to match embedding size
                    }
                }
            }
        }
        es.indices.create(index=index_name, body=mapping)
        print(f"Created index: {index_name}")

    # Add embeddings and upload data
    actions = []
    for entry in tqdm(data, desc="Processing entries", unit="entry"):
        try:
            # Generate embeddings for the description
            embedding = generate_embedding(entry["description"])
            if embedding:
                entry["embedding"] = embedding
                # Add entry to Elasticsearch bulk upload actions
                actions.append({
                    "_index": index_name,
                    "_source": entry
                })
            else:
                print(f"Skipping entry due to embedding failure: {entry.get('id', 'Unknown ID')}")
        except Exception as e:
            print(f"Error processing entry {entry.get('id', 'Unknown ID')}: {e}")

    # Bulk upload to Elasticsearch
    helpers.bulk(es, actions)
    print(f"Uploaded {len(actions)} entries to Elasticsearch index '{index_name}'")

# Example usage
if __name__ == "__main__":
    ELASTIC_CLOUD_ID = "My_deployment:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDA2NzRmYzY4NTBmNjRjNzBhZDgyNjI0MTVmMzYxM2I5JGE0ODIyZTVkYTVlMjRmNTliYTQyODVlZWI1YjJlNzIz"
    ELASTIC_API_KEY = "R1FGdlZwTUJtLV9GRml5dlR4bmQ6cmxQSWVSUTBTUHF0QldmRjRYbk91Zw=="
    # Create the client instance
    es = Elasticsearch(
        # For local development
        cloud_id=ELASTIC_CLOUD_ID,
        api_key=ELASTIC_API_KEY,
    )
    input_file = "gita_english.json"
    index_name = "gita_english_semantic"
    #add_embeddings_and_upload_to_elasticsearch(input_file, es, index_name)
