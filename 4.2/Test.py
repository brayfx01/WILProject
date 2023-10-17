# Example multidimensional array
multi_array = [
    ['section1', 'name1', 'value1'],
    ['section1', 'name2', 'value2'],
    ['section2', 'name3', 'value3'],
    ['section2', 'name4', 'value4'],
]

# Initialize an empty dictionary
result_dict = {}

# Loop through the multidimensional array and convert it into a dictionary
for item in multi_array:
    section, name, value = item
    if section not in result_dict:
        result_dict[section] = {}  # Create a new dictionary for the section if it doesn't exist
    result_dict[section][name] = value

print(result_dict["section1"])
