from neo4j import GraphDatabase
import google.generativeai as genai
import numpy as np
from scipy.spatial.distance import cosine

# ==== Gemini API Key ====
GEMINI_API_KEY = "AIzaSyBChB9OvBIcW9nL4-w24Gzkiz0GxDwBsTk"
genai.configure(api_key=GEMINI_API_KEY)

# ==== Neo4j Config ====
NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your_neo4j_password"  # 🔁 Replace with the password you used during Neo4j DB setup

# ==== Connect to Neo4j ====
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# ==== Get Embedding using Gemini ====
def get_embedding(text):
    try:
        response = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        return response["embedding"]
    except Exception as e:
        print("Embedding error:", e)
        return None

# ==== Store Embedding into Neo4j ====
def store_text_and_embedding(text, embedding):
    with driver.session() as session:
        session.run("""
            CREATE (n:TextNode {text: $text, embedding: $embedding})
        """, text=text, embedding=embedding)

# ==== Create relationship between similar texts (optional) ====
def create_similarity_relationships(threshold=0.9):
    with driver.session() as session:
        nodes = session.run("MATCH (n:TextNode) RETURN n.text AS text, n.embedding AS embedding, id(n) AS id")
        data = [(record["id"], record["text"], record["embedding"]) for record in nodes]

        for i in range(len(data)):
            for j in range(i+1, len(data)):
                id1, text1, emb1 = data[i]
                id2, text2, emb2 = data[j]
                sim = 1 - cosine(emb1, emb2)
                if sim > threshold:
                    session.run("""
                        MATCH (a), (b) WHERE id(a) = $id1 AND id(b) = $id2
                        MERGE (a)-[:SIMILAR {score: $sim}]->(b)
                    """, id1=id1, id2=id2, sim=sim)

# ==== Query Top Similar Nodes ====
def find_most_similar(input_text, top_k=3):
    input_embedding = get_embedding(input_text)
    if input_embedding is None:
        print("Failed to embed input.")
        return

    with driver.session() as session:
        result = session.run("MATCH (n:TextNode) RETURN n.text AS text, n.embedding AS embedding")
        similarities = []
        for record in result:
            node_text = record["text"]
            node_embedding = record["embedding"]
            score = 1 - cosine(input_embedding, node_embedding)
            similarities.append((node_text, score))

        similarities.sort(key=lambda x: x[1], reverse=True)
        print(f"\n🔍 Top {top_k} similar texts to: \"{input_text}\"")
        for text, score in similarities[:top_k]:
            print(f"🟢 Text: {text} | Similarity: {score:.4f}")

# ==== Main Execution ====
if __name__ == "__main__":
    texts = [
        "AI is transforming the future of technology.",
        "Artificial intelligence helps automate tasks.",
        "Cooking recipes are fun to experiment with.",
        "Machine learning is a part of AI.",
        "Baking cakes requires precise measurement."
    ]

    print("📥 Generating embeddings and storing in Neo4j...")
    for text in texts:
        emb = get_embedding(text)
        if emb:
            store_text_and_embedding(text, emb)

    print("🔗 Creating similarity relationships in graph (optional)...")
    create_similarity_relationships(threshold=0.88)

    print("✅ Done storing nodes and relationships.")

    # Run a similarity query
    user_input = "How is machine learning used in automation?"
    find_most_similar(user_input)
