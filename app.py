from flask import Flask, request, jsonify
from pandas import read_csv

app = Flask(__name__)

@app.route("/buoy/<buoy_id>")
def getBuoyData(buoy_id):
    BuoyInfo = read_csv(f"https://www.ndbc.noaa.gov/data/realtime2/{buoy_id}.txt")
    print(BuoyInfo)
    return {"id": buoy_id}

if __name__ == "main":
    app.run(debug=True)