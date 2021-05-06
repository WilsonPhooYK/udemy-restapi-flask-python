class Student:
    def __init__(self, name: str, grades: tuple[int, ...]) -> None:
        self.name = name
        self.__grades = grades

    def average(self):
        return sum(self.__grades) / len(self.__grades)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name


student: Student = Student("Rolf", (90, 90, 93, 78, 90))
print(student.name)
print(student.average())
