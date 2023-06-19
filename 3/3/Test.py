import re
class RoundTripEffiency:
    def __init__(self,target,efficency):
        self.target = target 
class Tank:
    def __init__(self,tName,volume,soc):
        self.tName = tName
        self.volume = volume
        self.soc = soc
    def currentChargedCapacity(self):
        chargedCapacity = self.volume *(self.soc/100)
        return chargedCapacity

class container:
    def __init__(self, sName,cName,onOffEfficency):
        self.cName = cName# contianer name
        self.sName = sName# Section Name
        self.onOffEfficency = onOffEfficency
  # create section and containers      
class section:
    def __init__(self, sName,numberOfContainers,onOffEfficency):
        self.sName = sName
        self.onOffEfficency = onOffEfficency
        self.containers = []
        for i in range(numberOfContainers):
            self.containers.append(container(self.sName,f"Container {i + 1}", self.onOffEfficency))

with open("config2.0.txt", "r") as file:
        # Read the contents of the file
            configFile = file.read()

            # Split the content into sections based on the "Section" keyword
            sections = configFile.split("Section")
            # Exclude the first empty section (if any)
            if sections[0].strip() == "":
                sections = sections[1:]
            # Get the count of sections
            numSections = len(sections) -1

file.close()
#now we want to go and get the number of containers in each section
   #this is getting the number of containers in a section
def getCount(target, sectionName, nextSection):
        # Initialize variables
        sectionFound = False
        containerCount = 0

        # Read the text file
        with open("config2.0.txt", "r") as file:
        # Iterate over the lines in the file
            for line in file:
                line = line.strip()

                # Check if Section 2 is encountered
                if line == nextSection or line == "END":
                    break

                # Check if Section 1 is found
                if line == sectionName:
                    sectionFound = True
                    continue

                # this will check to see if line contains the key word container and section found
                if sectionFound and target in line:
                    number = re.findall(r'\d+', line)
                    containerCount = int(number[0])

            # Cselflose the file
        file.close()
        return containerCount
def getCriticalInfo(target):
        # Read the text file
        targetCount = 0
        with open("config2.0.txt", "r") as file:
        # Iterate over the lines in the file
            for line in file:
                line = line.strip()

                # Check if Section 2 is encountered
                if line == "END":
                    break

                # this will check to see if line contains the key word container and section found
                if  target in line:
                    number = re.findall(r'\d+', line)
                    targetCount = int(number[0])

            # Cselflose the file
        file.close()
        return targetCount


onOffEfficencey = getCriticalInfo("Container On Off efficency ")
roundTripEfficency = getCriticalInfo("RoundTripEffiency")

numberofTanks = getCriticalInfo("Number Of Tanks")
VolumneOfTanks = getCriticalInfo("Volume")
socOfTanks = getCriticalInfo("SOC")

totalCharged = 0

cells =[]
tanks = []
tankVolumesForSection = []
tankSOCForSections = []

for i in range(numberofTanks):
    tankName = f"Tank{ i+1}"
    tanks.append(Tank(tankName,VolumneOfTanks,socOfTanks))
# this will get the total charged capacity of the system
for tank in tanks:
    totalCharged = totalCharged + tank.currentChargedCapacity()

 # this will create the strucutre of the sections and containers
for i in range(numSections):
    # we are going to dynamically create the name for the sections 
    sectionName = f"Section {i + 1}:" # + 1 because we start at 0 now 
    nextSection = f"Section {i + 2}:"
    # Now we are going to create the number of containers for each section 
    # we are going to first get the number of containers for this section by calling a function called getContainers
    numberOfContainers = getCount("Number of Containers:", sectionName, nextSection) 
    cells.append(section(sectionName, numberOfContainers, 5))
"""
for section in cells:
    print(section.sName)
    for container in section.containers:
        print("     ",container.cName)
"""