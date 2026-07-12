from copy import deepcopy


DEFAULT_WORKFLOW = {
    "Input Validation": "pending",
    "Destination Search": "pending",
    "Human Selection": "pending",
    "Weather": "pending",
    "Tourist Spots": "pending",
    "Geocoding": "pending",
    "Distance Matrix": "pending",
    "Packing Planner": "pending",
    "Budget Planner": "pending",
    "Itinerary Planner": "pending",
    "Human Approval": "pending",
    "Final Report": "pending",
}


_workflow = deepcopy(DEFAULT_WORKFLOW)


def reset_workflow():
    """
    Reset the workflow before a new graph execution.
    """
    global _workflow
    _workflow = deepcopy(DEFAULT_WORKFLOW)


def start_agent(agent_name: str):
    """
    Mark an agent as currently running.
    """
    _workflow[agent_name] = "running"


def set_status(agent_name: str, status: str):
    """
    Explicitly set the status of an agent (e.g. "waiting" during an
    interrupt that is awaiting human input).
    """
    if agent_name in _workflow:
        _workflow[agent_name] = status


def complete_agent(agent_name: str):
    """
    Mark an agent as completed.
    """
    _workflow[agent_name] = "completed"


def get_workflow():
    """
    Return the current workflow status.
    """
    return _workflow