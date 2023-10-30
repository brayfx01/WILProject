class saveTanksContainers():
    def __init__(self, saveFile,onOffEfficency, RTE,tankMaxVolume,tankMinVolume,tankMaxSOC,tankMinSOC,containerMaxCharge,containerMinCharge,
                 generatedColumnName,loadColumnName, optimalTanks,optimalContainers):
        self.saveFile = saveFile
        self.onOffEfficency = onOffEfficency
        self.RTE = RTE
        self.tankMaxVolume = tankMaxVolume
        self.tankMinVolume = tankMinVolume
        self.tankMaxSOC = tankMaxSOC
        self.tankMinSOC = tankMinSOC
        self.containerMaxCharge = containerMaxCharge
        self.containerMinCharge = containerMinCharge
        self.generatedColumnName = generatedColumnName
        self.loadColumnName = loadColumnName
        self.optimalTanks = optimalTanks
        self.optimalContainers = optimalContainers
    # going through and writing all the initial conditions to the save file location and
    # the optimal tanks and optimal containers statistics
    def writeToFile(self):
        if self.saveFile:
                with open(self.saveFile, 'w') as file:
                    #writing the initial parameters
                    file.write("Container On Off Efficency = " + str(self.onOffEfficency) + "\n")
                    file.write("Round Trip Efficency = " + str(self.RTE) + "\n\n")
                    file.write("Tank Max Volume =  " + str(self.tankMaxVolume) + "\n")
                    file.write("Tank Min Volume =  " + str(self.tankMinVolume) + "\n\n")
                    file.write("Tank Max SOC =  " + str(self.tankMaxSOC) + "\n")
                    file.write("Tank Min SOC =  " + str(self.tankMinSOC) + "\n\n")
                    file.write("Container Max Charge = " + str(self.containerMaxCharge) + "\n")
                    file.write("Container Min Charge =  " + str(self.containerMinCharge) + "\n\n")

                    file.write("Generated Column Name:  " + str(self.generatedColumnName) + "\n")
                    file.write("Load Column Name:   " + str(self.loadColumnName) + "\n\n")
                    #writing in the tanks and ocntianer statistics
                    file.write("END\n")
                    file.write("Tanks:   " +  "\n")
                    for tank in self.optimalTanks:
                        file.write("    " + tank.tName + "\n")
                        file.write("        Volume = "+str(tank.volume) +  "\n")
                        file.write("            SOC = "+str(tank.soc) +  "\n")
                    file.write("\n\n")
                    file.write("Containers:\n")
                    for container in self.optimalContainers:
                       
                        file.write("    Charge = "+str(container.charge) +  "\n")
                        file.write("       Corresponding Tanks = [")

                        # stops placing a comma after the last tank in the corresponding tank array
                        length = len(container.correspondingTanks)
                        current = 0
                        for tank in container.correspondingTanks:
                            current +=1
                            if(current != length):
                                file.write(tank.tName + ", " )
                            else:
                                file.write(tank.tName)
                        file.write("]\n")
                   