import requests

BASE = "https://johnfuhrm12.pythonanywhere.com/"
#BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE  + "ww3/20240604/buoy/51211")
print(response.json())