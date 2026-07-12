from state import TravelState
from tools.search_tool import search_tool


def input_validation_node(state: TravelState):
    print("input validation started....")
    """
    Validate user input before the graph proceeds.

    Validates:
    - Budget is positive
    - Days are positive
    - Interests are provided
    - If a destination is provided, verify it exists.
    """

    # -------------------------
    # Budget
    # -------------------------
    if state["budget"] <= 0:
        raise ValueError("Budget must be greater than zero.")

    # -------------------------
    # Days
    # -------------------------
    if state["days"] <= 0:
        raise ValueError("Days must be greater than zero.")

    # -------------------------
    # Interests
    # -------------------------
    interests = [
        interest.strip()
        for interest in state["interests"]
        if interest.strip()
    ]

    if not interests:
        raise ValueError("At least one interest is required.")

    # -------------------------
    # Destination Validation
    # -------------------------
    destination = state["destination"].strip()

    destination_exists = False

    # User did not provide a destination.
    if destination:

        response = search_tool.invoke(
            {
                "query": f"{destination} tourist destination"
            }
        )

        results = response.get("results", [])

        destination_lower = destination.lower()

        for result in results:

            title = result.get("title", "").lower()
            content = result.get("content", "").lower()

            if (
                destination_lower in title
                or destination_lower in content
            ):
                destination_exists = True
                break

    print("input validation done")
    return {
        "interests": interests,
        "destination_exists": destination_exists,
    }