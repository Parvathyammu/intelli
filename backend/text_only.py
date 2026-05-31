import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class WebScraper:
    def __init__(self, timeout=10):
        self.timeout = timeout

    # =====================================================
    # FETCH (FAST)
    # =====================================================
    def fetch_html(self, url):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=self.timeout)

            if res.status_code == 200:
                return res.text

        except Exception as e:
            print("Fetch error:", e)

        return None

    # =====================================================
    # SELENIUM FALLBACK
    # =====================================================
    def fetch_with_selenium(self, url):
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

            driver = webdriver.Chrome(options=options)
            driver.get(url)
            driver.implicitly_wait(5)

            html = driver.page_source
            driver.quit()

            return html

        except Exception as e:
            print("Selenium error:", e)
            return None

    # =====================================================
    # PARSE CONTENT
    # =====================================================
    def parse(self, html, base_url):
        soup = BeautifulSoup(html, "html.parser")

        # ---------- TITLE ----------
        title = soup.title.string.strip() if soup.title else "No title"

        # ---------- TEXT ----------
        paragraphs = soup.find_all("p")
        text_data = []

        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 50:
                text_data.append(text)

        # ---------- LINKS ----------
        links = [
            urljoin(base_url, a.get("href"))
            for a in soup.find_all("a", href=True)
        ]

        # ---------- IMAGES ----------
        images = [
            urljoin(base_url, img.get("src"))
            for img in soup.find_all("img", src=True)
        ]

        # ---------- CLEAN ----------
        unique_links = list(dict.fromkeys(links))  # preserve order
        unique_images = list(dict.fromkeys(images))

        result = {
            "title": title,
            "top_text": text_data[:5],
            "links": unique_links[:10],
            "images": unique_images[:10]
        }

        # =====================================================
        # SPECIAL CONDITION: MANY LINKS
        # =====================================================
        if len(unique_links) > 7:
            result["note"] = {
                "message": "Visit this URL for related maps and reports",
                "url": base_url,
                "preview": text_data[:3]
            }

        return result

    # =====================================================
    # MAIN SCRAPER
    # =====================================================
    def scrape(self, url):
        html = self.fetch_html(url)

        # fallback if empty / JS-heavy
        if not html or len(html) < 1000:
            html = self.fetch_with_selenium(url)

        if not html:
            return {
                "status": "error",
                "message": "Failed to load page"
            }

        data = self.parse(html, url)

        return {
            "status": "success",
            "data": data
        }


# =====================================================
# PUBLIC FUNCTION
# =====================================================
def scrape_website(url):
    scraper = WebScraper()
    return scraper.scrape(url)