import pandas as pd
import os

# Define the folder containing temperature data
temperature_folder = "C:\\temperature_data"

# Initialize a DataFrame to hold all the data
all_data = pd.DataFrame()

# Read and combine all CSV files
for filename in os.listdir(temperature_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(temperature_folder, filename)
        data = pd.read_csv(file_path)

        # Print the columns of the current file for debugging
        print(f"Columns in {filename}: {data.columns.tolist()}")
        
        # Reshape the DataFrame to long format
        data_melted = data.melt(id_vars=['STATION_NAME', 'STN_ID', 'LAT', 'LON'], 
                                 var_name='Month', 
                                 value_name='Temperature')
        
        # Add a Year column (extracted from the filename)
        year = filename.split('_')[2].split('.')[0]  # Extract year from the filename
        data_melted['Year'] = int(year)

        # Append to the main DataFrame
        all_data = pd.concat([all_data, data_melted], ignore_index=True)

# Check if all_data has been populated
if all_data.empty:
    print("No data has been loaded. Please check your CSV files.")
else:
    # Map month names to seasons
    seasons = {
        'January': 1, 'February': 1, 'March': 2, 
        'April': 2, 'May': 2, 'June': 3, 
        'July': 3, 'August': 3, 'September': 4, 
        'October': 4, 'November': 4, 'December': 1
    }
    all_data['Season'] = all_data['Month'].map(seasons)

    # Calculate average temperatures for each season 
    average_temp_per_season = all_data.groupby(['Year', 'Season'])['Temperature'].mean().reset_index()
    average_temp_per_season = average_temp_per_season.groupby('Season')['Temperature'].mean()

    # Save the average temperatures to "average_temp.txt"
    with open("average_temp.txt", "w") as f:
        for season, avg_temp in average_temp_per_season.items():
            f.write(f"Season {season}: {avg_temp:.2f}\n")

    # Find the station with the largest temperature range
    temperature_range = all_data.groupby('STATION_NAME')['Temperature'].agg(['max', 'min'])
    temperature_range['Range'] = temperature_range['max'] - temperature_range['min']
    largest_temp_range = temperature_range[temperature_range['Range'] == temperature_range['Range'].max()]

    # Save the largest temperature range station(s) to "largest_temp_range_station.txt"
    with open("largest_temp_range_station.txt", "w") as f:
        for station in largest_temp_range.index:
            f.write(f"Station: {station} - Range: {largest_temp_range.loc[station]['Range']:.2f}\n")

    # Find the warmest and coolest station
    warmest_station = temperature_range[temperature_range['max'] == temperature_range['max'].max()]
    coolest_station = temperature_range[temperature_range['min'] == temperature_range['min'].min()]

    # Save the warmest and coolest station(s) to "warmest_and_coolest_station.txt"
    with open("warmest_and_coolest_station.txt", "w") as f:
        for station in warmest_station.index:
            f.write(f"Warmest Station: {station} - Max Temp: {warmest_station.loc[station]['max']:.2f}\n")
        for station in coolest_station.index:
            f.write(f"Coolest Station: {station} - Min Temp: {coolest_station.loc[station]['min']:.2f}\n")

    print("Analysis complete. Results saved to files.")