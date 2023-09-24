import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import HourLocator, DateFormatter

# Read data from the Excel file
excel_file_path = 'DataSets/new_data_with_difference.xlsx'
df = pd.read_excel(excel_file_path)

# Convert 'Timestamp' column to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Create the plot
plt.figure(figsize=(12, 6))
plt.plot(df['Timestamp'], df['Load'], label='Load')
plt.plot(df['Timestamp'], df['WindGen'], label='WindGen')
plt.plot(df['Timestamp'], df['Difference'], label='Difference')

# Configure x-axis ticks to show only the hours
plt.gca().xaxis.set_major_locator(HourLocator(interval=1))
plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))

plt.xlabel('Time')
plt.ylabel('Values')
plt.title('Load, WindGen, and Difference Over Time')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()
