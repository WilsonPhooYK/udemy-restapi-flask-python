t: tuple[int, int] = 5, 11
x, y = t

person: tuple[str, int, str] = ("Bob", 42, "Mechanic")
name, _, profession = person

head, *middle, tail = [1, 2, 3, 4, 5]

print(head, middle, tail)
