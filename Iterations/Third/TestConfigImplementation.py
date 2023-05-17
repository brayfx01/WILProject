import numpy as np

class Battery:
    def __init__(self, maxCapacity):
        self.maxCapacity = maxCapacity

class MyClass:
    def __init__(self, value, maxBatteryCapacity):
        self.value = value
        self.battery = Battery(maxBatteryCapacity)

# Create a 2x2 array of MyClass objects with individual Batteries
myArray = np.empty((2, 2), dtype=object)
for i in range(2):
    for j in range(2):
        myArray[i][j] = MyClass(i+j, (i+j)*10)

# Print the value attribute and maxCapacity attribute of each element
for i in range(2):
    for j in range(2):
        print(f"Value of element ({i}, {j}): {myArray[i][j].value}")
        print(f"Max capacity of element ({i}, {j}): {myArray[i][j].battery.maxCapacity}")
print(myArray[1][1].battery.maxCapacity)