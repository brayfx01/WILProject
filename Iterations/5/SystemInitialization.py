import Cells
import sys
class SystemInitialization:
    def __init__(self, text):
        with open("config.txt", "r") as file:
        # Read the contents of the file
            configFile = file.read()

        # Split the content into sections based on the "Section" keyword
        sections = configFile.split("Section")
        # Exclude the first empty section (if any)
        if sections[0].strip() == "":
            sections = sections[1:]
        # Get the count of sections
        numSections = len(sections)

        file.close()



        self.instances = []  # Create an empty list to store instances

        num_instances = numSections  # Number of instances you want to create
        numContainers = 0 #instantiated else where
        numBatteries =0# instantiated elsewhere

        #where the cells are created
        for i in range(num_instances):
            name = f"Section {i+1}:"  # Generate a dynamic name for each instance
            nameTwo =   f"Section {i+2}:" 
            numContainers = self.getContainerCount(name,nameTwo)
            instance = Cells.Cells(name, numContainers, numBatteries)  # Create an instance of MyClass
            self.instances.append(instance)  # Add the instance to the list

        # Accessing the instances


   

    def Instances(self):
        return self.instances
    def printInstances(self):
        for instance in (self.instances):
            print(instance.name)
            for container in (instance.containers):
                print(" ",container.name)
                for battery in (container.batteries):
                    print("     ", battery.bName)
                    print("         CurrentCapacity", battery.currentCapacity, "    MaxCapacity " , battery.maxCapacity)
      
    # this will get the info of one of the batteries in the corresponding container
    def getBatteryInfo(sName,cName, bName):
        # Initialize variables
        section1_found = False
        containerFound = False
        maxCapacity = 0;
        currentCapacity = 0;
        # Read the text file
        with open("config.txt", "r") as file:
        # Iterate over the lines in the file
            for line in file:
                line = line.strip()

                # Check if Section 2 is encountered
                if line == "END" or "Container" in line and containerFound==True and section1_found == True or "Section" in line and section1_found == True:
                    break

                # Check if Section 1 is found
                if line == sName:
                    section1_found = True
                    continue
                if line == cName and section1_found == True:
                    containerFound = True
                    continue

                # Count containers in Section 1
                if section1_found and containerFound == True and line.startswith(bName):
                    # Extract the substring containing capacity information
                    capacity_info = line.split(":")[1].strip()
                    #essentailly grabs the value of max and current capaicty
                    current_capacity_str = capacity_info.split(",")[0].split("=")[1].strip()
                    currentCapacity = int(current_capacity_str.replace(" ", ""))
        
                    # Extract max capacity value
                    max_capacity_str = capacity_info.split(",")[1].split("=")[1].strip()
                    maxCapacity = int(max_capacity_str.replace(" ", ""))

                
        file.close()
        if(currentCapacity < 0):# this is not an acceptable value so throw an error 
            print("CurrentCapacity cannot be negative. Please review the config file")
            sys.exit()
        elif (maxCapacity <0):
            print("Max Capacity cannot have a negative value. Please review the config file")
            sys.exit()
        if(currentCapacity > maxCapacity):# this is an issue throw an error 
            print("Max value has to be equal to or greater than the currentCapacity please review config file")
            sys.exit()
        return currentCapacity,maxCapacity
   

    def getContainerCount(self,name, nameTwo):
        # Initialize variables
        section1_found = False
        container_count = 0

        # Read the text file
        with open("config.txt", "r") as file:
        # Iterate over the lines in the file
            for line in file:
                line = line.strip()

                # Check if Section 2 is encountered
                if line == nameTwo or line == "END":
                    break

                # Check if Section 1 is found
                if line == name:
                    section1_found = True
                    continue

                # Count containers in Section 1
                if section1_found and line.startswith("Container"):
                    container_count += 1

            # Cselflose the file
        file.close()
        return container_count
    #This will essentially determine if we need to store or take energy and how it is done
    def energyHandler(self,energy, action):
        if(action == 0): # this means we need to store energy so 
            #Now we will need to go through and get the battery with the lowest capacity 
            # then we can store
            i = 0 #used to set the intiail minimumCapacity of the system
            minimumStorageCapacity = 0# this will be the container with the smallest capacity to maxCapacity ratio
            section = None
            for instance in (self.instances): # cycling throw the sections one by on e
                for container in (instance.containers): #now we are dealing with the containers
                    #sum up the max and minimum capacity of this container and subtract them to determine the 
                    # remaing storage potential
                    for battery in (container.batteries):
                        sumOfMaxCapacity = sumOfMaxCapacity + battery.maxCapacity
                        sumOfCurrentCapacity = sumOfCurrentCapacity + battery.currentCapacity
                    remainingCapacity = sumOfMaxCapacity - sumOfCurrentCapacity
                    if(i == 0): # essentially we are in the first section so set it to this by default
                        section = container  