import os
import re
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
load_dotenv()

# -------------------------------
# CONFIG (ENV ONLY — no hardcoding)
# -------------------------------
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USERNAME")
NEO4J_PASS = os.getenv("NEO4J_PASSWORD")

if not all([NEO4J_URI, NEO4J_USER, NEO4J_PASS]):
    raise ValueError("Neo4j credentials missing in environment variables")

# -------------------------------
# DRIVER (connection pooling)
# -------------------------------
driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASS),
    max_connection_lifetime=1000,
    max_connection_pool_size=10,
    connection_timeout=10
)

# -------------------------------
# MODEL (load once globally)
# -------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")
EMBEDDING_DIM = model.get_sentence_embedding_dimension()

# -------------------------------
# CREATE VECTOR INDEX (SAFE INIT)
# -------------------------------
def create_vector_index():
    with driver.session() as session:
        session.run("""
            CREATE VECTOR INDEX page_embedding_index IF NOT EXISTS
            FOR (p:Page)
            ON (p.embedding)
            OPTIONS {
              indexConfig: {
                `vector.dimensions`: $dim,
                `vector.similarity_function`: 'cosine'
              }
            }
        """, dim=EMBEDDING_DIM)

# -------------------------------
# KEYWORD CLEANING (FAST)
# -------------------------------
def extract_keywords(query: str):
    query = query.lower()
    query = re.sub(r"[^a-z0-9\s]", " ", query)
    return [w for w in query.split() if len(w) > 2]

# -------------------------------
# SEARCH FUNCTION (MAIN API)
# -------------------------------
def search_best(query: str, top_k: int = 3):
    """
    Returns best matching MOSDAC pages
    """

    if not query:
        return []

    try:
        query_embedding = model.encode(query).tolist()
        keywords = extract_keywords(query)

        with driver.session() as session:
            result = session.run("""
            CALL db.index.vector.queryNodes(
              'page_embedding_index',
              8,
              $embedding
            )
            YIELD node AS p, score AS semantic_score

            OPTIONAL MATCH (p)-[:HAS_KEYWORD]->(k:Keyword)
            WHERE k.name IN $keywords

            WITH p,
                 semantic_score,
                 COUNT(k) AS keyword_score

            RETURN p.name AS name,
                   p.url AS url,
                   (semantic_score * 0.85 +
                    keyword_score * 0.15) AS final_score

            ORDER BY final_score DESC
            LIMIT $top_k
            """,
            embedding=query_embedding,
            keywords=keywords,
            top_k=top_k
            )

            data = result.data()

            # Normalize output
            return [
                {
                    "name": r.get("name"),
                    "url": r.get("url"),
                    "score": round(r.get("final_score", 0), 4)
                }
                for r in data if r.get("url")
            ]

    except Exception as e:
        print("Search error:", e)
        return []

# -------------------------------
# OPTIONAL: CLOSE DRIVER
# -------------------------------
def close():
    driver.close()