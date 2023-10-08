 
from Containers import container 
import re
from Tank import Tank
  # create section and containers      
class Section:
    def __init__(self, sName,numberOfContainers,onOffEfficency,tanks):
        self.sName = sName
        self.containers = []
        for i in range(numberOfContainers):
            containerName = f"Container {i + 1}"
            self.containers.append(container(self.sName,containerName, onOffEfficency,self.containerCharge(self.sName,containerName,"charge"),self.getCorrespondingTanks(tanks,sName,f"Container {i + 1}")))
   
    def containerCharge(self,sectionName,containerName,target):
        # Read the text file
        targetCount = 0
        sectionFound = False
        containerFound = False
        with open("config2.0.txt", "r") as file:
        # Iterate over the lines in the file
            for line in file:
                line = line.strip()

                # Check if Section 2 is encountered
                if line == "END":
                    break
                if sectionName in line: # we have found the right section in the config file
                  sectionFound = True
                  
                if containerName in line: # we have found a matching contianer name
                  if sectionFound == True: # it corresponds with the right section
                    containerFound = True # this is the right container
                    
                # this will check to see if line contains the key word container and section found
                if  target in line:
                    if(containerFound == True): # only return the charge if the right container has been found
                      number = re.findall(r'\d+', line)
                      targetCount = int(number[0])
                      return targetCount

            # Cselflose the file
        file.close()

    def getCorrespondingTanks(self,tanks,sectionName,containerName):
      
      correspondingTanks = [] # holds the corresponding tank objects
      target = [] # used to determine which tanks we need to get
      sectionFound = False
      containerFound = False
      with open("config2.0.txt", "r") as file:
      # Iterate over the lines in the file
          for line in file:
            
            line = line.strip()
            if sectionName in line:
              sectionFound = True
            if containerName in line and sectionFound == True:
                containerFound = True
            # Check if Section 2 is encountered
            if line == "END":
                break
            if containerFound == True: #this ensures that the corresponding containers works for each individual container 
              # this will check to see if line contains the key word container and section found
              if  "Corresponding Tanks:" in line:
                numbers = re.findall(r'\d+', line)
                for number in numbers:
                  target.append(number)
                break
                  
            # Cselflose the file
      file.close()
      for tank in tanks:# if true then this is a corresponding tank
        for number in target:
          if(f"Tank {number}:" == tank.tName):
            if(len(correspondingTanks) == 0):
                correspondingTanks.append(tank)
            else:
              for i in range (len(correspondingTanks)):
                if(correspondingTanks[i].tName != f"Tank {number}"): #checking for duplicates
                  correspondingTanks.append(tank)
      return correspondingTanks
