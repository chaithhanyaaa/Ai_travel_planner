from state import TravelState
from llm import llm


def final_report_node(state: TravelState) -> TravelState:
    """
    Generate the final travel report.
    """
    print("final node started")

    prompt = f"""
Create a professional travel report.

Destination:
{state["destination"]}

Weather:
{state["weather_report"]}

Tourist Attractions:
{", ".join(spot["name"] for spot in state["tourist_spots"])}

Packing List:
{", ".join(state["packing_list"])}

Budget Plan:
{state["budget_plan"]}

Itinerary:
{state["itinerary"]}

Produce a clean, well-formatted report.
"""

    response = llm.invoke(prompt)
    print("final node ended")
    return {
        "final_report": response.content.strip()
    }