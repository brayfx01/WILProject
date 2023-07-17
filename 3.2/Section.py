 
from Containers import container 
import re
from Tank import Tank
  # create section and containers      
class Section:
    def __init__(self, sName,numberOfContainers,onOffEfficency,charge,tanks):
        self.sName = sName
        self.containers = []
        for i in range(numberOfContainers):
            self.containers.append(container(self.sName,f"Container {i + 1}", onOffEfficency,charge,self.getCorrespondingTanks(tanks,sName,f"Container {i + 1}")))
   
   
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
          if(f"Tank {number}" == tank.tName):
            if(len(correspondingTanks) == 0):
                correspondingTanks.append(tank)
            else:
              for i in range (len(correspondingTanks)):
                if(correspondingTanks[i].tName != f"Tank {number}"): #checking for duplicates
                  correspondingTanks.append(tank)
      return correspondingTanks
'''
t = []
t.append(Tank("Tank 1", 100, 50))
t.append(Tank("Tank 2", 100 , 50))
t.append(Tank("Tank 3", 100, 50))

s =  Section("Section 1",2, 85,2,t)
st = Section("Section 2",2,85,2,t)
for container in s.containers:
  print(container.cName)
  for tank in container.correspondingTanks:
    print("   ",tank.tName)
for container in st.containers:
  print(container.cName)
  for tank in container.correspondingTanks:
    print("   ",tank.tName)
'''