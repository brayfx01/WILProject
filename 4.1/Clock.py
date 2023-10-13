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
    def update(self):
        # update time
        self.time = self.time + self.step
    def getTime(self):
        return self.time