import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "buoy/51201")
print(response.json())