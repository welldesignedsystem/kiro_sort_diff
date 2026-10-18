# Implementation Plan: String Sort Visualizer

## Overview

Implement a single-page Streamlit web application that sorts user-supplied strings using Bubble Sort, Selection Sort, and Quick Sort. The implementation follows the three-layer architecture defined in the design: `algorithms.py` (pure sort functions), `logic.py` (orchestration and input parsing), `app.py` (Streamlit UI), and `word_list.py` (predefined word list). Property-based tests use `hypothesis` with `max_examples=100` and cover all 10 correctness properties from the design.

## Tasks

- [x] 1. Set up project structure and shared data models
  - Create the top-level directory layout: `algorithms.py`, `logic.py`, `app.py`, `word_list.py`, and a `tests/` package with `__init__.py`
  - Define the `SortResult` frozen dataclass (`sorted_list: List[str]`, `step_count: int`) in `algorithms.py`
  - Define the `SortOutcome` frozen dataclass (`algorithm: str`, `result: SortResult`, `is_accurate: bool`) in `logic.py`
  - Add `requirements.txt` with pinned versions for `streamlit`, `hypothesis`, and `pytest`
  - _Requirements: 4.1, 5.1, 6.1, 7.1, 8.1_

- [x] 2. Implement the predefined word list
  - [x] 2.1 Create `word_list.py` with the `PREDEFINED_WORDS` constant
    - Include at least 20 strings covering lowercase-only, uppercase-only, digit-only, and mixed-character combinations, each between 1 and 20 characters long
    - _Requirements: 2.3_

- [x] 3. Implement sorting algorithms
  - [x] 3.1 Implement `bubble_sort(strings: List[str]) -> SortResult` in `algorithms.py`
    - Sort using case-sensitive ascending lexicographic order (Python default comparison, so uppercase precedes lowercase)
    - Increment `step_count` by 1 for every pairwise comparison, including comparisons that do not result in a swap
    - Return `step_count = 0` for empty or single-element input
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [ ]* 3.2 Write property tests for `bubble_sort` in `tests/test_properties.py`
    - **Property 5: Bubble Sort produces correctly ordered output** — use `st.lists(st.text())`, assert `result.sorted_list == sorted(strings)`
    - **Validates: Requirements 4.1**
    - **Property 6: Bubble Sort step count is non-negative** — use `st.lists(st.text())`, assert `result.step_count >= 0` and `result.step_count == 0` iff `len(strings) <= 1`
    - **Validates: Requirements 4.2, 4.4, 4.5**
    - Set `max_examples=100`; annotate with `# Feature: string-sort-visualizer, Property 5` and `# Feature: string-sort-visualizer, Property 6`

  - [x] 3.3 Implement `selection_sort(strings: List[str]) -> SortResult` in `algorithms.py`
    - Sort using case-sensitive ascending lexicographic order; preserve all duplicates in the output
    - Increment `step_count` by exactly 1 per pairwise comparison; for n inputs the total must equal `n * (n - 1) // 2`
    - Return `step_count = 0` for empty or single-element input
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

  - [ ]* 3.4 Write property tests for `selection_sort` in `tests/test_properties.py`
    - **Property 7: Selection Sort produces correctly ordered output** — use `st.lists(st.text())`, assert `result.sorted_list == sorted(strings)` and output is a permutation of the input
    - **Validates: Requirements 5.1, 5.6**
    - **Property 8: Selection Sort step count equals n*(n-1)/2** — use `st.lists(st.text())`, assert `result.step_count == len(strings) * (len(strings) - 1) // 2`
    - **Validates: Requirements 5.2, 5.4, 5.5**
    - Set `max_examples=100`; annotate with `# Feature: string-sort-visualizer, Property 7` and `# Feature: string-sort-visualizer, Property 8`

  - [x] 3.5 Implement `quick_sort(strings: List[str]) -> SortResult` in `algorithms.py`
    - Sort using case-insensitive ascending order with case-sensitive tie-breaking: `key=lambda s: (s.casefold(), s)`
    - Increment `step_count` by 1 for every pairwise comparison across all partitioning operations, including pivot comparisons
    - Return `step_count = 0` for empty or single-element input
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [ ]* 3.6 Write property tests for `quick_sort` in `tests/test_properties.py`
    - **Property 9: Quick Sort produces correctly ordered output** — use `st.lists(st.text())`, assert `result.sorted_list == sorted(strings, key=lambda s: (s.casefold(), s))`
    - **Validates: Requirements 6.1**
    - **Property 10: Quick Sort step count does not exceed n*(n-1)/2** — use `st.lists(st.text())`, assert `0 <= result.step_count <= len(strings) * (len(strings) - 1) // 2`
    - **Validates: Requirements 6.2, 6.3, 6.4, 6.5**
    - Set `max_examples=100`; annotate with `# Feature: string-sort-visualizer, Property 9` and `# Feature: string-sort-visualizer, Property 10`

  - [ ]* 3.7 Write unit tests for all three sorting algorithms in `tests/test_algorithms.py`
    - Empty list → `SortResult([], 0)` for each algorithm
    - Single-element list → output unchanged, `step_count == 0`
    - Already-sorted and reverse-sorted inputs → correct output for all three
    - Mixed-case Quick Sort: `["banana", "Apple", "cherry"]` → `["Apple", "banana", "cherry"]`
    - Selection Sort step count formula verified for small known inputs (e.g., n=4 → 6, n=5 → 10)
    - Bubble Sort and Selection Sort produce identical output for the same input
    - _Requirements: 4.1–4.5, 5.1–5.6, 6.1–6.5_

- [x] 4. Checkpoint — algorithms complete
  - Ensure all algorithm unit tests and property tests pass; ask the user if questions arise.

- [ ] 5. Implement the logic layer
  - [x] 5.1 Implement `parse_input(raw: str) -> List[str]` in `logic.py`
    - Split by newline, strip whitespace from each line, and discard empty lines
    - Silently truncate each string to 500 characters; silently truncate the list to at most 1,000 items
    - _Requirements: 1.2, 1.3, 1.4, 1.5_

  - [ ]* 5.2 Write property tests for `parse_input` in `tests/test_properties.py`
    - **Property 1: Input parsing strips surrounding whitespace** — use `st.text()` with whitespace prepended/appended, assert the stripped string appears in the result
    - **Validates: Requirements 1.4**
    - **Property 2: All-whitespace input produces empty parse result** — use `st.text(alphabet=st.sampled_from(" \t\n\r"))`, assert result is `[]`
    - **Validates: Requirements 1.2**
    - **Property 3: Duplicate strings are preserved through parsing** — use `st.lists(st.text(min_size=1))` with lines duplicated, assert all occurrences appear in result
    - **Validates: Requirements 1.3**
    - Set `max_examples=100`; annotate with `# Feature: string-sort-visualizer, Property 1`, `Property 2`, `Property 3`

  - [x] 5.3 Implement `_reference_sorted(strings: List[str], algorithm: str) -> List[str]` in `logic.py`
    - Bubble Sort / Selection Sort → `sorted(strings)`
    - Quick Sort → `sorted(strings, key=lambda s: (s.casefold(), s))`
    - _Requirements: 7.1, 7.4_

  - [ ] 5.4 Implement `run_all_sorts(strings: List[str]) -> List[SortOutcome]` in `logic.py`
    - Call `bubble_sort`, `selection_sort`, `quick_sort` in that order
    - Wrap each call in try/except; on exception set `is_accurate = False` and surface an error indicator
    - Compare each result against `_reference_sorted` to determine `is_accurate`
    - Return a list of exactly three `SortOutcome` values in the order `[Bubble, Selection, Quick]`
    - _Requirements: 3.2, 7.1, 7.2, 7.3, 7.4_

  - [ ]* 5.5 Write unit tests for the logic layer in `tests/test_logic.py`
    - `parse_input`: empty string, whitespace-only, blank lines mixed with content, duplicates preserved, per-string 500-char truncation, list 1,000-item truncation
    - `run_all_sorts`: known correct input → all three `is_accurate == True`; subtly incorrect sort (one element out of place) → `is_accurate == False`
    - `_reference_sorted`: Bubble/Selection returns `sorted(strings)`, Quick returns `sorted(strings, key=lambda s: (s.casefold(), s))`
    - _Requirements: 1.2–1.5, 7.1–7.4_

- [ ] 6. Checkpoint — logic layer complete
  - Ensure all logic, parsing, and accuracy tests pass; ask the user if questions arise.

- [ ] 7. Implement the Streamlit UI
  - [ ] 7.1 Create `app.py` with session state initialisation
    - Initialise `manual_text` (`""`), `predefined_selected` (`[]`), `sort_outcomes` (`None`), and `sort_running` (`False`) using `st.session_state.setdefault(...)` at the top of the render function
    - _Requirements: 3.5, 8.6_

  - [ ] 7.2 Implement the input panel in `app.py`
    - Render `st.text_area` bound to `manual_text` session state key (one string per line)
    - Render `st.multiselect` sourced from `PREDEFINED_WORDS`; when selection is non-empty use it as the active input; when selection is cleared, restore `manual_text`
    - _Requirements: 1.1, 2.1, 2.2, 2.4, 2.5_

  - [ ]* 7.3 Write property test for predefined selection round-trip in `tests/test_properties.py`
    - **Property 4: Predefined selection round-trip restores manual text** — use `st.text()` for manual content, `st.lists(st.sampled_from(PREDEFINED_WORDS), min_size=1)` for selection; assert that clearing the selection restores the original manual text
    - **Validates: Requirements 2.2, 2.4**
    - Set `max_examples=100`; annotate with `# Feature: string-sort-visualizer, Property 4`

  - [ ] 7.4 Implement the Sort button and sort execution flow in `app.py`
    - Render Sort button disabled when `sort_running` is `True`
    - On click: if active input is empty show a validation message and stop; otherwise set `sort_running = True`, call `run_all_sorts`, store results in `sort_outcomes`, set `sort_running = False`
    - _Requirements: 1.2, 3.1, 3.2, 3.3, 3.4, 3.5_

  - [ ] 7.5 Implement the results panel in `app.py`
    - Display three side-by-side columns, each labelled with its algorithm name, showing the sorted list and step count with a descriptive label
    - Display a success or error accuracy indicator beside each algorithm's result (Requirements 7.2, 7.3)
    - Display a summary table listing all three algorithm names, their step counts, and accuracy status (Requirement 8.5)
    - Render results area in empty state when `sort_outcomes` is `None` (Requirement 8.6)
    - _Requirements: 7.2, 7.3, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

  - [ ]* 7.6 Write Streamlit AppTest integration tests in `tests/test_app.py`
    - Sort button is present and initially enabled
    - Submitting empty input shows the validation message without executing any sort
    - Submitting a valid list renders three result sections labelled with algorithm names
    - `sort_running = True` in session state disables the Sort button
    - Predefined word list widget renders and contains the expected options
    - Results panel is in empty state before the first sort
    - Accuracy indicators appear after a successful sort
    - _Requirements: 1.2, 2.1, 3.1, 3.4, 3.5, 7.2, 7.3, 8.2, 8.6_

- [ ] 8. Add performance test
  - [ ]* 8.1 Write a performance test marked `@pytest.mark.perf` in `tests/test_perf.py`
    - Generate a list of 1,000 strings and time `run_all_sorts` against it; assert elapsed time < 5 seconds
    - _Requirements: 3.3_

- [ ] 9. Final checkpoint — wire everything together
  - Verify `app.py` imports resolve correctly from `algorithms.py`, `logic.py`, and `word_list.py`
  - Ensure all non-optional tests pass; ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- All 10 design correctness properties are covered by property-based tests in `tests/test_properties.py` using `hypothesis` with `max_examples=100`; each test is annotated with its property number and the requirements clause it validates
- Algorithm sort orders differ: Bubble Sort and Selection Sort use Python default `sorted()` (uppercase precedes lowercase); Quick Sort uses `key=lambda s: (s.casefold(), s)`
- Session state keys are always initialised with `setdefault` to prevent `KeyError` on first Streamlit load
- The `@pytest.mark.perf` test can be excluded from the normal suite with `pytest -m "not perf"`
- Checkpoint tasks exist to catch integration issues layer by layer before proceeding

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["2.1"] },
    { "id": 1, "tasks": ["3.1", "3.3", "3.5", "5.1", "5.3", "7.1"] },
    { "id": 2, "tasks": ["3.2", "3.4", "3.6", "3.7", "5.2", "5.4"] },
    { "id": 3, "tasks": ["5.5", "7.2", "7.3"] },
    { "id": 4, "tasks": ["7.4"] },
    { "id": 5, "tasks": ["7.5"] },
    { "id": 6, "tasks": ["7.6", "8.1"] }
  ]
}
```
