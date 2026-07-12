from langgraph.graph import StateGraph, START, END

from state import TravelState
from langgraph.checkpoint.memory import MemorySaver
from nodes.input_validation import input_validation_node
from nodes.destination_search import destination_search_node
from nodes.human_selection import human_selection_node
from nodes.weather import weather_node
from nodes.tourist_spots import tourist_spots_node
from nodes.geocoding import geocoding_node
from nodes.distance_matrix import distance_matrix_node
from nodes.packing_planner import packing_planner_node
from nodes.budget_planner import budget_planner_node
from nodes.itinerary_planner import itinerary_planner_node
from nodes.human_approval import human_approval_node
from nodes.final_report import final_report_node


builder = StateGraph(TravelState)


# -----------------------------
# Nodes
# -----------------------------

builder.add_node("input_validation", input_validation_node)
builder.add_node("destination_search", destination_search_node)
builder.add_node("human_selection", human_selection_node)
builder.add_node("weather", weather_node)

builder.add_node("tourist_spots", tourist_spots_node)
builder.add_node("geocoding", geocoding_node)
builder.add_node("distance_matrix", distance_matrix_node)

builder.add_node("packing", packing_planner_node)
builder.add_node("budget", budget_planner_node)

builder.add_node("itinerary", itinerary_planner_node)

builder.add_node("human_approval", human_approval_node)

builder.add_node("final_report", final_report_node)


# -----------------------------
# Routing Functions
# -----------------------------

def destination_router(state: TravelState):

    if state["destination_exists"]:
        return "weather"

    return "destination_search"


def approval_router(state: TravelState):

    if state["user_feedback_2"] is None:
        return "final_report"

    return "itinerary"

def first_approval(state:TravelState):
    if state["user_feedback"]:
        return "destination_search"
    return "weather"


# -----------------------------
# Start
# -----------------------------

builder.add_edge(START, "input_validation")


# -----------------------------
# Destination Routing
# -----------------------------

builder.add_conditional_edges(
    "input_validation",
    destination_router,
    {
        "weather": "weather",
        "destination_search": "destination_search",
    },
)

builder.add_edge(
    "destination_search",
    "human_selection",
)


builder.add_conditional_edges(
    "human_selection",
    first_approval,
    {
        "destination_search": "destination_search",
        "weather": "weather",
    }
)


# -----------------------------
# Parallel Execution
# -----------------------------

builder.add_edge(
    "weather",
    "tourist_spots",
)

builder.add_edge(
    "weather",
    "packing",
)

builder.add_edge(
    "weather",
    "budget",
)


# Tourist branch

builder.add_edge(
    "tourist_spots",
    "geocoding",
)

builder.add_edge(
    "geocoding",
    "distance_matrix",
)


# Merge

builder.add_edge(
    "distance_matrix",
    "itinerary",
)





# -----------------------------
# Human Approval
# -----------------------------

builder.add_edge(
    "itinerary",
    "human_approval",
)

builder.add_conditional_edges(
    "human_approval",
    approval_router,
    {
        "final_report": "final_report",
        "itinerary": "itinerary",
    },
)


# -----------------------------
# End
# -----------------------------

builder.add_edge(
    "final_report",
    END,
)

memory = MemorySaver()
graph = builder.compile(
    checkpointer=memory
)