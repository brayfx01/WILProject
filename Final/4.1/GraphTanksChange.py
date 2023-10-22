import matplotlib.pyplot as plt

class GraphTanksChange:
    def __init__(self,data):
        self.data = data
    def graph(self):
        """
        for individual tanks

        data = []
        for tank in self.data:
            if(tank[0] == "Tank: 12"):
                # this is the currentChargedcapacity
                data.append(tank[0])
        """
        print(self.data)
    
        data = self.data
        time = []
        value = 0
        for entry in data:
            time.append(value + 5)
            value += 5


        # Create a scatter plot or line plot
        plt.figure(figsize=(8, 6))
        plt.plot(time, self.data, label='Tank Volume', marker='o')
        #plt.plot(time, tankSoc, label='TankSoc', marker='s')
        plt.xlabel('Time(Minets)')
        plt.ylabel('Volume(MW)')
        plt.legend()
        plt.title('Plot of Volume And SOC over time')
        plt.grid(True)
        plt.show()
