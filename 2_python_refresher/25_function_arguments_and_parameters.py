def some_func(a: str, b: str) -> str:
    return f"{a} {b}"


print(some_func(b="B", a="A") * 4)


def arg_func(*args: str) -> None:
    a, b, c = args
    print(a, b, c)


arg_func("A", "B", "C")
