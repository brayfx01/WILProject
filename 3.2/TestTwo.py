class Object:
    def __init__(self, volume):
        self.volume = volume

def find_combination(objects, target_volume):
    n = len(objects)

    # Helper function to find all combinations recursively
    def find_combination_recursive(index, current_combination, current_total_volume):
        nonlocal best_combination, best_total_volume

        if current_total_volume >= target_volume:
            if best_combination is None or (current_total_volume < best_total_volume and current_total_volume >= target_volume):
                best_combination = current_combination
                best_total_volume = current_total_volume
            return

        if index >= n:
            return

        # Include the current object in the combination
        current_object = objects[index]
        find_combination_recursive(index + 1, current_combination + [current_object], current_total_volume + current_object.volume)

        # Exclude the current object from the combination
        find_combination_recursive(index + 1, current_combination, current_total_volume)

    # Sort objects in descending order based on volume
    objects.sort(key=lambda obj: obj.volume, reverse=True)

    # Initialize the best combination and total volume
    best_combination = None
    best_total_volume = float('inf')

    # Start the recursive search
    find_combination_recursive(0, [], 0)

    return best_combination

# Example usage
objects = [Object(50), Object(50), Object(50)]
target_volume = 250.10
best_combination = find_combination(objects, target_volume)
if best_combination:
    total_volume = sum(obj.volume for obj in best_combination)
    print("Best combination:")
    for obj in best_combination:
        print(f"Object with volume {obj.volume}")
    print(f"Total volume: {total_volume}")
else:
    print("No combination found")
