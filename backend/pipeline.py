import re
import spacy
import requests
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

import weather_report
import text_only
import ocean_current
import mosdac_data

from geopy.geocoders import Nominatim

# =========================================================
# INIT (load once)
# =========================================================
nlp = spacy.load("en_core_web_sm")
geolocator = Nominatim(user_agent="climate_app")

weather_engine = weather_report.CleanClimateEngine()
ocean_engine = ocean_current.MosdacOceanAnalyzer()

DEFAULT_LAT = 9.9312
DEFAULT_LON = 76.2673  # Kochi fallback

# =========================================================
# KEYWORDS (regex compiled)
# =========================================================
WEATHER_PATTERN = re.compile(r"\b(weather|temperature|humidity|wind|storm|climate|cyclone)\b")
OCEAN_PATTERN = re.compile(r"\b(ocean|sea|current|wave|marine|cyclone)\b")
SOLAR_PATTERN = re.compile(r"\b(solar|sun|radiation|sunlight|flux)\b")
RAIN_PATTERN = re.compile(
    r"\b(heavy rain|rainfall|downpour|torrential rain|cloudburst|monsoon|rain)\b"
)

# =========================================================
# LOCATION
# =========================================================
def extract_location(query):
    doc = nlp(query)
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            return ent.text
    return None


def get_lat_lon(place):
    try:
        if place:
            loc = geolocator.geocode(place, timeout=5)
            if loc:
                return loc.latitude, loc.longitude
    except:
        pass
    return DEFAULT_LAT, DEFAULT_LON


# =========================================================
# INTENT
# =========================================================
def detect_intent(query):
    q = query.lower()

    return {
        "weather": bool(WEATHER_PATTERN.search(q)),
        "ocean": bool(OCEAN_PATTERN.search(q)),
        "solar": bool(SOLAR_PATTERN.search(q)),
        "rain": bool(RAIN_PATTERN.search(q)),
    }


# =========================================================
# ☀️ SOLAR
# =========================================================
@lru_cache(maxsize=50)
def fetch_solar_data(lat, lon):
    try:
        url = f"https://mosdac.gov.in/apienergy/solar?lat={lat}&lon={lon}"
        res = requests.get(url, timeout=5)
        return res.json() if res.status_code == 200 else None
    except:
        return None


def parse_solar(data):
    try:
        if not data:
            return None

        flux = [float(d["flux"]) for d in data]
        temps = [float(d["temp"]) for d in data]

        return {
            "max_flux": max(flux),
            "avg_flux": round(sum(flux) / len(flux), 2),
            "solar_level": (
                "very_high" if max(flux) > 1000 else
                "high" if max(flux) > 700 else
                "moderate" if max(flux) > 300 else "low"
            ),
            "avg_temp": round(sum(temps) / len(temps), 2)
        }
    except:
        return None


# =========================================================
# 🌧 HEAVY RAIN
# =========================================================
@lru_cache(maxsize=10)
def fetch_rain():
    try:
        url = "https://mosdac.gov.in/app_php/getCurrent_hr_cb.php"
        res = requests.get(url, timeout=5)
        return res.json() if res.status_code == 200 else []
    except:
        return []


def parse_rain(raw_data, lat, lon, max_km=300):

    def distance(a, b, c, d):
        return ((a - c)**2 + (b - d)**2)**0.5 * 111

    try:
        # -----------------------------
        # 1. Extract JSON safely
        # -----------------------------
        if isinstance(raw_data, str):
            raw_data = raw_data.split("$")[-1]

        import json
        data = raw_data if isinstance(raw_data, dict) else json.loads(raw_data)

        features = data.get("features", [])

        cleaned = []

        for item in features:
            props = item.get("properties", {})
            geom = item.get("geometry", {})

            coords = geom.get("coordinates", [])
            if len(coords) < 2:
                continue

            lon2, lat2 = coords[0], coords[1]
            d = distance(lat, lon, lat2, lon2)

            if d > max_km:
                continue  # ❌ remove far points

            cities_raw = props.get("CITIES", "")
            cities = [c.strip() for c in cities_raw.split(",") if c.strip()]

            # ❌ skip entries with no useful info
            if not cities and float(props.get("RADIUS", 0)) < 10:
                continue

            cleaned.append({
                "cities": cities if cities else ["Unknown Area"],
                "distance_km": round(d, 2),
                "radius": float(props.get("RADIUS", 0)),
                "time": props.get("DATETIME")
            })

        # -----------------------------
        # 2. Remove duplicates (by location)
        # -----------------------------
        unique = {}
        for r in cleaned:
            key = tuple(r["cities"])
            if key not in unique or r["distance_km"] < unique[key]["distance_km"]:
                unique[key] = r

        results = list(unique.values())

        # -----------------------------
        # 3. Sort (closest + strongest)
        # -----------------------------
        results.sort(key=lambda x: (x["distance_km"], -x["radius"]))

        # -----------------------------
        # 4. Limit results
        # -----------------------------
        return results[:5]

    except Exception as e:
        print("Rain parse error:", e)
        return []


# =========================================================
# MAIN PIPELINE
# =========================================================
def run_pipeline(query):

    result = {
        "query": query,
        "weather": None,
        "ocean": None,
        "solar": None,
        "heavy_rain": None,
        "mosdac": None,
        "status": "success"
    }

    # ---------------- LOCATION ----------------
    intent = detect_intent(query)
    place = extract_location(query)
    lat, lon = get_lat_lon(place)

    # ---------------- MOSDAC SEARCH ----------------
    try:
        mosdac_results = mosdac_data.search_best(query)
        if mosdac_results:
            result["mosdac"] = mosdac_results[0]["name"]
    except:
        pass

    # ---------------- PARALLEL EXECUTION ----------------
    with ThreadPoolExecutor() as executor:
        futures = {}

        if intent["weather"]:
            futures["weather"] = executor.submit(
                weather_engine.generate_report, lat, lon
            )

        if intent["ocean"]:
            futures["ocean"] = executor.submit(ocean_engine.run)

        if intent["solar"]:
            futures["solar"] = executor.submit(
                lambda: parse_solar(fetch_solar_data(lat, lon))
            )

        if intent["rain"]:
            futures["heavy_rain"] = executor.submit(
                lambda: parse_rain(fetch_rain(), lat, lon)
            )

        for key, f in futures.items():
            try:
                result[key] = f.result()
            except:
                result[key] = None

    # ---------------- FINAL CHECK ----------------
    if not any([
        result["weather"],
        result["ocean"],
        result["solar"],
        result["heavy_rain"],
        result["mosdac"]
    ]):
        result["status"] = "no_data"

    return result