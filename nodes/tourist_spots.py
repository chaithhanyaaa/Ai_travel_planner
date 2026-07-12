from state import TravelState
from llm import llm


def tourist_spots_node(state: TravelState):
    """
    Recommend tourist attractions based on the selected destination,
    user interests, and current weather.
    """
    print("tourist node started")

    prompt = f"""
You are an expert travel guide.

Destination:
{state["destination"]}

Trip Duration:
{state["days"]} days

User Interests:
{", ".join(state["interests"])}

Current Weather:
{state["weather_report"]}
Recommend ONLY famous tourist attractions.

Rules:
- Return ONLY real tourist attractions.
- Do NOT return schools.
- Do NOT return colleges.
- Do NOT return hospitals.
- Do NOT return hotels.
- Do NOT return restaurants.
- Do NOT return markets.
- Do NOT return bus stations.
- Do NOT return railway stations.
- example: if in perticular destination give spots in radius 100km ,dont cross that 

The attractions should be places that tourists commonly visit.

Return ONLY attraction names.

One attraction per line.
"""

    response = llm.invoke(prompt)

    tourist_spots = [
        {
            "name": line.strip()
        }
        for line in response.content.split("\n")
        if line.strip()
    ]
    print("tourist node done")

    return {
        "tourist_spots": tourist_spots
    }