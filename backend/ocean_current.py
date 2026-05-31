import requests
import cv2
import numpy as np
from bs4 import BeautifulSoup


class MosdacOceanAnalyzer:
    def __init__(self):
        self.url = "https://mosdac.gov.in/gallery/index.html?ds=ocean&prod=REGNL_*_CUR.gif&date=2026-03-19&count=24#"

    # -------------------------
    # STEP 1: FETCH IMAGE URL (NO SELENIUM)
    # -------------------------
    def fetch_image_url(self):
        try:
            res = requests.get(self.url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            img = soup.find("img", {"id": "msgs"})

            if not img:
                return None

            img_url = img.get("src")

            # Handle relative URL
            if img_url and not img_url.startswith("http"):
                img_url = "https://mosdac.gov.in" + img_url

            return img_url

        except Exception as e:
            print("Fetch image URL error:", e)
            return None

    # -------------------------
    # STEP 2: DOWNLOAD IMAGE
    # -------------------------
    def download_image(self, url):
        try:
            filename = "ocean_current.gif"

            res = requests.get(url, timeout=10)

            with open(filename, "wb") as f:
                f.write(res.content)

            return filename

        except Exception as e:
            print("Download error:", e)
            return None

    # -------------------------
    # STEP 3: ANALYZE IMAGE (OPTIMIZED)
    # -------------------------
    def analyze_image(self, image_path):
        try:
            img = cv2.imread(image_path)

            if img is None:
                return []

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # 🔥 Downscale for speed
            img_small = cv2.resize(img, (200, 200))

            pixels = img_small.reshape(-1, 3)

            speeds = []

            for pixel in pixels:
                r, g, b = pixel

                if r < 20 and g < 20 and b < 20:
                    continue

                if r > 200 and g < 100:
                    speed = 0.7
                elif r > 200 and g > 150:
                    speed = 0.5
                elif g > 200:
                    speed = 0.3
                elif b > 200:
                    speed = 0.1
                else:
                    speed = 0.2

                speeds.append(speed)

            return speeds

        except Exception as e:
            print("Image analysis error:", e)
            return []

    # -------------------------
    # STEP 4: GENERATE REPORT
    # -------------------------
    def generate_report(self, speeds):
        if not speeds:
            return {
                "status": "error",
                "message": "No ocean data extracted"
            }

        avg_speed = float(np.mean(speeds))
        max_speed = float(np.max(speeds))
        min_speed = float(np.min(speeds))

        # Classification
        if max_speed > 0.6:
            condition = "Strong ocean currents"
            impact = "High energy zone affecting weather and marine conditions"
        elif max_speed > 0.3:
            condition = "Moderate ocean currents"
            impact = "Normal ocean activity"
        else:
            condition = "Calm ocean conditions"
            impact = "Stable sea state"

        if avg_speed > 0.5:
            flow = "Fast and active flow"
        elif avg_speed > 0.25:
            flow = "Moderate flow"
        else:
            flow = "Calm flow"

        return {
            "status": "success",
            "avg_speed": round(avg_speed, 3),
            "max_speed": round(max_speed, 3),
            "min_speed": round(min_speed, 3),
            "condition": condition,
            "flow": flow,
            "impact": impact
        }

    # -------------------------
    # MAIN ENTRY FUNCTION
    # -------------------------
    def run(self):
        img_url = self.fetch_image_url()

        if not img_url:
            return {"status": "error", "message": "Image URL not found"}

        img_path = self.download_image(img_url)

        if not img_path:
            return {"status": "error", "message": "Image download failed"}

        speeds = self.analyze_image(img_path)

        return self.generate_report(speeds)