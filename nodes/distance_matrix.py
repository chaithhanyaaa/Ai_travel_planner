import openrouteservice

from config import ORS_API_KEY
from state import TravelState

client = openrouteservice.Client(key=ORS_API_KEY)


def distance_matrix_node(state: TravelState) -> TravelState:
    """
    Compute road distances between every pair of tourist spots
    using the OpenRouteService Matrix API.
    """
    print("matrix node started")

    tourist_spots = state["geocoded_spots"]

    if not tourist_spots:
        print("No geocoded spots available - skipping distance matrix")
        return {"distance_matrix": []}

    coordinates = [
        (spot["longitude"], spot["latitude"])
        for spot in tourist_spots
    ]

    try:
        response = client.distance_matrix(
            locations=coordinates,
            profile="driving-car",
            metrics=["distance"],
        )
    except Exception as e:
        print(f"Distance matrix request failed: {e}")
        return {"distance_matrix": []}

    distances = response["distances"]

    print("\nDistance Matrix Returned By ORS\n")
    for row in distances:
        print(row)

    distance_matrix = []

    n = len(tourist_spots)

    for i in range(n):
        for j in range(i + 1, n):

            distance = distances[i][j]

            # Skip if ORS couldn't compute a route
            if distance is None:
                print(
                    f"Skipping route: "
                    f"{tourist_spots[i]['name']} -> "
                    f"{tourist_spots[j]['name']} "
                    "(No drivable route found)"
                )
                continue

            distance_matrix.append(
                {
                    "from_place": tourist_spots[i]["name"],
                    "to_place": tourist_spots[j]["name"],
                    "distance_km": round(distance / 1000, 2),
                }
            )

    print("matrix node done")
    return {
      "distance_matrix": distance_matrix
  }