import numpy as np
import matplotlib.pyplot as plt

# Sample data
data = [
    ("nameOne", 10,0),
    ("nameOne", 20,0),
    ("nameTwo", 15,0),
    ("nameTwo", 0,0),
    ("nameTwo", 25,0),
    ("nameThree", 5,0),
    ("nameThree", 15,0),
]

# Separate the data by names
name_data = {}
for name, value,nothing in data:
    if name in name_data:
        print(name)
        name_data[name].append(value)
    else:
        name_data[name] = [value]
print(name_data)
# Create a figure and axis
fig, ax = plt.subplots()

# Plot each individual name's values on the same graph
for name, values in name_data.items():
    plt.plot(range(len(values)), values, marker='o', label=name)

plt.title("Values for Different Names")
plt.xlabel("Entry")
plt.ylabel("Value")
ax.legend()

plt.show()
