import Battery
import sys
class Container:
    def __init__(self, sName,name, numBatteries):
        self.name = name# contianer name
        self.sName = sName# Section Name
        self.batteries = []
        numBatteries = self.getBatteryCount(self.sName, self.name) # this determines how many batteries in each containe
        for i in range(numBatteries):
            #Now we want anouther fucntion to calcluate the info of the Batteres 
            # it will take in the section name container name and battery name gerenated dynamically
            bName = f"Battery {i + 1} :"
            battery = Battery.Battery(sName,name,bName,0,0)
            self.batteries.append(battery)
      # gets the number of battereis in the correspoinding container
    def getBatteryCount(self,name, dName):
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
    