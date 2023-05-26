import sys

class Cells:
    def __init__(self, name, numContainers, numBatteries):
        self.name = name
        self.containers = []
        for i in range(numContainers):
            cName = f"Container {i+1}:"
            container = Container(name,cName, numBatteries)
            self.containers.append(container)
        self.numContainers = len(self.containers)
class Container:
    def __init__(self, sName,name, numBatteries):
        self.name = name# contianer name
        self.sName = sName# Section Name
        self.batteries = []
        numBatteries = getBatteryCount(self.sName, self.name) # this determines how many batteries in each containe
        for i in range(numBatteries):
            #Now we want anouther fucntion to calcluate the info of the Batteres 
            # it will take in the section name container name and battery name gerenated dynamically
            bName = f"Battery {i + 1} :"
            battery = Battery(sName,name,bName,0,0)
            self.batteries.append(battery)

              

class Battery:
      def __init__(self,sName,cName, bName, currentCapacity,maxCapacity):
          self.sName = sName#Sectinon
          self.cName = cName#container
          self.bName = bName#Battery
          self.currentCapacity = currentCapacity
          self.maxCapacity = maxCapacity
          self.currentCapacity ,self.maxCapacity = getBatteryInfo(sName,cName,bName)
          
          
          

def getContaierCount(name, nameTwo):
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

       
# gets the number of battereis in the correspoinding container
def getBatteryCount(name, dName):
    # Initialize variables
    section1_found = False
    containerFound = False
    container_count = 0
    # Read the text file
    with open("config.txt", "r") as file:
    # Iterate over the lines in the file
        for line in file:
            line = line.strip()

            # Check if Section 2 is encountered
            if line == "END" or "Container" in line and containerFound==True and section1_found == True or "Section" in line and section1_found == True:
                break

            # Check if Section 1 is found
            if line == name:
                section1_found = True
                continue
            if line == dName and section1_found == True:
                containerFound = True
                continue

            # Count containers in Section 1
            if section1_found and containerFound == True and line.startswith("Battery"):
                container_count += 1

        # Cselflose the file
    file.close()
    return container_count
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
def energyHandler(energy, action,instances):
        if(action == 0): # this means we need to store energy so 
            #Now we will need to go through and get the battery with the lowest capacity 
            # then we can store
            while(energy != 0 and allFull(instances) == False): # we have energy needing to be stored
            
                section = highestCapacitySection(instances)# we get the section with the greates remaining capacity for storage 
                while(maxCapacity(section) == False and energy != 0): # if there is more storage potentail 
                    battery = getSmallestCapacityBattery(section) # this will return the battery with the greatest storage potential
                    if(battery.maxCapacity - battery.currentCapacity >= energy):# more space then required
                        battery.currentCapacity = battery.currentCapacity + energy 
                        energy = 0
                    elif(battery.maxCapacity - battery.currentCapacity < energy):
                        energy = energy - (battery.maxCapacity - battery.currentCapacity ) # substract the remaining capacity from the energy
                        battery.currentCapacity = battery.maxCapacity # set the current capacity = to max cpacity 
                        
            if(allFull(instances) == True) :# now that we have the battery we need to store the energy so 
                print("There is not enough storage for the remaining ", energy)

def highestCapacitySection(instances):
            i = 0 #used to set the intiail minimumCapacity of the system
            minimumStorageCapacity = 0# this will be the container with the smallest capacity to maxCapacity ratio
            section = None
            greatestRemaingCapacity = 0# global 
            for instance in (instances): # cycling throw the sections one by one
                sumOfMaxCapacity = 0
                sumOfCurrentCapacity = 0
                remainingCapacity = 0# local 
                for container in (instance.containers): #now we are dealing with the containers
                    #sum up the max and minimum capacity of this container and subtract them to determine the 
                    # remaing storage potential
                    for battery in (container.batteries):
                        sumOfMaxCapacity = sumOfMaxCapacity + battery.maxCapacity
                        sumOfCurrentCapacity = sumOfCurrentCapacity + battery.currentCapacity
                remainingCapacity = sumOfMaxCapacity - sumOfCurrentCapacity
                if(i == 0): # essentially we are in the first section so set it to this by default
                    greatestRemaingCapacity = remainingCapacity
                    section = instance  
                    i = 1
                if(greatestRemaingCapacity < remainingCapacity): # then there is a section with more capacity 
                    greatestRemaingCapacity = remainingCapacity
                    section = instance
            return section
def getSmallestCapacityBattery(section):
    #We are now going to cycle through the sections batteries to find the one with the greates remaing capacity
    greatestRemainingCapacity = 0
    i = 0
    chosenBattery = None
    for container in (section.containers):
        for battery in (container.batteries):
            remainingCapacity = 0
            remainingCapacity = battery.maxCapacity - battery.currentCapacity
            if(i == 0):# first battery check set it to gretest by default
                greatestRemainingCapacity = remainingCapacity
                chosenBattery = battery
                i = 1
            elif(greatestRemainingCapacity < remainingCapacity):# otherwise if tehre is one greater then this is the battery that will be chosen for storage
                greatestRemainingCapacity = remainingCapacity
                chosenBattery = battery
    return chosenBattery



def maxCapacity(section):
    # essentially what this is going to do is go through the section and determine if it is full if so then return true else return flase
    for container in (section.containers):
        for battery in (container.batteries):
            if(battery.maxCapacity == battery.currentCapacity):# this is a max filled battery
                continue
            else: #There is a battery left in the section where there is room to store
                return False
    return True# this means there are no battereis that do not have any 
def allFull(instances):
    for section in(instances):
        for containers in (section.containers):
            for battery in (containers.batteries):
                if(battery.currentCapacity == battery.maxCapacity ):
                    continue # this is full
                else: # there is at least one battery that can store more energy 
                    return False 
    return True # all bateries are full
 

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

file.close()



instances = []  # Create an empty list to store instances

num_instances = num_sections  # Number of instances you want to create
numContainers = 0 #instantiated else where
numBatteries =0# instantiated elsewhere

#where the cells are created
for i in range(num_instances):
    name = f"Section {i+1}:"  # Generate a dynamic name for each instance
    nameTwo =   f"Section {i+2}:" 
    numContainers = getContaierCount(name,nameTwo)
    instance = Cells(name, numContainers, numBatteries)  # Create an instance of MyClass
    instances.append(instance)  # Add the instance to the list

# Accessing the instances
energyHandler(-2,0,instances)

