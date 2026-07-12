from langgraph.types import interrupt

from state import TravelState


def human_approval_node(state: TravelState):
    """
    Pause the graph and ask the user whether to
    accept or regenerate the itinerary.
    """

    print("human approval started")

    user_response = interrupt(
        {
            "type": "human_approval",
            "itinerary": state["itinerary"],
        }
    )

    print("human approval resumed")

    if user_response["approved"]:
        return {
            "user_feedback_2": None
        }

    return {
        "user_feedback_2": user_response["feedback"]
    }