import numpy as np

# Open the configuration file
with open('config.txt', 'r') as f:

    # Initialize variables
    current_section = None
    current_container = None
    myArray = []

    # Loop through each line of the file
    for line in f:

        # Check if the line starts with "Section"
        if line.startswith('Section'):

            # If we're currently processing a container, add it to the current section
            if current_container is not None:
                myArray[-1].append(current_container)

            # Update the current section and create a new empty list for its containers
            current_section = line.strip()
            current_container = {'name': None, 'batteries': []}
            myArray.append([])

        # Check if the line starts with "Container"
        elif line.startswith('Container'):

            # If we're currently processing a container, add it to the current section
            if current_container['name'] is not None:
                myArray[-1].append(current_container)

            # Update the current container and create a new empty list for its batteries
            current_container = {'name': line.strip(), 'batteries': []}
        
        # Check if the line starts with "Battery"
        elif line.startswith('Battery'):
            # If we're currently processing a battery, add it to the current container
            current_container['batteries'].append(line.strip())

    # Add the final container to the current section
    if current_container['name'] is not None:
        myArray[-1].append(current_container)

# Print the resulting 2D array
for i, section in enumerate(myArray):
    print(f"Section {i+1}:")
    for j, container in enumerate(section):
        print(f"  {container['name']}")
        print("        Batteries:")
        for battery in container['batteries']:
            print(f"            - {battery}")
