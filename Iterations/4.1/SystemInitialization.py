from Battery import Battery

class SystemInitialization:
    def __init__(self, text):
        # Open the config file 
        with open(text, "r") as file:
            # Read the contents of the file
            configFile = file.read()

        # Split the content into sections based on the "Section" keyword
        sections = configFile.split("Section")

        # Exclude the first empty section (if any)
        if sections[0].strip() == "":
            sections = sections[1:]

        # Get the count of sections
        numSections = len(sections)

        # Print the number of sections
        print("Number of sections:", numSections)

        # Create a multi-dimensional array to store the battery information for each container in each section
        sectionsA = []

        # Iterate over sections and store the battery information for each container
        for section in sections:
            # Split the section into lines
            lines = section.strip().split('\n')

            # Exclude the first line (section header)
            lines = lines[1:]

            # Initialize a list to store the battery information for each container
            containerBatteries = []

            # Iterate over the lines and extract the battery information
            for line in lines:
                if "Container" in line:
                    # If a line contains "Container", create a new container list and append it to container_batteries
                    container = []
                    containerBatteries.append(container)
                elif line.strip() != "":
                    # If a line is not empty, split it by ':' to extract the battery information
                    batteryInfo = line.split(':')

                    # Extract the battery name and strip leading/trailing spaces
                    batteryName = batteryInfo[0].strip()

                    # Extract the battery capacities
                    capacities = [cap.strip() for cap in batteryInfo[1].split(",")]
                    currentCapacity = int(capacities[0].split('=')[1])
                    maxCapacity = int(capacities[1].split('=')[1].replace(" ", ""))

                    # Create a new Battery object and append it to the container list
                    battery = Battery(maxCapacity, currentCapacity)
                    container.append(battery)

            # Store the container_batteries in the my_array
            sectionsA.append(containerBatteries)

        # Assign my_array to the class-level variable self.my_array
        self.sections = sectionsA
    # Getter method to access my_array
    def Sections(self):
        return self.sections

   
