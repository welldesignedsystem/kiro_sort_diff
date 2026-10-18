"""
word_list.py — Predefined word list constant.

Only lowercase letters, digits, and special characters (ordered by ASCII value).
No uppercase letters permitted.
"""

from typing import List

PREDEFINED_WORDS: List[str] = [
    # lowercase words
    "apple",
    "banana",
    "cherry",
    "date",
    "elderberry",
    "fig",
    "grape",
    "mango",
    "kiwi",
    "durian",
    # digit-only
    "0",
    "42",
    "100",
    "9999",
    # lowercase + digits
    "data2024",
    "python3",
    "sort42",
    "item99",
    # special characters (ASCII-ordered)
    "sort_me",
    "hello-world",
    "foo.bar",
    "abc#123",
    "zip!",
    "a@b",
    "x*y",
]
