import numpy as np
myArray =  np.empty(2, dtype=object)
print(myArray.shape)
for i in range(myArray.size):
    myArray[i] = np.array([i, i,i])

print(myArray)
myArray[1][0] = 100
print(myArray)
# Get the indices that would sort the array based on the first element of each sub-array
sort_indices = np.argsort(-1 * np.array([subarray[0] for subarray in myArray]), kind='quicksort')


# Apply the indices to the original array
sorted_array = myArray[sort_indices]

print("Sorted array based on the first element of each sub-array:")
print(sorted_array)