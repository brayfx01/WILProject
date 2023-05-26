import Container 
class Cells:
    def __init__(self, name, numContainers, numBatteries):
        self.name = name
        self.containers = []
        for i in range(numContainers):
            cName = f"Container {i+1}:"
            container = Container.Container(name,cName, numBatteries)
            self.containers.append(container)
        self.numContainers = len(self.containers)