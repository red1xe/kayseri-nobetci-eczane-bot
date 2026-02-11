# services/pharmacy_service.py
import requests
import math
from config import PHARMACIES_DATA_URL

API_URL = PHARMACIES_DATA_URL or ""

def get_pharmacies():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    pharmacies = response.json()
    return normalize_pharmacy_data(pharmacies)

def get_districts(pharmacies):
    return sorted(set(p["district"] for p in pharmacies))

def get_by_district(pharmacies, district):
    return [p for p in pharmacies if p["district"] == district]

def normalize_pharmacy_data(pharmacies):
    """
    Normalize the pharmacy data to ensure consistent formatting and handle missing values.
    """
    for pharmacy in pharmacies:
        pharmacy["id"] = int(pharmacy.get("id", 0))
        pharmacy["name"] = pharmacy.get("name", "Unknown").title()
        pharmacy["address"] = pharmacy.get("address", "Unknown")
        pharmacy["neighborhood"] = pharmacy.get("neighborhood", "Unknown").title()
        pharmacy["district"] = pharmacy.get("district", "Unknown").title()
        pharmacy["phone"] = pharmacy.get("phone", "N/A")
        pharmacy["watchType"] = pharmacy.get("watchType", "Unknown")
        pharmacy["latitude"] = float(pharmacy.get("latitude", 0))
        pharmacy["longitude"] = float(pharmacy.get("longitude", 0))
        pharmacy["distanceKm"] = pharmacy.get("distanceKm", "0 m")
    return pharmacies

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two latitude/longitude points using the Haversine formula.
    """
    R = 6371  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def add_distances(pharmacies, user_lat, user_lon):
    """
    Add distance information to each pharmacy based on the user's location.
    """
    for pharmacy in pharmacies:
        pharmacy["distanceKm"] = f"{calculate_distance(user_lat, user_lon, pharmacy['latitude'], pharmacy['longitude']):.2f} km"
    return pharmacies
