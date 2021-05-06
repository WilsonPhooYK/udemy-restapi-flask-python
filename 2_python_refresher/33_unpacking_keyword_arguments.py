from typing import Union


def both(*args: int, **kwargs: Union[str, int]):
    print(args)
    print(kwargs)


both(1, 3, 5, name="Bob", age=25)
