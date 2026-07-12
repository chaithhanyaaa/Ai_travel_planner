import threading
import time

import streamlit as st
from langchain_core.callbacks import BaseCallbackHandler
from langgraph.types import Command

from graph import graph
from utils import run_state
from utils.workflow_tracker import (
    get_workflow,
    reset_workflow,
    set_status,
    start_agent,
    complete_agent,
)

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🌍",
    layout="wide",
)

# -----------------------------
# Node name -> Workflow display name
# -----------------------------

NODE_DISPLAY = {
    "input_validation": "Input Validation",
    "destination_search": "Destination Search",
    "human_selection": "Human Selection",
    "weather": "Weather",
    "tourist_spots": "Tourist Spots",
    "geocoding": "Geocoding",
    "distance_matrix": "Distance Matrix",
    "packing": "Packing Planner",
    "budget": "Budget Planner",
    "itinerary": "Itinerary Planner",
    "human_approval": "Human Approval",
    "final_report": "Final Report",
}


class WorkflowCallback(BaseCallbackHandler):
    """Marks workflow steps running / completed as graph nodes execute.

    LangGraph only puts ``langgraph_node`` in the *start* metadata, so we
    remember the active node per run_id and resolve it on chain end.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._active = {}

    def on_chain_start(
        self,
        serialized,
        inputs,
        *,
        run_id=None,
        parent_run_id=None,
        tags=None,
        metadata=None,
        run_type=None,
        **kwargs,
    ):
        name = (metadata or {}).get("langgraph_node")
        if name in NODE_DISPLAY:
            self._active[run_id] = name
            start_agent(NODE_DISPLAY[name])

    def on_chain_end(
        self,
        outputs,
        *,
        run_id=None,
        parent_run_id=None,
        tags=None,
        metadata=None,
        **kwargs,
    ):
        name = self._active.pop(run_id, None)
        if name in NODE_DISPLAY:
            complete_agent(NODE_DISPLAY[name])


# -----------------------------
# Cross-thread handoff lives in utils/run_state.py.
# Its module-level globals survive Streamlit reruns (imported modules
# are cached) and are shared with the background thread - unlike this
# script's own top-level variables, which are re-initialized every
# rerun and would clobber the thread's updates.
# -----------------------------

for key, default in {
    "thread_id": "travel-planner",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def _runner(payload, thread_id):
    """Run (or resume) the graph in a background thread."""
    cfg = {
        "configurable": {"thread_id": thread_id},
        "callbacks": [WorkflowCallback()],
    }
    try:
        result = graph.invoke(payload, config=cfg)
    except Exception as e:  # keep pipeline alive on node/network errors
        run_state.run_status = "error"
        run_state.run_error = f"{type(e).__name__}: {e}"
        return

    run_state.run_result = result
    if "__interrupt__" in result:
        run_state.run_status = "interrupted"
        run_state.run_interrupt = result["__interrupt__"][0].value
    else:
        run_state.run_status = "done"


def launch(payload, reset=False):
    if reset:
        reset_workflow()
    run_state.run_status = "running"
    run_state.run_result = None
    run_state.run_interrupt = None
    run_state.run_error = None
    threading.Thread(
        target=_runner,
        args=(payload, st.session_state.thread_id),
        daemon=True,
    ).start()


def render_workflow():
    workflow = get_workflow()
    st.subheader("Workflow")
    for name, status in workflow.items():
        icon = {
            "pending": "⏳",
            "running": "🔄",
            "completed": "✅",
            "waiting": "👤",
        }.get(status, "⏳")
        st.markdown(f"{icon} **{name}** &nbsp;—&nbsp; `{status}`")


# -----------------------------
# UI: Inputs
# -----------------------------

st.title("🌍 AI Travel Planner")

with st.sidebar:
    st.header("Trip Details")

    if run_state.run_status == "idle":
        destination = st.text_input("Destination (Optional)")
        budget = st.number_input("Budget (₹)", min_value=1.0, step=1000.0)
        days = st.number_input("Days", min_value=1, step=1)
        interests = st.text_input("Interests (comma separated)")

        if st.button("Generate Travel Plan", use_container_width=True):
            initial_state = {
                "destination": destination.strip(),
                "budget": float(budget),
                "days": int(days),
                "interests": [i.strip() for i in interests.split(",") if i.strip()],
                "destination_exists": False,
                "suggested_destinations": [],
                "user_feedback": None,
                "user_feedback_2": None,
                "weather_report": "",
                "tourist_spots": [],
                "geocoded_spots": [],
                "distance_matrix": [],
                "packing_list": [],
                "budget_plan": "",
                "itinerary": "",
                "final_report": "",
            }
            launch(initial_state, reset=True)
    else:
        st.info("Trip is being planned. Use **Reset** to start a new one.")

    if st.button("Reset", use_container_width=True):
        run_state.run_status = "idle"
        run_state.run_result = None
        run_state.run_interrupt = None
        run_state.run_error = None
        reset_workflow()
        st.rerun()

# -----------------------------
# Poll while the background run is in progress.
# Re-runs the whole app every 0.5s so the workflow + output stay live.
# -----------------------------

status = run_state.run_status

# -----------------------------
# Layout: Output (left) + Workflow (right).
# The Workflow panel is rendered FIRST and ALWAYS, so it stays visible
# during the running phase too. st.stop() after the running poll
# guarantees we never fall through and double-render.
# -----------------------------

col_out, col_wf = st.columns([2, 1])

with col_wf:
    render_workflow()

if status == "running":
    with col_out:
        st.info("Planning your trip... (see the Workflow panel for live progress)")
    time.sleep(0.3)
    st.rerun()
    st.stop()

with col_out:
    st.subheader("Output")

    if status == "idle":
        st.info("Enter your trip details and click **Generate Travel Plan**.")

    elif status == "error":
        st.error("The graph stopped with an error:")
        st.code(run_state.run_error)

    elif status == "interrupted":
        data = run_state.run_interrupt
        step_type = data.get("type")

        # Highlight the step that is currently awaiting human input.
        waiting_step = {
            "destination_selection": "Human Selection",
            "human_approval": "Human Approval",
        }.get(step_type)
        if waiting_step:
            set_status(waiting_step, "waiting")

        if step_type == "destination_selection":
            st.subheader("Choose a Destination")
            st.markdown("Pick a suggested destination, or ask for new ones.")

            options = list(data["suggested_destinations"]) + [
                "🔄 Suggest new destinations"
            ]
            choice = st.radio(
                "Suggested Destinations", options, index=0, key="dest_choice"
            )
            feedback = st.text_input(
                "Extra preferences (optional, used when requesting new suggestions)",
                key="dest_feedback",
            )

            def _continue():
                sel = st.session_state.dest_choice
                interrupt_data = run_state.run_interrupt
                if sel == "🔄 Suggest new destinations":
                    payload = Command(
                        resume={"choice": 0, "feedback": st.session_state.dest_feedback}
                    )
                else:
                    idx = interrupt_data["suggested_destinations"].index(sel)
                    payload = Command(resume={"choice": idx + 1, "feedback": ""})
                launch(payload, reset=False)

            st.button("Continue", on_click=_continue, use_container_width=True)

        elif step_type == "human_approval":
            st.subheader("Review Itinerary")
            st.markdown(data.get("itinerary", ""))

            decision = st.radio(
                "Do you approve this itinerary?",
                ["Approve", "Regenerate"],
                index=0,
                key="appr_decision",
            )
            feedback = st.text_input(
                "Feedback for regeneration (optional)", key="appr_feedback"
            )

            def _submit():
                approved = st.session_state.appr_decision == "Approve"
                payload = Command(
                    resume={
                        "approved": approved,
                        "feedback": st.session_state.appr_feedback,
                    }
                )
                launch(payload, reset=False)

            st.button("Submit", on_click=_submit, use_container_width=True)

        else:
            st.warning("Unknown interrupt received.")

    elif status == "done":
        result = run_state.run_result
        if result and "final_report" in result:
            st.markdown(result["final_report"])
        else:
            st.warning("Graph finished without a final report.")
