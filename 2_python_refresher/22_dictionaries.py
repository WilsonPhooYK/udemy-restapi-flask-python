from typing import TypedDict

PersonType = TypedDict("PersonType", {
    "name": str,
    "age": int,
})

friends: list[PersonType] = [
    {"name": "Rolf", "age": 24},
    {"name": "Adman", "age": 30},
    {"name": "Anne", "age": 27},
]

friends_dict: dict[str, dict[str, int]] = {friend["name"]: {"age": friend["age"]} for friend in friends}
print(friends_dict)

sum_age_friends: int = sum([value for _, item in friends_dict.items() for value in item.values()])
print(sum_age_friends)
