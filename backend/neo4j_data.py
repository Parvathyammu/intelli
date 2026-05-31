import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from neo4j import Driver, GraphDatabase
from sentence_transformers import SentenceTransformer
import json
import time

# 🔐 FIX YOUR PASSWORD (do not expose publicly)
driver: Driver = GraphDatabase.driver("neo4j+s://64629b27.databases.neo4j.io", auth=("64629b27", "BpHYODWD371YzPNrRZOsForNVAxuAzVwkV2JaxOXoRk"))


# 🔥 Load embedding model (fast + good)
model = SentenceTransformer('all-MiniLM-L6-v2')

visited = set()

# -------------------------------
# URL FILTER
# -------------------------------
def is_valid(url):
    parsed = urlparse(url)
    return "mosdac.gov.in" in parsed.netloc

# -------------------------------
# PAGE SCRAPER
# -------------------------------
def get_page_data(url):
    try:
        res = requests.get(url, timeout=5)
        status = res.status_code

        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.title.string.strip() if soup.title else ""
        content = soup.get_text(" ", strip=True)[:5000]  # limit text

        # 🔥 Create embedding
        embedding = model.encode(content).tolist()

        links = set()
        for a in soup.find_all("a", href=True):
            link = urljoin(url, a['href'])
            if is_valid(link):
                links.add(link)

        return {
            "url": url,
            "status": status,
            "title": title,
            "content": content,
            "embedding": embedding,
            "links": list(links)
        }

    except Exception as e:
        return {
            "url": url,
            "status": 500,
            "title": "",
            "content": "",
            "embedding": [],
            "links": []
        }

# -------------------------------
# 🔥 BATCH INSERT (OPTIMIZED)
# -------------------------------
def save_batch(session, batch):
    session.run("""
        UNWIND $batch AS row
        MERGE (p:Page {url: row.url})
        SET p.status = row.status,
            p.title = row.title,
            p.content = row.content,
            p.embedding = row.embedding

        WITH p, row
        UNWIND row.links AS link
        MERGE (p2:Page {url: link})
        MERGE (p)-[:LINKS_TO]->(p2)
    """, batch=batch)

# -------------------------------
# CRAWLER
# -------------------------------
def crawl(start_urls, max_pages=200, batch_size=10):
    with driver.session() as session:
        queue = list(start_urls)
        batch = []

        while queue and len(visited) < max_pages:
            url = queue.pop(0)

            if url in visited:
                continue

            print("Crawling:", url)
            visited.add(url)

            data = get_page_data(url)
            batch.append(data)

            for link in data["links"]:
                if link not in visited:
                    queue.append(link)

            # 🔥 Batch write
            if len(batch) >= batch_size:
                save_batch(session, batch)
                batch = []

            time.sleep(1)

        # Save remaining
        if batch:
            save_batch(session, batch)

# -------------------------------
# LOAD SITEMAP
# -------------------------------
with open("sitemap.json") as f:
    data = json.load(f)

start_urls = list(data.values())

crawl(start_urls, max_pages=200)