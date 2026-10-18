"""
app.py — Streamlit entry point and UI rendering.

All business logic is delegated to logic.py; all algorithm implementations
live in algorithms.py. This module handles only UI rendering and session state.
"""

import streamlit as st

from logic import parse_input, run_all_sorts
from word_list import PREDEFINED_WORDS


def main() -> None:
    """Main render function called on every Streamlit rerun."""

    st.title("String Sort Visualizer")

    # --- Session state initialisation (Req 3.5, 8.6) ---
    st.session_state.setdefault("manual_text", "")
    st.session_state.setdefault("predefined_selected", [])
    st.session_state.setdefault("sort_outcomes", None)
    st.session_state.setdefault("sort_running", False)

    # ------------------------------------------------------------------ #
    # INPUT PANEL (Tasks 7.2)                                             #
    # ------------------------------------------------------------------ #
    st.subheader("Input")

    # Predefined word list selector (Req 2.1, 2.2, 2.4, 2.5)
    predefined_selected = st.multiselect(
        "Pick from predefined words (optional):",
        options=PREDEFINED_WORDS,
        default=st.session_state["predefined_selected"],
        max_selections=50,
        key="predefined_widget",
    )
    st.session_state["predefined_selected"] = predefined_selected

    # Manual text area (Req 1.1)
    # When predefined selection is active it takes precedence; the text area
    # still shows manual_text so the user can restore it by clearing selection.
    manual_text = st.text_area(
        "Or enter strings manually (one per line):",
        value=st.session_state["manual_text"],
        height=180,
        key="manual_widget",
        disabled=bool(predefined_selected),
        placeholder="apple\nbanana\nCherry\n42",
    )
    # Only persist manual text when predefined selector is empty (Req 2.4)
    if not predefined_selected:
        st.session_state["manual_text"] = manual_text

    # Determine active input
    if predefined_selected:
        active_raw = "\n".join(predefined_selected)
    else:
        active_raw = st.session_state["manual_text"]

    # ------------------------------------------------------------------ #
    # SORT BUTTON & EXECUTION (Task 7.4)                                  #
    # ------------------------------------------------------------------ #
    sort_clicked = st.button(
        "Sort",
        disabled=st.session_state["sort_running"],
        type="primary",
    )

    if sort_clicked:
        strings = parse_input(active_raw)
        if not strings:
            # Req 1.2 / 3.4 — validation message, no sort executed
            st.warning("Please enter at least one non-empty string before sorting.")
        else:
            st.session_state["sort_running"] = True
            st.session_state["sort_outcomes"] = run_all_sorts(strings)
            st.session_state["sort_running"] = False

    # ------------------------------------------------------------------ #
    # RESULTS PANEL (Task 7.5)                                            #
    # ------------------------------------------------------------------ #
    outcomes = st.session_state["sort_outcomes"]

    if outcomes is None:
        # Req 8.6 — empty state before first sort
        st.info("Results will appear here after you click Sort.")
        return

    st.subheader("Results")

    # Three side-by-side columns, one per algorithm (Req 8.2)
    cols = st.columns(4)
    for col, outcome in zip(cols, outcomes):
        with col:
            # Accuracy indicator (Req 7.2 / 7.3)
            if outcome.is_accurate:
                st.success(f"✅ {outcome.algorithm}")
            else:
                st.error(f"❌ {outcome.algorithm}")

            # Step count with descriptive label (Req 8.3)
            st.metric("Comparisons", outcome.result.step_count)

            # Sorted list (Req 8.4)
            st.write("**Sorted output:**")
            for i, word in enumerate(outcome.result.sorted_list, 1):
                st.write(f"{i}. {word}")

    # Summary table (Req 8.5)
    st.subheader("Summary")
    summary_data = {
        "Algorithm": [o.algorithm for o in outcomes],
        "Comparisons": [o.result.step_count for o in outcomes],
        "Accurate": ["✅ Yes" if o.is_accurate else "❌ No" for o in outcomes],
    }
    st.table(summary_data)


if __name__ == "__main__":
    st.set_page_config(page_title="String Sort Visualizer", layout="wide")
    main()
