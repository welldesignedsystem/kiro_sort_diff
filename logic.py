"""
logic.py — Orchestration layer: input parsing, sort dispatch, accuracy checking.

No UI logic lives here. All functions are pure / side-effect-free with respect
to application state; Streamlit session state is managed exclusively in app.py.
"""

from dataclasses import dataclass
from typing import List, Optional

from algorithms import SortResult

_MAX_STRINGS = 1_000
_MAX_STRING_LEN = 500


@dataclass(frozen=True)
class SortOutcome:
    """Immutable result of running one algorithm and checking its accuracy."""

    algorithm: str       # "Bubble Sort" | "Selection Sort" | "Quick Sort"
    result: SortResult
    is_accurate: bool    # True if result.sorted_list == reference sorted output


def parse_input(raw: str) -> List[str]:
    """
    Split raw text by newline, strip whitespace from each line, and discard
    lines that are empty after stripping.

    Silently truncates each string to at most 500 characters (Req 1.5) and
    truncates the resulting list to at most 1,000 items (Req 1.5).

    Duplicates are preserved as-is (Req 1.3).
    """
    lines = []
    for line in raw.split("\n"):
        stripped = line.strip()
        if stripped:
            lines.append(stripped[:_MAX_STRING_LEN])
    return lines[:_MAX_STRINGS]


def _reference_sorted(strings: List[str], algorithm: str) -> List[str]:
    """
    Returns the expected correct sort order for the given algorithm.
    Used by the accuracy check (Req 7.1, 7.4).

    All algorithms use ascending ASCII/Unicode order (Python default sorted()).
    """
    return sorted(strings)


def run_all_sorts(strings: List[str]) -> List["SortOutcome"]:
    """
    Run all three sorting algorithms against *strings* and return a list of
    four SortOutcome values in the order [Bubble Sort, Selection Sort, Quick Sort, Merge Sort].

    Each algorithm is wrapped in try/except so a failure in one does not
    prevent the others from running.  On exception, is_accurate is set to False
    and the Sort_Result contains an empty list with step_count 0.

    Requirements: 3.2, 7.1, 7.2, 7.3, 7.4
    """
    from algorithms import bubble_sort, selection_sort, quick_sort, merge_sort

    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Selection Sort", selection_sort),
        ("Quick Sort", quick_sort),
        ("Merge Sort", merge_sort),
    ]

    outcomes: List[SortOutcome] = []
    for name, fn in algorithms:
        try:
            result: SortResult = fn(strings)
            reference = _reference_sorted(strings, name)
            is_accurate = result.sorted_list == reference
        except Exception:
            result = SortResult(sorted_list=[], step_count=0)
            is_accurate = False
        outcomes.append(SortOutcome(algorithm=name, result=result, is_accurate=is_accurate))

    return outcomes
