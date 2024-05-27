import requests

# BASE = "https://johnfuhrm12.pythonanywhere.com/"
BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE  + "buoy/51201/spectral")
print(response.json())