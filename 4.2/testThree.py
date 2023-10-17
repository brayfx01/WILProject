data = [
    ("Section1", "Name1", 1),
    ("Section2", "Name2", 2),
    ("Section1", "Name1", 3),  # Name1 with multiple values
    ("Section2", "Name2", 4),  # Name2 with multiple values
]

result = {}

for section, name, value in data:
    if section not in result:
        result[section] = {}
    if name not in result[section]:
        result[section][name] = []  # Create a list for the name if it doesn't exist
    result[section][name].append(value)  # Append the value to the name's list

print(result)
