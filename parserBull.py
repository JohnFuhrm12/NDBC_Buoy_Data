import requests

def getWaveWatcher3Data(buoy_id):
    ww3_bull = f"https://polar.ncep.noaa.gov/waves/WEB/multi_1.latest_run/plots/multi_1.{buoy_id}.bull"
    response = requests.get(ww3_bull)
    data = response.content.decode('utf-8')

    rows = data.split('\n')
    rowsCleaned = rows[7:25]

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
            row_data[f"swell{i}Height"] = float(swell_info[0])
            row_data[f"swell{i}Period"] = float(swell_info[1])
            row_data[f"swell{i}Dir"] = int(swell_info[2])

        return row_data
    
    for row in rowsCleaned:
        parameters = row.split("|")
        parameters = [param.strip() for param in parameters]
        swellObject = parse_row_parameters(parameters)
        data.append(swellObject)

    print(data)
    return data


getWaveWatcher3Data("51201")