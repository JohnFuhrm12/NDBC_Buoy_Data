import requests

def getWaveWatcher3Data(model_date, buoy_id):
    import requests

    # Try cycles in descending order (00, 18, 12, 06)
    cycles = ["00", "18", "12", "06"]
    
    file_url = None
    raw_text = None

    for cycle in cycles:
        url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{model_date}/{cycle}/wave/station/bulls.t{cycle}z/gfswave.{buoy_id}.bull"

        res = requests.get(url)

        if res.status_code == 200 and len(res.text.strip()) > 0:
            file_url = url
            raw_text = res.text
            break

    if raw_text is None:
        return {"error": "No WW3 bulletin available for this buoy/date"}, 404

    rows = raw_text.split("\n")

    # Find end of bulletin (line starting with "+")
    end_index = None
    for i in range(7, len(rows)):
        if len(rows[i]) > 1 and rows[i][1] == "+":
            end_index = i
            break

    if end_index is None:
        end_index = len(rows)

    # Remove header rows (first 7 lines are metadata)
    data_rows = rows[7:end_index]

    output = []

    def parse_row_params(params):
        row_data = {}

        # Example params: ["", "18 03", "1.5 3", "0.7 12 210", ...]
        # DAY + HOUR
        try:
            day, hour = params[1].strip().split()
            row_data["day"] = int(day)
            row_data["hour"] = int(hour)
        except:
            return None

        # sWVHT + num swell rows
        try:
            sWVHT, dataRows = params[2].strip().split()
            row_data["sWVHT"] = float(sWVHT)
            row_data["dataRows"] = int(dataRows)
        except:
            return None

        # Parse swell rows safely
        swell_index = 1
        param_index = 3  # Swell rows start here

        while swell_index <= row_data["dataRows"]:
            if param_index >= len(params):
                break  # Missing row → stop safely

            raw = params[param_index].strip().split()

            # Skip "*" markers
            if raw and raw[0].startswith("*"):
                raw = raw[1:]

            if len(raw) >= 3:
                h = float(raw[0])
                p = float(raw[1])
                d = int(raw[2])

                row_data[f"swell{swell_index}Height"] = h
                row_data[f"swell{swell_index}Period"] = p
                row_data[f"swell{swell_index}Dir"] = d

            swell_index += 1
            param_index += 1

        return row_data

    # Parse each bulletin row
    for row in data_rows:
        params = [p.strip() for p in row.split("|")]
        parsed = parse_row_params(params)
        if parsed:
            output.append(parsed)

    return output


getWaveWatcher3Data("20251116", "51211")