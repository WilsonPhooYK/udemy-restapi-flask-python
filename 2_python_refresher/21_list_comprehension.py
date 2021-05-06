numbers: list[int] = [1, 3, 5]
doubled: list[int] = [n * 2 for n in numbers]

print(doubled)

friends: list[str] = ["Rolf", "Sam", "Samantha", "Saurbah", "Jen"]
start_s: list[str] = [friend for friend in friends if friend.startswith("S")]

print(start_s)
print(id(friends), id(start_s))
