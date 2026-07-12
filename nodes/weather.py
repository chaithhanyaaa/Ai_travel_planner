from state import TravelState
from tools.search_tool import search_tool
from llm import llm


def weather_node(state: TravelState) -> TravelState:
    """
    Retrieve and summarize the weather for the selected destination.
    """
    print("weather node started")

    destination = state["destination"]

    query = f"Current weather in {destination}"

    search_results = search_tool.invoke(
        {
            "query": query
        }
    )

    prompt = f"""
You are a travel assistant.

Using the search results below, write a concise weather report.

Search Results:
{search_results}

Include:
- Temperature (if available)
- Weather condition
- Any travel advice

Keep it under 120 words.
"""

    response = llm.invoke(prompt)
    print("weather node ended")

    return {
        "weather_report": response.content.strip()

    }