from typing import Literal, Union


def add(x: int, y: Union[str, int]) -> int:
    if type(y) is int:
        return x + y
    return 0


# nums: dict[str, int] = {"c": 15, "y": 25}
# Needs to be same key
nums: dict[str, int] = {"x": 15, "y": 25}
# Unpack into add(x=15, y=25)
print(add(**nums))


def multiply(*args: int) -> int:
    total = 1
    for arg in args:
        total *= arg

    return total


def apply(*args: int, operator: Literal["*", "+"]):
    if operator == "*":
        return multiply(*args)
    elif operator == "+":
        return sum(args)
    else:
        return "No valid operator provided to apply()."


print(apply(1, 3, 6, 7, operator="*"))
