from __future__ import annotations
from operator import itemgetter
from typing import Callable, TypedDict

PersonType = TypedDict("PersonType", {
    "name": str,
    "age": int,
})
FinderType = Callable[[PersonType], str]

def search(sequence:list[PersonType], expected: str, finder:FinderType):
    for elem in sequence:
        if finder(elem) == expected:
            return elem
    raise RuntimeError(f"Could not find an element with {expected}.")

friends: list[PersonType] = [
    {"name": "Rolf", "age": 24},
    {"name": "adam", "age": 30},
    {"name": "Anne", "age": 27},
]

try:
    print(search(friends, "aolf", itemgetter("name")))
except RuntimeError as e:
    print(e)
