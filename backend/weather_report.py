import requests
import numpy as np


class CleanClimateEngine:
    def __init__(self):
        self.openmeteo_url = "https://api.open-meteo.com/v1/forecast"
        self.mosdac_url = "https://mosdac.gov.in/apiweather1/weather"

    # =========================================================
    # 🌐 FETCH OPEN-METEO
    # =========================================================
    def fetch_openmeteo(self, lat, lon):
        try:
            params = {
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
                "hourly": "temperature_2m,relative_humidity_2m,precipitation,cloudcover,windspeed_10m,pressure_msl",
                "daily": "precipitation_sum",
                "forecast_days": 1,
                "timezone": "auto"
            }

            res = requests.get(self.openmeteo_url, params=params, timeout=10)

            if res.status_code == 200:
                return res.json()

        except Exception as e:
            print("OpenMeteo error:", e)

        return None

    # =========================================================
    # 🌐 FETCH MOSDAC
    # =========================================================
    def fetch_mosdac(self, lat, lon):
        try:
            url = f"{self.mosdac_url}?lat={lat}&lon={lon}"
            res = requests.get(url, timeout=10)

            if res.status_code == 200:
                return res.json()

        except Exception as e:
            print("MOSDAC error:", e)

        return None

    # =========================================================
    # 🔒 SAFE EXTRACTOR
    # =========================================================
    def safe_get(self, data, *keys):
        try:
            for k in keys:
                data = data[k]
            return data[0] if isinstance(data, list) else data
        except:
            return 0

    # =========================================================
    # 🔥 HEAT INDEX
    # =========================================================
    def heat_index(self, temp, humidity):
        if temp < 27:
            return temp

        hi = (
            -8.784695 +
            1.61139411 * temp +
            2.338549 * humidity -
            0.14611605 * temp * humidity -
            0.012308094 * temp**2 -
            0.016424828 * humidity**2 +
            0.002211732 * temp**2 * humidity +
            0.00072546 * temp * humidity**2 -
            0.000003582 * temp**2 * humidity**2
        )
        return round(hi, 2)

    # =========================================================
    # ⚡ LIGHTNING ESTIMATION
    # =========================================================
    def lightning(self, humidity, rain, cloud):
        score = 0
        score += 2 if humidity > 80 else 0
        score += 2 if rain > 5 else 0
        score += 2 if cloud > 80 else 0

        if score >= 5:
            return "high"
        elif score >= 3:
            return "moderate"
        elif score >= 1:
            return "low"
        return "none"

    # =========================================================
    # 📊 ANALYZE OPEN-METEO
    # =========================================================
    def analyze_openmeteo(self, data):
        temp = self.safe_get(data, "hourly", "temperature_2m")
        humidity = self.safe_get(data, "hourly", "relative_humidity_2m")
        wind = self.safe_get(data, "hourly", "windspeed_10m")
        rain = self.safe_get(data, "hourly", "precipitation")
        pressure = self.safe_get(data, "hourly", "pressure_msl")
        cloud = self.safe_get(data, "hourly", "cloudcover")
        daily_rain = self.safe_get(data, "daily", "precipitation_sum")

        return {
            "temperature": temp,
            "feels_like": self.heat_index(temp, humidity),
            "humidity": humidity,
            "wind_speed": wind,
            "pressure": pressure,
            "rain_value": rain,
            "cloud": cloud,
            "daily_rain": daily_rain,
            "lightning": self.lightning(humidity, rain, cloud)
        }

    # =========================================================
    # 📊 PARSE MOSDAC
    # =========================================================
    def parse_mosdac(self, data):
        try:
            records = data.get("data", [])
            if not records:
                return None

            temps = [float(r["t2"]) for r in records]
            humidity = [float(r["rh2"]) for r in records]
            wind = [float(r["ws10"]) for r in records]
            rain = [float(r["rainc"]) + float(r["rainnc"]) for r in records]

            return {
                "avg_temp": np.mean(temps),
                "max_temp": max(temps),
                "min_temp": min(temps),
                "avg_humidity": np.mean(humidity),
                "avg_wind": np.mean(wind),
                "total_rain": sum(rain)
            }

        except Exception as e:
            print("MOSDAC parse error:", e)
            return None

    # =========================================================
    # 🔀 FUSION ENGINE
    # =========================================================
    def fuse_weather(self, openmeteo, mosdac):
        if not mosdac:
            return openmeteo

        fused = openmeteo.copy()

        try:
            fused["temperature"] = round(
                (openmeteo["temperature"] + mosdac["avg_temp"]) / 2, 2
            )

            fused["humidity"] = round(
                (openmeteo["humidity"] + mosdac["avg_humidity"]) / 2, 2
            )

            fused["wind_speed"] = round(
                (openmeteo["wind_speed"] + mosdac["avg_wind"]) / 2, 2
            )

            # Rain interpretation
            if mosdac["total_rain"] == 0:
                fused["rain"] = "none"
            elif mosdac["total_rain"] < 10:
                fused["rain"] = "moderate"
            else:
                fused["rain"] = "heavy"

            # Extreme heat detection
            if mosdac["max_temp"] > 42:
                fused["alert"] = "extreme_heat"

            return fused

        except Exception as e:
            print("Fusion error:", e)
            return openmeteo

    # =========================================================
    # 🚀 MAIN ENTRY
    # =========================================================
    def generate_report(self, lat, lon):

        # 1. Open-Meteo
        openmeteo_raw = self.fetch_openmeteo(lat, lon)

        if not openmeteo_raw:
            return {
                "status": "error",
                "message": "OpenMeteo failed"
            }

        openmeteo_data = self.analyze_openmeteo(openmeteo_raw)

        # 2. MOSDAC
        mosdac_raw = self.fetch_mosdac(lat, lon)
        mosdac_data = self.parse_mosdac(mosdac_raw) if mosdac_raw else None

        # 3. Fusion
        final_data = self.fuse_weather(openmeteo_data, mosdac_data)

        # 4. Final structured output
        return {
            "status": "success",
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "weather": final_data,
            "sources": {
                "openmeteo": openmeteo_data,
                "mosdac": mosdac_data
            }
        }