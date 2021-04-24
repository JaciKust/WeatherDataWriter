import json
import requests

from marra_query_maker import MarraQueryMaker


class Runner:
    current_weather = 'api.openweathermap.org/data/2.5/weather?q=Denver&appid={}'
    hourly_daily = 'https://api.openweathermap.org/data/2.5/onecall?lat=39.7392&lon=-104.9847&exclude=minutely&appid={}'

    api_call = None
    weather_json = None

    def __init__(self):
        self.weather_json = self.get_weather_json()
        print(self.weather_json)

        self.write_to_marra()

    def write_to_marra(self):
        query_maker = MarraQueryMaker.getInstance()

        try:
            json_string = str(self.weather_json).replace("'", '"')
            query_maker.write_weather_data_json(json_string, "Open Weather", "Hourly, Daily", self.api_call)
        finally:
            query_maker.close_connection()

    def get_weather_json(self):
        api_key = self.get_api_key()
        self.api_call = self.hourly_daily.format(api_key)

        r = requests.get(self.api_call)
        return r.json()

    def get_api_key(self):
        with open('/home/jaci/Projects/LocalData/api_keys.json') as myFile:
            data = myFile.read()
        api_keys = json.loads(data)
        return api_keys['open weather']


if __name__ == '__main__':
    Runner()
