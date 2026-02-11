# services/distance_service.py
from geopy.distance import geodesic

def find_nearest(user_location, pharmacies):
    user_coords = (user_location.latitude, user_location.longitude)

    nearest = min(
        pharmacies,
        key=lambda p: geodesic(
            user_coords,
            (float(p["latitude"]), float(p["longitude"]))
        ).km
    )
    return nearest
