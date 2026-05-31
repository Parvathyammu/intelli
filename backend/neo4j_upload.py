import json
import os
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# -------------------------------
# LOAD ENV
# -------------------------------
load_dotenv()


driver = GraphDatabase.driver("neo4j+s://64629b27.databases.neo4j.io", auth=("64629b27", "BpHYODWD371YzPNrRZOsForNVAxuAzVwkV2JaxOXoRk"))


# -------------------------------
# LOAD MODEL
# -------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------------
# LOAD JSON (your file)
# -------------------------------
with open("sitemap.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# -------------------------------
# PREPARE DATA
# -------------------------------
pages = []

for name, obj in data.items():
    url = obj.get("url", "")
    keywords = obj.get("keywords", [])

    # 🔥 Create embedding using name + keywords
    text = name + " " + " ".join(keywords)
    embedding = model.encode(text).tolist()

    pages.append({
        "name": name,
        "url": url,
        "keywords": keywords,
        "embedding": embedding
    })

print(f"Prepared {len(pages)} pages")

# -------------------------------
# CREATE CONSTRAINT
# -------------------------------
def create_constraints(tx):
    tx.run("""
        CREATE CONSTRAINT page_url_unique IF NOT EXISTS
        FOR (p:Page) REQUIRE p.url IS UNIQUE
    """)
    tx.run("""
        CREATE CONSTRAINT keyword_name_unique IF NOT EXISTS
        FOR (k:Keyword) REQUIRE k.name IS UNIQUE
    """)

# -------------------------------
# UPLOAD DATA (BATCH)
# -------------------------------
def upload_data(tx, batch):
    tx.run("""
        UNWIND $batch AS row

        // Create Page
        MERGE (p:Page {url: row.url})
        SET p.name = row.name,
            p.embedding = row.embedding

        // Create Keywords
        WITH p, row
        UNWIND row.keywords AS kw
        MERGE (k:Keyword {name: kw})
        MERGE (p)-[:HAS_KEYWORD]->(k)
    """, batch=batch)

# -------------------------------
# RUN UPLOAD
# -------------------------------
with driver.session() as session:
    session.execute_write(create_constraints)

    BATCH_SIZE = 20
    for i in range(0, len(pages), BATCH_SIZE):
        batch = pages[i:i+BATCH_SIZE]
        session.execute_write(upload_data, batch)
        print(f"Uploaded {i + len(batch)} / {len(pages)}")

driver.close()

print("✅ Upload completed successfully!")