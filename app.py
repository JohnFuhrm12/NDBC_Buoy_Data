from flask import Flask
from pandas import read_csv

app = Flask(__name__)

@app.route("/buoy/<buoy_id>")
def getBuoyData(buoy_id):
    buoy_csv = f"https://www.ndbc.noaa.gov/data/realtime2/{buoy_id}.txt"
    buoy_data_df = read_csv(buoy_csv, delim_whitespace=True)
    json_output = buoy_data_df.to_json(indent=1, orient="records")
    return json_output

if __name__ == "main":
    app.run(debug=True)