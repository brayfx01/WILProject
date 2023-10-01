
class onOffDrain:
    def __init__(self,target,drain):
        self.target = target *( drain/100)
    def drain(self):
        return self.target