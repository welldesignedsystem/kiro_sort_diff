"""
algorithms.py — Pure sorting functions and shared data types.

Each function is a stateless, side-effect-free operation on a list of strings.
Step counts reflect the total number of pairwise comparisons performed,
including comparisons that do not result in a swap.
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class SortResult:
    """Immutable result of a single sorting algorithm run."""

    sorted_list: List[str]  # output strings in sorted order
    step_count: int         # non-negative count of pairwise comparisons made


def bubble_sort(strings: List[str]) -> SortResult:
    """Sort strings using Bubble Sort.

    Sort order: case-sensitive ascending lexicographic (Python default <),
    so uppercase letters precede lowercase letters for the same character.
    step_count counts every pairwise comparison, including non-swaps.
    Returns step_count=0 for empty or single-element input.
    """
    arr = list(strings)
    n = len(arr)
    step_count = 0

    for i in range(n):
        for j in range(0, n - i - 1):
            step_count += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return SortResult(sorted_list=arr, step_count=step_count)


def selection_sort(strings: List[str]) -> SortResult:
    """Sort strings using Selection Sort.

    Sort order: case-sensitive ascending lexicographic (Python default <).
    step_count is exactly n*(n-1)//2 for any input of length n.
    All duplicates are preserved. Returns step_count=0 for n <= 1.
    """
    lst = list(strings)
    n = len(lst)
    step_count = 0

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            step_count += 1
            if lst[j] < lst[min_idx]:
                min_idx = j
        lst[i], lst[min_idx] = lst[min_idx], lst[i]

    return SortResult(sorted_list=lst, step_count=step_count)


def quick_sort(strings: List[str]) -> SortResult:
    """Sort strings using Quick Sort (Lomuto partition).

    Sort order: ascending by ASCII/Unicode value (same as Python default <).
    step_count counts every element-vs-pivot comparison.
    Returns step_count=0 for empty or single-element input.
    """
    lst = list(strings)
    n = len(lst)
    if n <= 1:
        return SortResult(sorted_list=lst, step_count=0)

    counter = [0]

    def _partition(arr: List[str], lo: int, hi: int) -> int:
        pivot = arr[hi]
        i = lo - 1
        for j in range(lo, hi):
            counter[0] += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
        return i + 1

    def _quicksort(arr: List[str], lo: int, hi: int) -> None:
        if lo < hi:
            p = _partition(arr, lo, hi)
            _quicksort(arr, lo, p - 1)
            _quicksort(arr, p + 1, hi)

    _quicksort(lst, 0, n - 1)
    return SortResult(sorted_list=lst, step_count=counter[0])


def merge_sort(strings: List[str]) -> SortResult:
    """Sort strings using Merge Sort.

    Sort order: case-sensitive ascending lexicographic (Python default <).
    step_count counts every pairwise comparison made during the merge phase.
    Returns step_count=0 for empty or single-element input.
    """
    arr = list(strings)
    counter = [0]

    def _merge(left: List[str], right: List[str]) -> List[str]:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            counter[0] += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def _mergesort(lst: List[str]) -> List[str]:
        if len(lst) <= 1:
            return lst
        mid = len(lst) // 2
        return _merge(_mergesort(lst[:mid]), _mergesort(lst[mid:]))

    sorted_arr = _mergesort(arr)
    return SortResult(sorted_list=sorted_arr, step_count=counter[0])
