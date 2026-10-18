# Design Document

## Overview

The String Sort Visualizer is a single-page Streamlit web application that lets users compare three classic sorting algorithms — Bubble Sort, Selection Sort, and Quick Sort — applied to a user-supplied collection of strings. Users provide input either by typing strings manually (one per line) or by selecting entries from a predefined word list. Clicking the Sort button triggers all three algorithms simultaneously in the Python backend. The application then displays each algorithm's sorted output, step count, and accuracy verdict side by side, together with a summary comparison table.

The application is intentionally simple: one Python file per concern (algorithms, UI, state management), no database, no authentication, no background workers. All computation is synchronous and in-memory.

## Architecture

The application follows a three-layer architecture within a single Python process:

```mermaid
flowchart TD
    subgraph UI["UI Layer (app.py — Streamlit)"]
        INPUT["Input Panel\n(text_area + multiselect)"]
        BUTTON["Sort Button"]
        RESULTS["Results Panel\n(3 columns + summary table)"]
    end

    subgraph LOGIC["Logic Layer"]
        PARSER["Input Parser\n(parse_input)"]
        RUNNER["Sort Runner\n(run_all_sorts)"]
        CHECKER["Accuracy Checker\n(check_accuracy)"]
    end

    subgraph ALGORITHMS["Algorithm Layer"]
        BUBBLE["bubble_sort(strings) → (result, steps)"]
        SELECTION["selection_sort(strings) → (result, steps)"]
        QUICKSORT["quick_sort(strings) → (result, steps)"]
    end

    INPUT -->|raw text / selected items| PARSER
    BUTTON -->|click triggers| RUNNER
    PARSER -->|List[str]| RUNNER
    RUNNER --> BUBBLE
    RUNNER --> SELECTION
    RUNNER --> QUICKSORT
    BUBBLE -->|SortResult| CHECKER
    SELECTION -->|SortResult| CHECKER
    QUICKSORT -->|SortResult| CHECKER
    CHECKER -->|SortOutcome| RESULTS
```

**Key architectural decisions:**

- **No concurrency**: All three sorts run sequentially in the Streamlit request cycle. For up to 1,000 strings the combined runtime is well under 5 seconds (Req 3.3); concurrency would add complexity for no practical gain at this scale.
- **Stateless algorithm functions**: Each sorting function is a pure function — no global state — making them straightforward to test with property-based testing.
- **Streamlit session state** (`st.session_state`) stores the last manual-entry text so it can be restored when the user deselects all predefined-list items (Req 2.4).

## Components and Interfaces

### Module: `algorithms.py`

Contains the three pure sorting functions and their shared types.

```python
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class SortResult:
    sorted_list: List[str]   # sorted output
    step_count: int          # number of pairwise comparisons performed

def bubble_sort(strings: List[str]) -> SortResult: ...
def selection_sort(strings: List[str]) -> SortResult: ...
def quick_sort(strings: List[str]) -> SortResult: ...
```

**Sort-order contracts:**

| Algorithm      | Primary order                              | Notes                                  |
|----------------|--------------------------------------------|----------------------------------------|
| Bubble Sort    | Case-sensitive ascending (ASCII/Unicode)   | Uppercase precedes lowercase (Req 4.1) |
| Selection Sort | Case-sensitive ascending (ASCII/Unicode)   | Consistent with Bubble Sort (Req 5.1)  |
| Quick Sort     | Case-insensitive ascending, case-sensitive tie-break | `key=lambda s: (s.casefold(), s)` (Req 6.1) |

**Step counting contract** (shared by all three):
- Increment `step_count` by 1 for every pairwise string comparison, including comparisons that do not result in a swap (Req 4.2, 5.2, 6.2).
- Single-element and empty inputs produce `step_count = 0` (Req 4.4, 4.5, 5.4, 5.5, 6.4, 6.5).

---

### Module: `logic.py`

Thin orchestration layer — parses raw input, drives the three sorts, and performs the accuracy check.

```python
from dataclasses import dataclass
from typing import List, Optional
from algorithms import SortResult

@dataclass(frozen=True)
class SortOutcome:
    algorithm: str         # "Bubble Sort" | "Selection Sort" | "Quick Sort"
    result: SortResult
    is_accurate: bool      # True if result.sorted_list == reference_sorted

def parse_input(raw: str) -> List[str]:
    """
    Split raw text by newline, strip whitespace from each line,
    discard empty lines. Returns at most 1,000 items, each at most
    500 characters (excess silently truncated per Req 1.5).
    """
    ...

def run_all_sorts(strings: List[str]) -> List[SortOutcome]:
    """
    Execute bubble_sort, selection_sort, quick_sort on `strings`.
    Compute accuracy for each. Return list of three SortOutcome values
    in the order [Bubble, Selection, Quick].
    """
    ...

def _reference_sorted(strings: List[str], algorithm: str) -> List[str]:
    """
    Returns the expected correct sort for the given algorithm.
    Used by accuracy check (Req 7.1, 7.4).
    - Bubble / Selection: sorted(strings)
    - Quick: sorted(strings, key=lambda s: (s.casefold(), s))
    """
    ...
```

**Accuracy check logic (Req 7.1, 7.4):** For each algorithm, compare `result.sorted_list` against `_reference_sorted(strings, algorithm)`. Each algorithm has its own expected sort order, so the reference is algorithm-specific rather than a single global `sorted()` call.

---

### Module: `app.py` (Streamlit entry point)

Handles all UI rendering and session-state management. No business logic lives here.

```
Session state keys:
  "manual_text"          str   — last text entered in the manual text area
  "predefined_selected"  list  — currently selected items from the word list
  "sort_outcomes"        list  — List[SortOutcome] from the most recent sort, or None
  "sort_running"         bool  — True while sorts are executing (disables Sort button)
```

**Render flow** (each Streamlit rerun):

1. Render input panel (text area + multiselect).
2. Determine active `String_Input`:
   - If `predefined_selected` is non-empty → use those strings.
   - Else → parse `manual_text`.
3. Render Sort button (disabled when `sort_running` is True).
4. On Sort button click:
   a. Validate: if active input is empty → show validation message, stop.
   b. Set `sort_running = True`, rerun.
   c. Call `run_all_sorts(active_input)`.
   d. Store results in `sort_outcomes`.
   e. Set `sort_running = False`, rerun.
5. Render results panel if `sort_outcomes` is not None.

---

### Module: `word_list.py`

Provides the predefined word list constant.

```python
PREDEFINED_WORDS: List[str] = [...]  # ≥ 20 words, 1–20 chars each,
                                     # lowercase, uppercase, digits, mixed (Req 2.3)
```

## Data Models

### `SortResult` (immutable dataclass)

| Field         | Type       | Description                                        |
|---------------|------------|----------------------------------------------------|
| `sorted_list` | `List[str]`| Output strings in sorted order                     |
| `step_count`  | `int`      | Non-negative count of pairwise comparisons made    |

Invariant: `step_count >= 0` always. `step_count == 0` iff input length ≤ 1.

---

### `SortOutcome` (immutable dataclass)

| Field         | Type       | Description                                        |
|---------------|------------|----------------------------------------------------|
| `algorithm`   | `str`      | Algorithm name label                               |
| `result`      | `SortResult` | The algorithm's output                           |
| `is_accurate` | `bool`     | Whether output matches expected reference sort     |

---

### Session State Schema

| Key                  | Type              | Initial value | Purpose                                         |
|----------------------|-------------------|---------------|-------------------------------------------------|
| `manual_text`        | `str`             | `""`          | Persists manual entry across reruns             |
| `predefined_selected`| `List[str]`       | `[]`          | Persists multiselect state across reruns        |
| `sort_outcomes`      | `List[SortOutcome] \| None` | `None` | Holds last sort results for display        |
| `sort_running`       | `bool`            | `False`       | Controls Sort button disabled state             |

---

### Input Constraints

| Constraint                   | Value  | Requirement |
|------------------------------|--------|-------------|
| Max strings per input        | 1,000  | Req 1.5     |
| Max characters per string    | 500    | Req 1.5     |
| Max predefined list selection| 50     | Req 2.5     |
| Min predefined word list size| 20     | Req 2.3     |
| Min predefined word length   | 1 char | Req 2.3     |
| Max predefined word length   | 20 chars | Req 2.3   |


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system — essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Input parsing strips surrounding whitespace

*For any* string containing non-whitespace characters surrounded by arbitrary leading/trailing whitespace, `parse_input` shall return that string with whitespace trimmed, preserving the core content unchanged.

**Validates: Requirements 1.4**

---

### Property 2: All-whitespace input produces empty parse result

*For any* text composed entirely of whitespace characters (spaces, tabs, newlines, or combinations thereof), `parse_input` shall return an empty list.

**Validates: Requirements 1.2**

---

### Property 3: Duplicate strings are preserved through parsing

*For any* raw text input containing duplicate non-empty lines, `parse_input` shall include all occurrences of each duplicate string in the output, without deduplication.

**Validates: Requirements 1.3**

---

### Property 4: Predefined selection round-trip restores manual text

*For any* manually entered text string, setting a non-empty predefined selection replaces the active input with the selection, and subsequently clearing that selection to empty restores the active input to the original manual text unchanged.

**Validates: Requirements 2.2, 2.4**

---

### Property 5: Bubble Sort produces correctly ordered output

*For any* list of strings, `bubble_sort` shall return a sorted list equal to `sorted(strings)` — ascending case-sensitive lexicographic order where uppercase letters precede lowercase letters for the same character (Python's default string comparison).

**Validates: Requirements 4.1**

---

### Property 6: Bubble Sort step count is non-negative

*For any* list of strings, `bubble_sort` shall return a `step_count` that is greater than or equal to zero, and equal to zero if and only if the input contains at most one element.

**Validates: Requirements 4.2, 4.4, 4.5**

---

### Property 7: Selection Sort produces correctly ordered output

*For any* list of strings, `selection_sort` shall return a sorted list equal to `sorted(strings)` — ascending case-sensitive lexicographic order — and the output shall contain exactly the same multiset of strings as the input.

**Validates: Requirements 5.1, 5.6**

---

### Property 8: Selection Sort step count equals n*(n-1)/2

*For any* list of n strings, `selection_sort` shall return a `step_count` equal to exactly `n * (n - 1) // 2`, because Selection Sort always performs a fixed number of comparisons regardless of input order.

**Validates: Requirements 5.2, 5.4, 5.5**

---

### Property 9: Quick Sort produces correctly ordered output

*For any* list of strings, `quick_sort` shall return a sorted list equal to `sorted(strings, key=lambda s: (s.casefold(), s))` — ascending case-insensitive lexicographic order with case-sensitive tie-breaking for strings that differ only in case.

**Validates: Requirements 6.1**

---

### Property 10: Quick Sort step count does not exceed n*(n-1)/2

*For any* list of n strings, `quick_sort` shall return a `step_count` in the range `[0, n*(n-1)//2]` inclusive, ensuring the algorithm never performs more comparisons than the worst-case quadratic upper bound.

**Validates: Requirements 6.2, 6.3, 6.4, 6.5**

---

## Error Handling

### Input Validation Errors

| Condition | Handling | Requirement |
|-----------|----------|-------------|
| Empty input (no non-whitespace lines) | Display validation message; do not execute any sort | Req 1.2, 3.4 |
| Input exceeds 1,000 strings | Silently truncate to first 1,000 strings after parsing | Req 1.5 |
| Individual string exceeds 500 characters | Silently truncate that string to 500 characters | Req 1.5 |

No exceptions are raised for input validation failures. The UI handles them with user-visible messages or silent truncation as specified.

### Algorithm Errors

The sorting functions are pure Python operating on in-memory lists. No I/O, no external calls. The only realistic failure mode is an unexpected exception from a programming error. `run_all_sorts` wraps each algorithm call in a try/except; if an algorithm raises, `SortOutcome.is_accurate` is set to `False` and an error indicator is shown in the results panel (aligns with Req 7.3 behavior).

### Streamlit State Errors

If `st.session_state` is missing an expected key (e.g., on first load), all keys are initialised to their default values at the top of `app.py`'s render function using `session_state.setdefault(...)`. This prevents `KeyError` on first run.

## Testing Strategy

### Unit Tests (`tests/test_algorithms.py`, `tests/test_logic.py`)

Unit tests cover specific examples, edge cases, and error conditions that complement the property tests:

- **Algorithms**:
  - Empty list → `([], 0)` for all three algorithms.
  - Single element → input unchanged, `step_count == 0`.
  - Already-sorted input → output unchanged for Bubble and Selection Sort.
  - Reverse-sorted input → correct output for all three.
  - Inputs with mixed case → verify Quick Sort's case-insensitive tie-breaking (e.g., `["banana", "Apple", "cherry"]` → `["Apple", "banana", "cherry"]`).
  - Bubble Sort and Selection Sort with identical inputs produce the same sorted output (consistent sort order).
  - Selection Sort step count formula: `n*(n-1)//2` for small known inputs.

- **Logic / Input parsing**:
  - Empty string → empty list.
  - Whitespace-only string → empty list.
  - String with blank lines mixed in → blank lines discarded.
  - Duplicates preserved.
  - Strings truncated at 500 characters; list truncated at 1,000 items.
  - `check_accuracy`: correct sort → `True`; intentionally wrong sort → `False`.

- **Accuracy check**:
  - Correct output for each algorithm → `is_accurate == True`.
  - Subtly wrong output (one element out of place) → `is_accurate == False`.

### Property-Based Tests (`tests/test_properties.py`)

Uses the **`hypothesis`** library. Each property test runs a minimum of **100 iterations** per test (Hypothesis default; set `max_examples=100` explicitly for reproducibility).

Each test is tagged with a comment referencing the design property it validates:
`# Feature: string-sort-visualizer, Property N: <property_text>`

| Test function | Design property | Hypothesis strategy |
|---|---|---|
| `test_parse_strips_whitespace` | Property 1 | `st.text()` with surrounding whitespace added |
| `test_parse_rejects_all_whitespace` | Property 2 | `st.text(alphabet=st.sampled_from(" \t\n\r"))` |
| `test_parse_preserves_duplicates` | Property 3 | `st.lists(st.text())` with intentional duplicates |
| `test_predefined_selection_round_trip` | Property 4 | `st.text()`, `st.lists(st.sampled_from(PREDEFINED_WORDS), min_size=1)` |
| `test_bubble_sort_correctness` | Property 5 | `st.lists(st.text())` |
| `test_bubble_sort_step_count_nonnegative` | Property 6 | `st.lists(st.text())` |
| `test_selection_sort_correctness` | Property 7 | `st.lists(st.text())` |
| `test_selection_sort_step_count_formula` | Property 8 | `st.lists(st.text())` |
| `test_quick_sort_correctness` | Property 9 | `st.lists(st.text())` |
| `test_quick_sort_step_count_upper_bound` | Property 10 | `st.lists(st.text())` |

**Notes:**
- `st.text()` generates arbitrary Unicode strings, covering edge cases such as empty strings, whitespace-only strings, mixed case, digits, and special characters automatically.
- `st.lists(st.text(), max_size=100)` is used to keep individual test runs fast; the key properties hold for any size.
- Property tests do NOT test Streamlit UI rendering — those are covered by example-based integration tests using Streamlit's `AppTest` utility.

### Integration / Smoke Tests (`tests/test_app.py`)

Uses Streamlit's built-in `AppTest` framework for lightweight UI-level smoke tests:

- Sort button is present and initially enabled.
- Submitting empty input shows validation message without executing sorts.
- Submitting a valid list of strings renders three result sections with algorithm names.
- `sort_running = True` disables the Sort button.
- Predefined word list widget renders with expected options.
- Results panel is empty before first sort.
- Accuracy indicators appear after a successful sort.

### Performance Test

Time `run_all_sorts` on a 1,000-string input; assert elapsed time < 5 seconds (Req 3.3). Run as a separate pytest mark (`@pytest.mark.perf`) so it can be excluded from the normal test suite.
