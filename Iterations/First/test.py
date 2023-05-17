import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import array as arr
import mplcursors
from dateutil import parser
from matplotlib.widgets import CheckButtons

path = 'Data/T1Day.csv'
pathTwo = "Data/ExpectedDay.csv"

df = pd.read_csv(path)
dft = pd.read_csv(pathTwo)
df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%d %m %Y %H:%M')

# Extract the hour, minute, and second components of the data generated
df['hour'] = df['Date/Time'].dt.hour
df['minute'] = df['Date/Time'].dt.minute
df['second'] = df['Date/Time'].dt.second

# This will generate the hourly sum and put it into an array with the first entry denoting the first hour
hourlySumOfGenerated = df.groupby(df['Date/Time'].dt.hour)['LV ActivePower (kW)'].sum()
hourlyLoad = dft.groupby(dft['time'].apply(lambda x: parser.parse(x).hour))['total load actual'].sum().to_numpy()

# Create line graphs for generated power and load
fig, ax = plt.subplots()
line1, = ax.plot(hourlySumOfGenerated.index, hourlySumOfGenerated.values, label='Generated Power')
line2, = ax.plot(hourlyLoad, label='Load')

# Add axis labels and title
ax.set_xlabel('Hour')
ax.set_ylabel('Power (kW)')
ax.set_title('Hourly Sum of Generated Power and Load')

# Use mplcursors to display information on mouse hover
cursor = mplcursors.cursor([line1, line2], hover=True)

# Dictionary to store annotations
annotations = {}

@cursor.connect("add")
def on_add(sel):
    hour = int(sel.target[0])
    generated_power = hourlySumOfGenerated[hour]
    load = hourlyLoad[hour]
    text = f"Hour: {hour}\nGenerated Power: {generated_power} kW\nLoad: {load} kW"
    annotation = sel.annotation
    if annotation is None:
        annotation = sel.annotate(text)
    else:
        annotation.set_text(text)
    annotations[sel.artist] = annotation

# Add checkbox to disable one of the lines
rax = plt.axes([0.02, 0.88, 0.1, 0.1])
check = CheckButtons(rax, ('Generated Power', 'Load'), (True, True))

def func(label):
    if label == 'Generated Power':
        line1.set_visible(not line1.get_visible())
        if not line1.get_visible():
            annotations.pop(line1, None)
    elif label == 'Load':
        line2.set_visible(not line2.get_visible())
        if not line2.get_visible():
            annotations.pop(line2, None)
    plt.draw()

check.on_clicked(func)

plt.legend()
plt.show()
