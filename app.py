from flask import Flask
from pandas import read_csv
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

if __name__ == "main":
    app.run(debug=True)