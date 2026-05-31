import requests
import json


class ClimateIntelligenceSystem:
    def __init__(self):
        self.api_url = "https://api.open-meteo.com/v1/forecast"

    # -------------------------
    # FETCH DATA
    # -------------------------
    def fetch(self, lat, lon):
        params = {
            "latitude": lat,
            "longitude": lon,

            "current_weather": True,

            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "cloudcover",
                "windspeed_10m",
                "pressure_msl"
            ],

            "daily": [
                "precipitation_sum",
                "windspeed_10m_max"
            ],

            "timezone": "auto"
        }

        res = requests.get(self.api_url, params=params)

        if res.status_code != 200:
            return None

        return res.json()

    # -------------------------
    # WEATHER ANALYSIS
    # -------------------------
    def weather_analysis(self, data):
        current = data.get("current_weather", {})

        return {
            "temperature": current.get("temperature"),
            "wind_speed": current.get("windspeed"),
            "wind_direction": current.get("winddirection")
        }

    # -------------------------
    # RAIN ANALYSIS
    # -------------------------
    def rain_analysis(self, data):
        rain = data["hourly"]["precipitation"][0]

        if rain == 0:
            status = "No Rain"
        elif rain < 2:
            status = "Light Rain"
        elif rain < 10:
            status = "Moderate Rain"
        else:
            status = "Heavy Rain"

        return {"rain_mm": rain, "status": status}

    # -------------------------
    # STORM DETECTION
    # -------------------------
    def storm_analysis(self, data):
        wind = data["hourly"]["windspeed_10m"][0]
        rain = data["hourly"]["precipitation"][0]
        cloud = data["hourly"]["cloudcover"][0]

        score = 0

        if wind > 40:
            score += 3
        elif wind > 25:
            score += 2

        if rain > 10:
            score += 3
        elif rain > 5:
            score += 2

        if cloud > 80:
            score += 2

        if score >= 6:
            level = "Severe Storm ⚡"
        elif score >= 4:
            level = "Storm Likely ⛈"
        elif score >= 2:
            level = "Windy/Cloudy"
        else:
            level = "No Storm"

        return {
            "wind": wind,
            "rain": rain,
            "cloud": cloud,
            "storm_level": level
        }

    # -------------------------
    # FLOOD RISK
    # -------------------------
    def flood_risk(self, data):
        rain_daily = data["daily"]["precipitation_sum"][0]

        if rain_daily > 100:
            risk = "Severe Flood Risk 🌊"
        elif rain_daily > 50:
            risk = "Moderate Flood Risk"
        elif rain_daily > 20:
            risk = "Low Flood Risk"
        else:
            risk = "No Flood Risk"

        return {
            "daily_rain_mm": rain_daily,
            "flood_risk": risk
        }

    # -------------------------
    # CYCLONE RISK (basic logic)
    # -------------------------
    def cyclone_risk(self, data):
        wind = data["hourly"]["windspeed_10m"][0]
        pressure = data["hourly"]["pressure_msl"][0]

        if wind > 60 and pressure < 1000:
            level = "High Cyclone Risk 🌀"
        elif wind > 40:
            level = "Possible Cyclonic Activity"
        else:
            level = "No Cyclone Risk"

        return {
            "wind": wind,
            "pressure": pressure,
            "cyclone_risk": level
        }

    # -------------------------
    # FINAL REPORT
    # -------------------------
    def generate_report(self, lat, lon):
        data = self.fetch(lat, lon)

        if not data:
            return {"error": "API failed"}

        weather = self.weather_analysis(data)
        rain = self.rain_analysis(data)
        storm = self.storm_analysis(data)
        flood = self.flood_risk(data)
        cyclone = self.cyclone_risk(data)

        report = {
            "location": {"lat": lat, "lon": lon},
            "weather": weather,
            "rain": rain,
            "storm": storm,
            "flood": flood,
            "cyclone": cyclone
        }

        print("\n🔥 COMPLETE CLIMATE REPORT:\n")
        print(json.dumps(report, indent=2))

        return report


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    engine = ClimateIntelligenceSystem()

    # Example: Kochi
    lat = 9.9312
    lon = 76.2673

    engine.generate_report(lat, lon)