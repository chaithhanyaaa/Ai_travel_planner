from state import TravelState
from llm import llm


def itinerary_planner_node(state: TravelState) -> TravelState:
    """
    Generate a realistic day-wise itinerary using all
    available planning information.
    """
    print("itenenary node started")

    tourist_spots = "\n".join(
        spot["name"] for spot in state["geocoded_spots"]
    )

    distances = "\n".join(
        f"{item['from_place']} -> {item['to_place']} : {item['distance_km']} km"
        for item in state["distance_matrix"]
    )

    packing = "\n".join(state["packing_list"])

    prompt = f"""
You are an expert travel planner.

Destination:
{state["destination"]}

Trip Duration:
{state["days"]} days

Budget:
{state["budget"]}

User Interests:
{", ".join(state["interests"])}

Weather:
{state["weather_report"]}

Tourist Attractions:
{tourist_spots}

Road Distances:
{distances}

Packing List:
{packing}

Budget Plan:
{state["budget_plan"]}

Instructions:

1. Create a day-wise itinerary.
2. Group nearby attractions together.
3. Avoid visiting places that are far apart on the same day.
4. Consider the weather.
5. Keep the schedule realistic.
6. Stay within the user's budget.

Return only the itinerary.
"""

    response = llm.invoke(prompt)
    print("itenenary node ended")
    return {
        "itinerary": response.content.strip()
    }