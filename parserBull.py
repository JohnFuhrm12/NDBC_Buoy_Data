import requests

def getWaveWatcher3Data(model_date, buoy_id):
    ww3_bull = f"https://ftpprd.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.{model_date}/00/wave/station/bulls.t00z/gfswave.{buoy_id}.bull"
    # ww3_bull = f"https://polar.ncep.noaa.gov/waves/WEB/multi_1.latest_run/plots/multi_1.{buoy_id}.bull"
    response = requests.get(ww3_bull)
    data = response.content.decode('utf-8')

    ## 00 after model date indicates hour of model data, can also be 06, 12, and 18

    rows = data.split('\n')
    rowsCleaned = rows[7:160] # Start at row 7 to remove header, end at row 160 to give 7 days

    data = []

    def parse_row_parameters(row_parameters):
        # Remove whitespace and convert the array into an object
        row_data = {
            "day": int(row_parameters[1].strip().split()[0]),  # Extract day from the second parameter
            "hour": int(row_parameters[1].strip().split()[1]),  # Extract hour from the second parameter
            "sWVHT": float(row_parameters[2].strip().split()[0]),  # Extract significant wave height
            "dataRows": int(row_parameters[2].strip().split()[1])  # Extract number of swell data rows
        }

        # Iterate over swell data rows and extract swell information
        for i in range(1, row_data["dataRows"] + 1):
            swell_info = row_parameters[2 + i].strip().split()
            if swell_info[0][0] == '*':
                swell_info = swell_info[1:]
            if len(swell_info) >= 3:  # Check if there are enough items in the list
                row_data[f"swell{i}Height"] = float(swell_info[0])
                row_data[f"swell{i}Period"] = float(swell_info[1])
                row_data[f"swell{i}Dir"] = int(swell_info[2])
            else:

                print(f"Warning: Insufficient data for swell {i} in row {row_data['day']} {row_data['hour']}")

        return row_data
    
    for row in rowsCleaned:
        parameters = row.split("|")
        parameters = [param.strip() for param in parameters]
        swellObject = parse_row_parameters(parameters)
        data.append(swellObject)

    print(data)
    return data


getWaveWatcher3Data("20240530", "51201")