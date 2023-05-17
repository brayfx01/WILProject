class Battery:
    def __init__(self, max_capacity, current_capacity):
        self.max_capacity = max_capacity
        self.current_capacity = current_capacity

# Open the config file
with open("config.txt", "r") as file:
    # Read the contents of the file
    config_content = file.read()

# Split the content into sections based on the "Section" keyword
sections = config_content.split("Section")

# Exclude the first empty section (if any)
if sections[0].strip() == "":
    sections = sections[1:]

# Get the count of sections
num_sections = len(sections)

# Print the number of sections
print("Number of sections:", num_sections)

# Create a multi-dimensional array to store the battery information for each container in each section
my_array = []

# Iterate over sections and store the battery information for each container
for section in sections:
    # Split the section into lines
    lines = section.strip().split('\n')

    # Exclude the first line (section header)
    lines = lines[1:]

    # Initialize a list to store the battery information for each container
    container_batteries = []

    # Iterate over the lines and extract the battery information
    for line in lines:
        if "Container" in line:
            # If a line contains "Container", create a new container list and append it to container_batteries
            container = []
            container_batteries.append(container)
        elif line.strip() != "":
            # If a line is not empty, split it by ':' to extract the battery information
            battery_info = line.split(':')

            # Extract the battery name and strip leading/trailing spaces
            battery_name = battery_info[0].strip()

            # Extract the battery capacities
            capacities = [cap.strip() for cap in battery_info[1].split(",")]
            current_capacity = int(capacities[0].split('=')[1])
            max_capacity = int(capacities[1].split('=')[1].replace(" ", ""))

            # Create a new Battery object and append it to the container list
            battery = Battery(max_capacity, current_capacity)
            container.append(battery)

    # Store the container_batteries in the my_array
    my_array.append(container_batteries)

# Print the array
print("my_array:", my_array[0][0][2].current_capacity)
#print all of the max anc current capacity of the batteries
for i in range (len(my_array)):
    for k in range(len(my_array[i])):
        for l in range(len(my_array[i][k])):
            print("Section", i + 1)
            print(" Container " ,k + 1)
            print("     Battery " , l + 1)
            print("         maxCapacity" , my_array[i][k][l].max_capacity)
            print("         currentCapacity" , my_array[i][k][l].current_capacity)
        #for future refecen if you are comming back 
        #my_array[i][k][l] I is the sections k are the containers in sections, l are the batteries in the containers in the sections