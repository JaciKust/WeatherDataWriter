import json

import requests

class Runner:
    current_weather = 'api.openweathermap.org/data/2.5/weather?q=Denver&appid={}'
    hourly_daily = 'https://api.openweathermap.org/data/2.5/onecall?lat=39.7392&lon=-104.9847&exclude=minutely&appid={}'

    def __init__(self):
        weather = self.get_weather()
        print(weather)

    def get_weather(self):
        api_key = self.get_api_key()
        url = self.hourly_daily.format(api_key)
        r = requests.get(url)
        return r.json()

    def get_api_key(self):
        with open('/home/jaci/Projects/LocalData/api_keys.json') as myFile:
            data = myFile.read()
        api_keys = json.loads(data)
        return api_keys['open weather']


if __name__ == '__main__':
    Runner()
