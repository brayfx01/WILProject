from itertools import combinations

# Your input list
items = [1, 2, 3]

# Generate combinations of different lengths
combinations_list = []
for r in range(2, len(items) + 1):  # Generating combinations of length 2 to length of items
    combinations_list.extend(combinations(items, r))

# Print the combinations
for combo in combinations_list:
    print(combo)