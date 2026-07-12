from state import TravelState
from tools.search_tool import search_tool
from llm import llm


def destination_search_node(state: TravelState) -> TravelState:
    """
    Search for travel destinations based on the user's preferences
    and store the best suggestions in the shared state.
    """
    print("destination_search started")

    # -------------------------
    # Build Search Query
    # -------------------------
    query = (
    f"Best travel destinations for a {state['days']}-day trip "
    f"with a budget of {state['budget']} rupees "
    f"for someone interested in {', '.join(state['interests'])}."
    )

    if state["user_feedback"]:
        query += f" Extra specifications: {state['user_feedback']}"

    # -------------------------
    # Retrieve search results
    # -------------------------
    search_results = search_tool.invoke({"query": query})

    # -------------------------
    # Ask the LLM to rank them
    # -------------------------
    prompt = f"""
You are an expert travel planner.

The following search results contain possible travel destinations.

Search Results:
{search_results}

User Preferences:
- Budget: {state["budget"]}
- Days: {state["days"]}
- Interests: {", ".join(state["interests"])}
Choose the 5 BEST travel destinations.

Rules:
- Return ONLY cities, towns, islands, or tourist regions.
- DO NOT return countries.
- DO NOT return states.
- The destinations should be specific enough for itinerary planning.

Return ONLY the destination names.

One destination per line.
"""

    response = llm.invoke(prompt)

    # -------------------------
    # Parse response
    # -------------------------
    destinations = [
        line.strip()
        for line in response.content.split("\n")
        if line.strip()
    ]
    print("destination_serach ended")
    return {
        "suggested_destinations": destinations
    }