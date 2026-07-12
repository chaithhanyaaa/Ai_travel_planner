# Cross-rerun / cross-thread run state for the Streamlit app.
#
# Imported modules are cached by Python (sys.modules), so their
# module-level globals survive Streamlit script reruns AND are shared
# with background threads. Do NOT re-initialize these elsewhere - just
# mutate the attributes below.

run_status = "idle"          # idle | running | interrupted | done | error
run_result = None
run_interrupt = None
run_error = None
