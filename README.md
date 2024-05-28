# NDBC Buoy Data
Flask API to parse NDBC buoy data by buoy id from CSV to JSON 

Deployed on PythonAnywhere, paid account for unrestricted external API access (NDBC, NCEP)

# Endpoints

/buoy/{buoy_id}:
Returns a given NDBC buoy dataset in JSON format

/buoy/{buoy_id}/spectral:
Returns a given NDBC buoy spectral summary dataset in JSON

/buoy/{buoy_id}/spectral/raw:
Returns a given NDBC buoy raw spectral dataset in JSON

/buoy/{buoy_id}/spectral/raw/pairs:
Returns a given NDBC buoys' most recent raw spectral dataset organized as wave energey and frequency pairs within a list

/ww3/buoy/{buoy_id}:
Returns Wave Watcher 3 data for a given NDBC buoy in .bull format
