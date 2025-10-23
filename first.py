import requests
#pip install requests
import json

import time
import datetime
api_key = "VGH2EXmyclRgyevMXbNcvtDEuZBvV2l4"
lalong = "22.43, 88.28"
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
heyyyy hloooo


