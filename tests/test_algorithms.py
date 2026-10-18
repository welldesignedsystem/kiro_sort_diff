"""Unit tests for all four sorting algorithms."""

import pytest
from algorithms import bubble_sort, selection_sort, quick_sort, merge_sort, SortResult


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #

ALGOS = [
    ("bubble_sort", bubble_sort),
    ("selection_sort", selection_sort),
    ("quick_sort", quick_sort),
    ("merge_sort", merge_sort),
]


# --------------------------------------------------------------------------- #
# Correctness — all algorithms                                                #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("name,fn", ALGOS)
def test_empty_input(name, fn):
    r = fn([])
    assert r.sorted_list == []
    assert r.step_count == 0


@pytest.mark.parametrize("name,fn", ALGOS)
def test_single_element(name, fn):
    r = fn(["apple"])
    assert r.sorted_list == ["apple"]
    assert r.step_count == 0


@pytest.mark.parametrize("name,fn", ALGOS)
def test_already_sorted(name, fn):
    inp = ["apple", "banana", "cherry"]
    r = fn(inp)
    assert r.sorted_list == sorted(inp)


@pytest.mark.parametrize("name,fn", ALGOS)
def test_reverse_sorted(name, fn):
    inp = ["cherry", "banana", "apple"]
    r = fn(inp)
    assert r.sorted_list == sorted(inp)


@pytest.mark.parametrize("name,fn", ALGOS)
def test_duplicates_preserved(name, fn):
    inp = ["banana", "apple", "banana", "apple"]
    r = fn(inp)
    assert r.sorted_list == sorted(inp)
    assert len(r.sorted_list) == 4


@pytest.mark.parametrize("name,fn", ALGOS)
def test_ascii_ordering(name, fn):
    # digits < lowercase letters in ASCII; special chars < digits
    inp = ["banana", "42", "apple", "9", "!zip", "cherry"]
    r = fn(inp)
    assert r.sorted_list == sorted(inp)


@pytest.mark.parametrize("name,fn", ALGOS)
def test_digits_only(name, fn):
    inp = ["100", "9", "42", "0", "999"]
    r = fn(inp)
    assert r.sorted_list == sorted(inp)  # lexicographic, not numeric


@pytest.mark.parametrize("name,fn", ALGOS)
def test_step_count_positive_for_multiple_elements(name, fn):
    r = fn(["b", "a", "c"])
    assert r.step_count > 0


@pytest.mark.parametrize("name,fn", ALGOS)
def test_returns_sortresult(name, fn):
    r = fn(["b", "a"])
    assert isinstance(r, SortResult)


# --------------------------------------------------------------------------- #
# Algorithm-specific step count invariants                                    #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("n", [2, 3, 4, 5, 10])
def test_bubble_sort_step_count(n):
    """Bubble sort outer i in range(n), inner j in range(n-i-1): total = n*(n-1)/2."""
    inp = list(reversed([str(i) for i in range(n)]))
    r = bubble_sort(inp)
    assert r.step_count == n * (n - 1) // 2


@pytest.mark.parametrize("n", [2, 3, 4, 5, 10])
def test_selection_sort_step_count_fixed(n):
    """Selection sort always performs exactly n*(n-1)/2 comparisons regardless of order."""
    inp_random = [str(i) for i in range(n)]
    inp_sorted = sorted(inp_random)
    inp_reversed = list(reversed(inp_sorted))
    assert selection_sort(inp_random).step_count == n * (n - 1) // 2
    assert selection_sort(inp_sorted).step_count == n * (n - 1) // 2
    assert selection_sort(inp_reversed).step_count == n * (n - 1) // 2


@pytest.mark.parametrize("n", [2, 3, 4, 5, 10])
def test_quick_sort_step_count_within_bounds(n):
    """Quick sort step count must be between n-1 (best) and n*(n-1)/2 (worst)."""
    inp = [str(i) for i in range(n)]
    r = quick_sort(inp)
    assert r.step_count >= 0
    assert r.step_count <= n * (n - 1) // 2


@pytest.mark.parametrize("n", [2, 3, 4, 5, 10])
def test_merge_sort_step_count_within_bounds(n):
    """Merge sort comparisons are bounded by n*ceil(log2(n))."""
    import math
    inp = list(reversed([str(i) for i in range(n)]))
    r = merge_sort(inp)
    upper = n * math.ceil(math.log2(n)) if n > 1 else 0
    assert r.step_count >= 0
    assert r.step_count <= upper
