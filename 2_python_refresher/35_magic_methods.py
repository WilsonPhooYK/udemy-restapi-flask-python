class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    # def __str__(self) -> str:
    #   return "hello"

    def __repr__(self) -> str:
        return f"<Person('{self.name}', {self.age})>"


bob: Person = Person("Bob", 35)
print(bob)
