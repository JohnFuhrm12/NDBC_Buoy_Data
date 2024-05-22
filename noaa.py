import pandas as pd
 

buoy_csv = "https://www.ndbc.noaa.gov/data/realtime2/51201.txt"
buoy_data_df = pd.read_csv(buoy_csv, sep="\s+")

json_path = "./51201.json"
json_output = buoy_data_df.to_json(json_path, indent=1, orient="records")

selected_json = buoy_data_df.to_json(orient='records', lines=True)

#print(selected_json)
