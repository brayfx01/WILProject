import matplotlib.pyplot as plt

class ContainerGraph:
    def __init__(self,data):
        self.data = data
    def graph(self):
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
        plt.xlabel('Time')
        plt.ylabel('SOC/VOLUME')
        plt.legend()
        plt.title('Plot of Volume And SOC over time')
        plt.grid(True)
        plt.show()
