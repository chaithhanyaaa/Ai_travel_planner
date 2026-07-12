from typing import List, Optional, TypedDict


class TouristSpot(TypedDict, total=False):
    name: str
    latitude: float
    longitude: float


class DistanceInfo(TypedDict):
    from_place: str
    to_place: str
    distance_km: float


class TravelState(TypedDict):
    # User Input
    destination_exists: bool
    destination: str
    budget: float
    days: int
    interests: List[str]

    # Destination Search
    suggested_destinations: List[str]
    user_feedback: Optional[str]

    # Weather
    weather_report: str

    # Tourist Spots
    tourist_spots: List[TouristSpot]

    # NEW
    geocoded_spots: List[TouristSpot]

    # Distance Matrix
    distance_matrix: List[DistanceInfo]

    # Parallel Outputs
    packing_list: List[str]
    budget_plan: str

    # Final Planning
    itinerary: str
    user_feedback_2:Optional[str]
    final_report: str