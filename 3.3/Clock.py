# this will work in steps of 5 minutes
# so we initialize what the step size is 
# from here we will update all the nessessary functions 
# within the software wich include 

"""
The battery On/off if they are on then they will loose charge 
Also will have a constant called time that wll reset to 0 upon 24 hours reached 


"""
class clock:
    def __init__(self,step, sections,tanks,energyHandler):
        self.step = step
        self.time = 0
        self.sections = sections
        self.tanks = tanks
        self.energyHandler = energyHandler
    def update(self,tanks,sections,fullEmpty):
        # we are going through and checking which containers are on 

        containerONCount = 0
        for section in sections: 
            for container in section.containers:
                if(container.onOffStatus == True):
                    containerONCount = containerONCount + 1
        # this will essentailly get how many containers are running and using energy this cycle and 
        #subtract from their usage
        drain = -containerONCount * sections[0].containers[0].onOffEfficency * self.step
        self.energyHandler.energyManagement(drain,tanks,fullEmpty)
        self.time = self.time + self.step