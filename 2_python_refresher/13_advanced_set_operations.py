friends: set[str] = {"Bob", "Rob", "Anne"}
abroad: set[str] = {"Bob", "Anne", "Jack"}
# Need comma to denote tuple
tuple_single: tuple[str] = ("Jannie",)

local_friends: set[str] = friends.difference(abroad)
# all_friends: set[str] = friends.union(abroad)
all_friends: set[str] = {*friends, *abroad}
intersect_friends: set[str] = friends.intersection(abroad)

print(local_friends)
print(all_friends)
print(intersect_friends)
