import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates  # Import mdates for HourLocator and DateFormatter
import tkinter as tk
def graph():
    # Read data from the Excel file
    excel_file_path = 'DataSets/new_data_with_difference.xlsx'
    df = pd.read_excel(excel_file_path)

    # Convert 'Timestamp' column to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Create a Tkinter window
    root = tk.Tk()
    root.title('Load, WindGen, and Difference Over Time')

    # Create a Matplotlib Figure
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the data
    ax.plot(df['Timestamp'], df['Load'], label='Load')
    ax.plot(df['Timestamp'], df['WindGen'], label='WindGen')
    ax.plot(df['Timestamp'], df['Difference'], label='Difference')

    # Configure x-axis ticks to show only the hours
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Use mdates.HourLocator
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Use mdates.DateFormatter

    ax.set_xlabel('Time',labelpad= 10)
    ax.set_ylabel('Values',labelpad=-10)
    ax.set_title('Load, WindGen, and Difference Over Time')
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)

    # Create a FigureCanvasTkAgg widget
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    # Run the Tkinter main loop
    root.mainloop()
graph()