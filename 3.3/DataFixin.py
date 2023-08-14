import pandas as pd
from datetime import datetime, timedelta

# Load original data
data = pd.read_excel('dataSets/GenAndLoadDay.xlsx')  # Replace 'your_dataset.csv' with the actual filename

# Convert 'Time (Hour-Ending)' column to datetime
data['Time (Hour-Ending)'] = pd.to_datetime(data['Time (Hour-Ending)'])

# Create a new DataFrame for 5-minute intervals
new_data = pd.DataFrame(columns=['Timestamp', 'Date', 'Load', 'WindGen', 'Difference'])

# Loop through original data
for index, row in data.iterrows():
    timestamp = row['Time (Hour-Ending)']
    date = row['Date']
    load = row['Load']
    wind_gen = row['WindGen']
    
    # Generate 5-minute intervals for each hour
    for minute in range(0, 60, 5):
        new_timestamp = timestamp + timedelta(minutes=minute)
        difference = wind_gen - load
        new_data = new_data.append({'Timestamp': new_timestamp, 'Date': date, 'Load': load, 'WindGen': wind_gen, 'Difference': difference}, ignore_index=True)

# Export data to Excel
new_data.to_excel('DataSets/new_data_with_difference.xlsx', index=False)
