import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import os
import re

ROOT_URL = "https://mosdac.gov.in/sitemap"
SAVE_FOLDER = "mosdac_scraped"
FILE_LIMIT = 100

os.makedirs(SAVE_FOLDER, exist_ok=True)


def safe_filename(url):
    name = url.replace("https://", "").replace("http://", "")
    return re.sub(r'[<>:"/\\|?*#=]', '_', name)[:150]


def get_page_data(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        content = soup.find("div", id="content")
        if not content:
            return "", []

        text = content.get_text(separator="\n", strip=True)

        links = []
        for a in soup.find_all("a", href=True):
            links.append(urljoin(url, a["href"]))

        return text, links

    except Exception as e:
        print("Error:", e)
        return "", []


def save_page(url, text):
    filename = safe_filename(url) + ".json"
    path = os.path.join(SAVE_FOLDER, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump({"url": url, "text": text}, f, indent=2, ensure_ascii=False)

    print("Saved:", filename)


def crawl(root_url):
    visited = set()
    queue = [root_url]
    count = 0

    while queue and count < FILE_LIMIT:
        url = queue.pop(0)

        if url in visited:
            continue

        visited.add(url)
        print("Visiting:", url)

        text, links = get_page_data(url)

        if text:
            save_page(url, text)
            count += 1

        for link in links:
            if urlparse(link).netloc == urlparse(root_url).netloc:
                if link not in visited:
                    queue.append(link)


crawl(ROOT_URL)