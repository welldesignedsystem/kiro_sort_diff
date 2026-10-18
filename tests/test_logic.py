"""Unit tests for the logic layer: parse_input, _reference_sorted, run_all_sorts."""

import pytest
from logic import parse_input, _reference_sorted, run_all_sorts, SortOutcome


# --------------------------------------------------------------------------- #
# parse_input                                                                 #
# --------------------------------------------------------------------------- #

def test_parse_empty_string():
    assert parse_input("") == []


def test_parse_whitespace_only():
    assert parse_input("   \n  \n\t") == []


def test_parse_strips_whitespace():
    assert parse_input("  apple  \n  banana  ") == ["apple", "banana"]


def test_parse_discards_blank_lines():
    assert parse_input("apple\n\nbanana\n\n") == ["apple", "banana"]


def test_parse_preserves_duplicates():
    assert parse_input("apple\nbanana\napple") == ["apple", "banana", "apple"]


def test_parse_truncates_long_string():
    long = "a" * 600
    result = parse_input(long)
    assert len(result[0]) == 500


def test_parse_truncates_list_to_1000():
    raw = "\n".join(["word"] * 1200)
    result = parse_input(raw)
    assert len(result) == 1000


def test_parse_single_word():
    assert parse_input("hello") == ["hello"]


# --------------------------------------------------------------------------- #
# _reference_sorted                                                           #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("algo", ["Bubble Sort", "Selection Sort", "Quick Sort", "Merge Sort"])
def test_reference_sorted_matches_sorted(algo):
    strings = ["cherry", "apple", "42", "banana"]
    assert _reference_sorted(strings, algo) == sorted(strings)


def test_reference_sorted_empty():
    assert _reference_sorted([], "Bubble Sort") == []


# --------------------------------------------------------------------------- #
# run_all_sorts                                                               #
# --------------------------------------------------------------------------- #

def test_run_all_sorts_returns_four_outcomes():
    outcomes = run_all_sorts(["banana", "apple", "cherry"])
    assert len(outcomes) == 4


def test_run_all_sorts_algorithm_order():
    outcomes = run_all_sorts(["b", "a"])
    assert [o.algorithm for o in outcomes] == [
        "Bubble Sort", "Selection Sort", "Quick Sort", "Merge Sort"
    ]


def test_run_all_sorts_all_accurate():
    outcomes = run_all_sorts(["cherry", "apple", "42", "banana", "9"])
    for o in outcomes:
        assert o.is_accurate, f"{o.algorithm} reported inaccurate"


def test_run_all_sorts_empty_input():
    outcomes = run_all_sorts([])
    for o in outcomes:
        assert o.result.sorted_list == []
        assert o.result.step_count == 0
        assert o.is_accurate


def test_run_all_sorts_single_element():
    outcomes = run_all_sorts(["only"])
    for o in outcomes:
        assert o.result.sorted_list == ["only"]
        assert o.is_accurate


def test_run_all_sorts_returns_sortoutcome_instances():
    outcomes = run_all_sorts(["b", "a"])
    for o in outcomes:
        assert isinstance(o, SortOutcome)


def test_run_all_sorts_sorted_output_matches():
    inp = ["fig", "apple", "42", "cherry", "banana"]
    expected = sorted(inp)
    outcomes = run_all_sorts(inp)
    for o in outcomes:
        assert o.result.sorted_list == expected, f"{o.algorithm}: {o.result.sorted_list}"
