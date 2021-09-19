import googlemaps
import config
import requests
import json

key=config.api_key


url1 = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
origin = 'origins=29.755537,-95.372003&'
destination = 'destinations=29.716361,-95.409329'

full_url = url1+origin+destination+'&key='+key

payload={}
headers = {}
print(full_url)
response = requests.request("GET", full_url, headers=headers, data=payload)
print(json.loads(response.text))


def get_drive_time(param, param1):
    return None