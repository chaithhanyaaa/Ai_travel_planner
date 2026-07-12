from langgraph.types import interrupt

from state import TravelState


def human_selection_node(state: TravelState):
    """
    Pause the graph and allow the user to choose a destination
    from the suggested destinations.
    """

    print("human selection node started")

    user_response = interrupt(
        {
            "type": "destination_selection",
            "suggested_destinations": state["suggested_destinations"],
        }
    )

    print("human selection node resumed")

    # User wants new recommendations
    if user_response["choice"] == 0:
        return {
            "user_feedback": user_response["feedback"],
            "destination": "",
        }

    selected_destination = state["suggested_destinations"][
        user_response["choice"] - 1
    ]

    print("human selection node ended")

    return {
        "user_feedback": None,
        "destination": selected_destination,
    }