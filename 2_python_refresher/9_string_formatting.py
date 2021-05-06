name: str = "Bob"
hello_str: str = f"Hello, {name}"

greeting: str = "Hello, {} {} {}"

print(hello_str)
print(greeting.format(*[name, "Jane", "Jack"]))
print(greeting.format(name, "Jane", "Jack"))
