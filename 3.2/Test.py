class Object:
    def __init__(self, volume):
        self.volume = volume

def find_best_combination(objects, target):
    n = len(objects)
    # Create a 2D table to store the maximum value for each subproblem
    dp = [[0.0] * (int(target) + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, int(target) + 1):
            if objects[i - 1].volume <= j:
                # Choose the maximum value between including the current object or excluding it
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][int(j - objects[i - 1].volume)] + objects[i - 1].volume)
            else:
                # If the current object's volume is greater than the current target, exclude it
                dp[i][j] = dp[i - 1][j]

    # Retrieve the objects that make up the best combination
    combination = []
    i, j = n, int(target)
    while i > 0 and j > 0:
        print(i,j)
        if abs(dp[i][j] - dp[i - 1][j]) > 1e-9:
            combination.append(objects[i - 1])
            j -= objects[i - 1].volume
        i -= 1

    return combination

# Example usage
objects = [Object(50.5)]
target = 100.0
best_combination = find_best_combination(objects, target)
print(best_combination)
# Print the volumes of the objects in the best combination
for obj in best_combination:
    print(obj.volume)
