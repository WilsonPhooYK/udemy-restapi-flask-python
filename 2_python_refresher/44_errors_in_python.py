def divide(dividend: int, divisor: int) -> float:
    if divisor == 0:
        raise ZeroDivisionError("Divisor canot be 0.")
    return dividend / divisor

grades:list[int] = []

try:
    average:float = divide(sum(grades), len(grades))
except ZeroDivisionError as e:
    print("There are no grades yest in your list")
else:
    print(f"The average grade is {average}.")
finally:
    print("Thanks you!")