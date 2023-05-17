import numpy as np
my_array = np.empty(7, dtype=object)
print(my_array[0])
for i in range(my_array.size):
    my_array[i] = np.array([i,i,i])
print(my_array[0])