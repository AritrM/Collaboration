import requests
import json
import datetime
from latlong import api_key,get_lalong




place = input("Location: ")
latlong = get_lalong(place)

if latlong:
    lat,long = latlong
    print(f"{lat},{long}")
    
lalong = f"{lat}, {long}"
time  =  "[2025]-[10]-[22]T[11]:[34]:[00]"
url = f"https://api.pirateweather.net/forecast/{api_key}/{lalong}"

query = {
    "lang" : "en",
    "units" : "si",
    "exclude": "minutely,hourly"
}

response = requests.get(url,params = query)

ans = response.json()

ans_r = json.dumps(ans, indent = 2) #string
ans_nr = json.loads(ans_r)  #list
print(type(ans_r))

# print(ans_r)

tplace = []
ans_nr['currently']["time"] = datetime.datetime.fromtimestamp(ans_nr['currently']["time"])
for i in range(8):
    ans_nr['daily']['data'][i]["time"] = datetime.datetime.fromtimestamp(ans_nr['daily']['data'][i]["time"])

print(ans_nr)
read = str()
k = input("[Enter to close.]")