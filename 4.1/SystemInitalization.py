
import re
from Section import Section
from Tank import Tank
from ReadData import ReadData
from EnergyHandler import energyHandler
from FullEmpty import FullEmpty
from RoundTripEfficency import roundTripEffiency
import pandas as pd

class systemInitalization():
    def __init__(self, generated,load,configFile):
        self.cells = []
        self.RTE = 0
        self.tanks = []
        self.configFile = configFile
        self.generated = pd.read_csv(generated)
        self.load = pd.read_csv(load)
        # this will initialize the datasets
        ##self.data.read(generated,load)
        self.fullEmpty = None
        
        #self.generatedSurplus = self.data.getGeneratedSurplus()
        self.initalizeTanks()
          # this will create the strucutre of the sections and containers
        numSections = self.getSectionCount(configFile)
        for i in range(numSections):
            # we are going to dynamically create the name for the sections 
            sectionName = f"Section {i + 1}:" # + 1 because we start at 0 now 
            nextSection = f"Section {i + 2}:"
            # Now we are going to create the number of containers for each section 
            # we are going to first get the number of containers for this section by calling a function called getContainers
            numberOfContainers = self.getCount("Number of Containers:", sectionName, nextSection) 
            self.cells.append(Section(sectionName, numberOfContainers, self.getCriticalInfo("Container On Off Efficency"),self.tanks))

        #now we want to go and get the number of containers in each section
         #this is getting the number of containers in a section
    def generateSurplus(self):
        difference = self.generated["Power(MW)"] - self.load["total load actual"]
        difference = difference.dropna()
        return difference
        

    def getCount(self,target, sectionName, nextSection):
        # Initialize variables
        sectionFound = False
        containerCount = 0

        # Read the text file
        with open(self.configFile, "r") as file:
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
        with open(self.configFile, "r") as file:
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
        tankName = None
        tankVolume = 0
        socTank = 0

        with open(self.configFile, "r") as file:
        # Iterate over the lines in the file
            line = ""
            for line in file:
                line = line.strip()

                # Check if Section 2 is encountered
                if line == "END":
                    break

                # this will check to see if line contains the key word container and section found
                if  "Tanks:" in line:
                    # while it is not == end then check if the line is Tanks
                    while(line != "END"):
                        # getting what makes up a tank
                        line = file.readline().strip()
                        # if section encountered end this
                        if "Section" in line:
                            break
                        # so if line contains Tank
                        if "Tank" in line:
                            tankName = line
                            line = file.readline().strip()
                            pattern = r'\d+'# one or more digits
                            # this will extract the number from the string
                            tankVolume = [int(match) for match in re.findall(pattern, line)][0]
                            line = file.readline().strip()
                            socTank = [int(match) for match in re.findall(pattern, line)][0]

                            # now appending this to the aray 
                            self.tanks.append(Tank(tankName,tankVolume,socTank))
            # Cselflose the file
        file.close()
   
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
            with open(self.configFile, "r") as file:
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
    def getSections(self):
            return self.cells
    def getTanks(self):
        return self.tanks
    def getRTE(self):
        self.efficency = self.getCriticalInfo("Round Trip Efficency")
        self.RTE = roundTripEffiency(self.efficency)
        return self.RTE
    def getFullEmpty(self):
        self.fullEmpty = FullEmpty(self.tanks)
        return self.fullEmpty
            
                
        
            