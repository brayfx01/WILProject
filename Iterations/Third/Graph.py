import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import array as arr
import mplcursors
from dateutil import parser
class Graph:
    def __init__(self, pathOne, pathTwo):
        self.pathOne = pathOne
        self.pathTwo = pathTwo
    def GraphGeneratedLoadAndDifference(self):
        path = self.pathOne
        pathTwo = self.pathTwo
        df = pd.read_csv(path)
        dft = pd.read_csv(pathTwo)
        df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%d %m %Y %H:%M')
        # Extract the hour, minute, and second components of the data generated
        df['hour'] = df['Date/Time'].dt.hour
        df['minute'] = df['Date/Time'].dt.minute
        df['second'] = df['Date/Time'].dt.second

        # This will generate the hourly sum and put it into an array with the first entry denoting the firs hour
        hourlySumOfGenerated = df.groupby(df['Date/Time'].dt.hour)['LV ActivePower (kW)'].sum()
        hourlyLoad = dft['total load actual'].to_numpy()
        # Create x and y arrays for generated power line plot
        hours = hourlySumOfGenerated.index
        sums = hourlySumOfGenerated.values

        # Plot line graph
        generatedLine = plt.plot(hours, sums, label='Generated Power')
        # Add labels and title

        difference = np.zeros(24, dtype=float)
                # now just creating an array of their differences to be able to determine where we need to store and where we need to grab from
        for i in range(hourlySumOfGenerated.size):
            difference[i]  = hourlySumOfGenerated[i]-hourlyLoad[i]
            
        # Create a line plot of the differences
        hours = range(24)
        differenceLine=plt.plot(hours, difference, label='Hourly Difference')

        # Add labels and title
        plt.xlabel('Hour')
        plt.ylabel('Hourly Difference (kW)')
        plt.title('Hourly Difference between Generated Power and Load')

        plt.xlabel('Hour')
        plt.ylabel('Hourly sum of LV ActivePower (kW)')
        plt.title('Hourly Sum of Generated Power')


        # Create x and y arrays for load line plot for load
        hours = range(24)
        sums = hourlyLoad

        # Plot load line graph
        loadLine = plt.plot(hours, sums, label='Hourly Load')

        # Add labels and title
        plt.xlabel('Hour')
        plt.ylabel('Hourly load (kW)')
        plt.title('Hourly Load')

        # Add legend
        plt.legend()

        # Add annotations to the generated power line
        cursorGen = mplcursors.cursor(generatedLine, hover=True)
        cursorGen.connect(
            "add", lambda sel: sel.annotation.set_text(f"Hour: {sel.target[0]}, Generated: {sel.target[1]:.2f} kW") or sel.annotation.set_color(generatedLine[0].get_color())
        )

        # Add annotations to the load line
        cursorLoad = mplcursors.cursor(loadLine, hover=True)
        cursorLoad.connect(
            "add", lambda sel: sel.annotation.set_text(f"Hour: {sel.target[0]}, Load: {sel.target[1]:.2f} kW") or sel.annotation.set_color(loadLine[0].get_color())
        )
        # Add annotations to the load line
        cursorDiff = mplcursors.cursor(differenceLine, hover=True)
        cursorDiff.connect(
            "add", lambda sel: sel.annotation.set_text(f"Hour: {sel.target[0]}, Difference: {sel.target[1]:.2f} kW")

        )

        # Display plot
        plt.show()
