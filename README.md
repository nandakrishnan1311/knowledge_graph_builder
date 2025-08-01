# Knowledge Graph from Text using Gemini Embeddings + Neo4j

## 🚀 Overview
This Python project builds a semantic knowledge graph from raw text using Gemini Embeddings and stores relationships in Neo4j.

## 🔧 Tech Stack
- Python 3.10+
- Gemini API (Google AI)
- Neo4j Graph Database (local or AuraDB)
- NumPy

## 📦 Setup
1. Clone the repo
2. Install dependencies:

3. Set your `.env` file or update the script with:
- GEMINI_API_KEY
- NEO4J_URI, USER, PASSWORD

4. Run:


## 📊 Output
- View the graph at [http://localhost:7474](http://localhost:7474)
- Nodes: Input text chunks
- Edges: Semantic similarity > threshold

## Screenshorts
1.🟦 View All Nodes
Shows all nodes (each node represents a piece of text):
- MATCH (n) RETURN n LIMIT 100;
<img width="1913" height="979" alt="Screenshot (102)" src="https://github.com/user-attachments/assets/94215e6e-849b-4f69-91f4-001d720e6958" />

2.🔗 View All Relationships
Displays all SIMILAR relationships between texts (edges with similarity scores):
- MATCH (a)-[r:SIMILAR]->(b) RETURN a, r, b LIMIT 100;
<img width="1913" height="955" alt="Screenshot (110)" src="https://github.com/user-attachments/assets/d490ad67-b6da-4b9b-ae92-dc8339b1cd60" />
<img width="1913" height="967" alt="Screenshot (104)" src="https://github.com/user-attachments/assets/4b756e06-78d9-44d8-b3a4-8b13631bca16" />
<img width="1913" height="949" alt="Screenshot (106)" src="https://github.com/user-attachments/assets/00c3dba6-fb49-4f4a-b44c-b696eb24414f" />
<img width="1913" height="953" alt="Screenshot (108)" src="https://github.com/user-attachments/assets/9ee68229-6be3-4bdc-9cd4-35eddc399e42" />

3. 💬 View Text and Embeddings
- Returns the raw text and the corresponding embedding vectors:
- MATCH (n:TextNode) RETURN n.text, n.embedding LIMIT 10;
<img width="1919" height="971" alt="Screenshot (112)" src="https://github.com/user-attachments/assets/35b969b4-5510-4d64-b15b-f9b18a205bc7" />

4. 🧠 Query Top Similar Texts
- Lists top similar text pairs with their cosine similarity scores:
- MATCH (a:TextNode)-[r:SIMILAR]->(b:TextNode)
RETURN a.text AS Source, b.text AS SimilarText, r.score AS Similarity
ORDER BY r.score DESC
LIMIT 10;
<img width="1913" height="954" alt="Screenshot (114)" src="https://github.com/user-attachments/assets/7639ec6b-95ee-40f6-873f-0a4c5a476e6d" />

5. 🧰 (Optional) Show Node IDs
- Useful for debugging relationships:
- MATCH (n) RETURN elementId(n), n.text LIMIT 10;
<img width="1913" height="951" alt="Screenshot (116)" src="https://github.com/user-attachments/assets/9e852650-b888-482a-98af-3e693657f14f" />





