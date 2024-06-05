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
    return 'Hello from Flask! Available Data: Buoy, Spectral, Raw Spectral'

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

@app.route("/ww3/<model_date>/buoy/<buoy_id>")
@cross_origin()
def getWaveWatcher3Data(model_date, buoy_id):
    ww3_bull = f"https://ftpprd.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.{model_date}/00/wave/station/bulls.t00z/gfswave.{buoy_id}.bull"
    response = requests.get(ww3_bull)
    data = response.content.decode('utf-8')

    rows = data.split('\n')
    end_index = 100

    for i in range(7, len(rows)):
        if rows[i][1] == '+':
            end_index = i
            break

    rowsCleaned = rows[7:end_index]

    data = []

    def parse_row_parameters(row_parameters):
        row_data = {
            "day": int(row_parameters[1].strip().split()[0]),
            "hour": int(row_parameters[1].strip().split()[1]),
            "sWVHT": float(row_parameters[2].strip().split()[0]),
            "dataRows": int(row_parameters[2].strip().split()[1])
        }

        for i in range(1, row_data["dataRows"] + 1):
            swell_info = row_parameters[2 + i].strip().split()
            if len(swell_info) >= 3:
                if swell_info[0][0] == '*':
                    swell_info = swell_info[1:]
                    if len(swell_info) >= 3:
                        row_data[f"swell{i}Height"] = float(swell_info[0])
                        row_data[f"swell{i}Period"] = float(swell_info[1])
                        row_data[f"swell{i}Dir"] = int(swell_info[2])
                    else:
                        print(f"Warning: Insufficient data for swell {i} in row {row_data['day']} {row_data['hour']}")
            else:
                print(f"Warning: Insufficient data for swell {i} in row {row_data['day']} {row_data['hour']}")

        return row_data

    for row in rowsCleaned:
        parameters = row.split("|")
        parameters = [param.strip() for param in parameters]
        swellObject = parse_row_parameters(parameters)
        data.append(swellObject)

    return data

if __name__ == "main":
    app.run(debug=True)