import copy
import openrouteservice

from config import ORS_API_KEY
from state import TravelState

client = openrouteservice.Client(key=ORS_API_KEY)


def geocoding_node(state: TravelState):
    print("geocoding node started")

    geocoded_spots = []

    for spot in state["tourist_spots"]:

        query = f"{spot['name']}, {state['destination']}"

        try:
            response = client.pelias_search(
                text=query,
                size=1,
            )
        except Exception as e:
            print(f"Geocoding failed for '{query}': {e}")
            continue

        features = response.get("features", [])

        if not features:
            print(f"No coordinates found for '{query}'")
            continue

        coordinates = features[0]["geometry"]["coordinates"]

        

        new_spot = copy.deepcopy(spot)

        new_spot["longitude"] = coordinates[0]
        new_spot["latitude"] = coordinates[1]

        geocoded_spots.append(new_spot)

    print("geocoding node ended")
    return {
        "geocoded_spots": geocoded_spots
    }