import json

import pandas as pandas
import requests

from marra_query_maker import MarraQueryMaker


class Runner:
    current_weather = 'api.openweathermap.org/data/2.5/weather?q=Denver&appid={}'
    hourly_daily = 'https://api.openweathermap.org/data/2.5/onecall?lat=39.7392&lon=-104.9847&exclude=minutely&appid={}'

    api_call = None
    weather_json = None

    def __init__(self):
        self.query_maker = MarraQueryMaker.getInstance()
        try:
            self.query_maker.open_connection()

            self.weather_json = self.get_weather_json()
            print(self.weather_json)

            self.forcast_id = self.write_weather_data_json()
            self.write_all_hourly_data(self.weather_json['hourly'])
            self.write_all_daily_data(self.weather_json['daily'])
        finally:
            self.query_maker.close_connection()

    def write_weather_data_json(self):
        json_string = str(self.weather_json).replace("'", '"')
        return self.query_maker.write_weather_data_json(json_string, "Open Weather", "Hourly, Daily", self.api_call)

    def get_weather_json(self):
        api_key = self.get_api_key()
        self.api_call = self.hourly_daily.format(api_key)

        requests.session().close()
        r = requests.get(self.api_call)
        return r.json()

    def get_api_key(self):
        with open('/home/jaci/Projects/LocalData/api_keys.json') as myFile:
            data = myFile.read()
        api_keys = json.loads(data)
        return api_keys['open weather']

    def write_all_hourly_data(self, hourly_data):
        for data in hourly_data:
            time_stamp = pandas.to_datetime(self.get_data(data, 'dt'), unit='s')
            temperature = self.get_data(data, 'temp')
            feels_like_temperature = self.get_data(data, 'feels_like')
            pressure = self.get_data(data, 'pressure')
            humidity = self.get_data(data, 'humidity')
            dew_point = self.get_data(data, 'dew_point')
            uv_index = self.get_data(data, 'uvi')
            clouds = self.get_data(data, 'clouds')
            visibility = self.get_data(data, 'visibility')
            wind_speed = self.get_data(data, 'wind_speed')
            wind_deg = self.get_data(data, 'wind_deg')
            wind_gust = self.get_data(data, 'wind_gust')

            weather_quick_display = self.get_data(data, 'weather')
            weather_quick_display_id = self.write_weather_data(weather_quick_display[0])

            self.query_maker.write_hourly_forcast(self.forcast_id, time_stamp, temperature, feels_like_temperature, pressure, humidity, clouds, visibility, wind_speed, wind_deg, wind_gust, weather_quick_display_id, uv_index, dew_point)

    def write_all_daily_data(self, daily_data):
        for data in daily_data:
            time_stamp = pandas.to_datetime(self.get_data(data, 'dt'), unit='s')
            sunrise = pandas.to_datetime(self.get_data(data, 'sunrise'), unit='s')
            sunset = pandas.to_datetime(self.get_data(data, 'sunset'), unit='s')
            moonrise = pandas.to_datetime(self.get_data(data, 'moonrise'), unit='s')
            moonset = pandas.to_datetime(self.get_data(data, 'moonset'), unit='s')
            moon_phase = self.get_data(data, 'moon_phase')

            temperature_data = self.get_data(data, 'temp')
            day_temp = self.get_data(temperature_data, 'day')
            min_temp = self.get_data(temperature_data, 'min')
            max_temp = self.get_data(temperature_data, 'max')
            night_temp = self.get_data(temperature_data, 'night')
            eve_temp = self.get_data(temperature_data, 'eve')
            morning_temp = self.get_data(temperature_data, 'morn')

            pressure = self.get_data(data, 'pressure')
            humidity = self.get_data(data, 'humidity')
            dew_point = self.get_data(data, 'dew_point')
            wind_speed = self.get_data(data, 'wind_speed')
            wind_deg = self.get_data(data, 'wind_deg')
            wind_gust = self.get_data(data, 'wind_gust')
            clouds = self.get_data(data, 'clouds')
            pop = self.get_data(data, 'pop')
            uv_index = self.get_data(data, 'uvi')

            weather_quick_display = self.get_data(data, 'weather')
            weather_quick_display_id = self.write_weather_data(weather_quick_display[0])

            self.query_maker.write_daily_forcast(sunrise, sunset, moonrise, moon_phase, day_temp, min_temp, max_temp, night_temp, eve_temp, morning_temp, pressure, humidity, dew_point, wind_speed, wind_deg, wind_gust, weather_quick_display_id, clouds, pop, uv_index, self.forcast_id, time_stamp, moonset)

    def write_weather_data(self, weather_data):
        id = self.get_data(weather_data, 'id')

        is_in_database = self.query_maker.has_quick_display_data(id)
        if is_in_database:
            return id

        main = self.get_data(weather_data, 'main')
        description = self.get_data(weather_data, 'description')
        icon = self.get_data(weather_data, 'icon')
        self.query_maker.write_quick_display_data(id, main, description, icon)

        return id

    def get_data(self, data, index):
        try:
            return data[index]
        except:
            return None


if __name__ == '__main__':
    Runner()
