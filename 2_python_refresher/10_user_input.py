size_input: str = input("How big is your house (in square feet): ")

try:
    # All inputs are strings
    square_feet: int = int(size_input)
    square_metres: float = square_feet / 10.8

    # To 2 decimal places
    print(f"Square feet: {square_feet}ft = {square_metres:,.2}m")
except ValueError:
    print("Oops!  That was no valid number.  Try again...")
