from flask import Flask
from pandas import read_csv
import csv
import json
import requests
from io import StringIO
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def hello_world():
    return 'Hello from Flask!'

@app.route('/test')
@cross_origin()
def test():
    return 'Test Successful!'

@app.route("/buoy/<buoy_id>")
@cross_origin()
def getBuoyData(buoy_id):
    buoy_csv = f"https://www.ndbc.noaa.gov/data/realtime2/{buoy_id}.txt"
    buoy_data_df = read_csv(buoy_csv, delim_whitespace=True)
    json_output = buoy_data_df.to_json(indent=1, orient="records")
    return json_output

@app.route("/buoy/<buoy_id>/spectral")
@cross_origin()
def getSpectralData(buoy_id):
    buoy_csv = f"https://www.ndbc.noaa.gov/data/realtime2/{buoy_id}.spec"
    buoy_data_df = read_csv(buoy_csv, delim_whitespace=True)
    json_output = buoy_data_df.to_json(indent=1, orient="records")
    return json_output

@app.route("/buoy/<buoy_id>/spectral/raw")
@cross_origin()
def getSpectralDataRaw(buoy_id):
    buoy_csv = f"https://www.ndbc.noaa.gov/data/realtime2/{buoy_id}.data_spec"
    buoy_data_df = read_csv(buoy_csv, delim_whitespace=True)
    json_output = buoy_data_df.to_json(indent=1, orient="records")
    return json_output

@app.route("/buoy/<buoy_id>/spectral/raw/pairs")
@cross_origin()
def getSpectralDataRawPairs(buoy_id):
    buoy_csv = f"https://www.ndbc.noaa.gov/data/realtime2/{buoy_id}.data_spec"

    def csv_to_json(csv_data):
        data = []
        csv_buffer = StringIO(csv_data)
        csv_reader = csv.DictReader(csv_buffer)
        row = next(csv_reader, None)
        if row:
            data.append(row)
            json_data = json.dumps(data, indent=4)
            return json_data
        else:
            return None

    def getSpectralDataRaw():
        response = requests.get(buoy_csv)
        if response.status_code == 200:
            json_data = csv_to_json(response.text)
            return json_data
        else:
            return None
        
    json_data = getSpectralDataRaw()
    if json_data:
        data_list = json.loads(json_data)
        spectral_data_str = list(data_list[0].values())[0]
        pairs = spectral_data_str.split()[6:]
        cleaned_freq = [float(freq.strip('()')) for freq in pairs[1::2]]
        result = [{"spec": float(pairs[i]), "freq": cleaned_freq[i//2]} for i in range(0, len(pairs), 2)]
        return result

@app.route("/ww3/buoy/<buoy_id>")
@cross_origin()
def getWaveWatcher3Data(buoy_id):
    ww3_bull = f"https://polar.ncep.noaa.gov/waves/WEB/multi_1.latest_run/plots/multi_1.{buoy_id}.bull"
    print(ww3_bull)

if __name__ == "main":
    app.run(debug=True)