from typing import Callable

add: Callable[[int, int], int] = lambda x, y: x + y
double: Callable[[int], int] = lambda x: x * x
print(add(5, 7))

sequence: list[int] = [1, 3, 7, 9]
doubled: list[int] = list(map(lambda x: x * x, sequence))
print(doubled)
