from state import TravelState
from llm import llm


def budget_planner_node(state: TravelState) -> TravelState:
    """
    Generate a budget allocation for the trip.
    """
    print("budger planner started")

    prompt = f"""
You are an expert travel budget planner.

Destination:
{state["destination"]}

Total Budget:
₹{state["budget"]}

Trip Duration:
{state["days"]} days

User Interests:
{", ".join(state["interests"])}

Create a practical budget allocation.

Distribute the budget among:
- Accommodation
- Food
- Transport
- Activities
- Emergency

Keep the total within the user's budget.

Return only the budget plan in a clear format.
"""

    response = llm.invoke(prompt)
    print("budget planner ended")

    return {
        "budget_plan": response.content.strip()

    }