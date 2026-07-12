from state import TravelState
from llm import llm


def packing_planner_node(state: TravelState) -> TravelState:
    """
    Generate a packing list based on the destination,
    trip duration, weather, and user interests.
    """
    print("packing node started")

    prompt = f"""
You are an experienced travel assistant.

Destination:
{state["destination"]}

Trip Duration:
{state["days"]} days

Current Weather:
{state["weather_report"]}

User Interests:
{", ".join(state["interests"])}

Generate a practical packing list.

Consider:
- Weather
- Trip duration
- User activities/interests

Return ONLY the packing items.

One item per line.

Example:
Umbrella
Rain Jacket
Power Bank
Water Bottle
Comfortable Walking Shoes
"""

    response = llm.invoke(prompt)

    packing_list = [
        item.strip()
        for item in response.content.split("\n")
        if item.strip()
    ]

    print("paking node done")

    return {
        "packing_list": packing_list
    }