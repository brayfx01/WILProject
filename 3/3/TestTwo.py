import re
from EnergyHandler import energyHandler

#thiss will calculate the loss of energy per cycle of charging

class onOffDrain:
    def __init__(self,target,drain):
        self.target = target *( drain/100)
    def RTP(self):
        return self.target
class Tank:
    def __init__(self,tName,volume,soc):
        self.tName = tName
        self.volume = volume
        self.soc = (soc/100)  #makes this a percentage
    #how much of the battery is charged
    def currentChargedCapacity(self):
        self.chargedCapacity = self.volume *(self.soc)
        return self.chargedCapacity
    # how much is not chraged
    def remainingCapacity(self):
        remainingCapacity = self.volume - self.currentChargedCapacity()
        return remainingCapacity 
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
#Where the system will be initalized
class systemInitalization():
    def __init__(self):
        self.cells = []
          # this will create the strucutre of the sections and containers
        numSections = self.getSectionCount("config2.0.txt")
        for i in range(numSections):
            # we are going to dynamically create the name for the sections 
            sectionName = f"Section {i + 1}:" # + 1 because we start at 0 now 
            nextSection = f"Section {i + 2}:"
            # Now we are going to create the number of containers for each section 
            # we are going to first get the number of containers for this section by calling a function called getContainers
            numberOfContainers = self.getCount("Number of Containers:", sectionName, nextSection) 
            self.cells.append(section(sectionName, numberOfContainers, 5))
            self.initalizeTanks()
        #now we want to go and get the number of containers in each section
         #this is getting the number of containers in a section
    def getCount(self,target, sectionName, nextSection):
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
    def getCriticalInfo(self,target):
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

    def getSectionCount(self,file):
        with open(file, "r") as file:
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
        return numSections
    def initalizeTanks(self):
        self.tanks = []
        numberofTanks = self.getCriticalInfo("Number Of Tanks")
        VolumneOfTanks = self.getCriticalInfo("Volume")
        socOfTanks = self.getCriticalInfo("SOC")
        for i in range(numberofTanks):
            tankName = f"Tank { i+1}"
            self.tanks.append(Tank(tankName,VolumneOfTanks,socOfTanks))
    def getSections(self):
        return self.cells
    def getTanks(self):
        return self.tanks
#now we want to go and get the number of containers in each section
   #this is getting the number of containers in a section
    def getCount(self,target, sectionName, nextSection):
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

cells =[]
tanks = []
tankVolumesForSection = []
tankSOCForSections = []

system = systemInitalization() # this will create all the sections
cells = system.getSections()
tanks = system.getTanks()
temp = energyHandler(1000,tanks)
print(tanks[1].currentChargedCapacity())




# to do for tommorow
# add in the storage condidtions it will include utilizing
# the round trip efficiency
# if this is done move onto the system clock as this will determine what we are looking at when storing
# when this is done then look at finding more datasets for testing and implementing these