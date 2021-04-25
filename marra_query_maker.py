import json
import logging

import psycopg2

import sql_queries


class MarraQueryMaker:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if MarraQueryMaker.__instance is None:
            MarraQueryMaker()
        return MarraQueryMaker.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if MarraQueryMaker.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            with open('/home/jaci/Projects/LocalData/databases.json') as myFile:
                data = myFile.read()
            databases = json.loads(data)
            marra = databases["marra"]

            self.marra_database_host = marra['host']
            self.marra_database_name = marra['name']
            self.marra_database_user = marra['username']
            self.marra_database_pass = marra['password']
            self.connection = None

            MarraQueryMaker.__instance = self

    def __del__(self):
        self.close_connection()

    def open_connection(self):
        if self.connection is not None:
            return
        try:
            self.connection = psycopg2.connect(
                dbname=self.marra_database_name,
                host=self.marra_database_host,
                user=self.marra_database_user,
                password=self.marra_database_pass
            )
            self.connection.autocommit = True
        except Exception as e:
            logging.warning("Could not connect to Marra.")
            self.close_connection()

    def close_connection(self):
        try:
            if self.connection is not None:
                self.connection.close()
        except:
            pass
        finally:
            self.connection = None

    def write_weather_data_json(self, json_data, service, call_type, api_call):
        inserted_id = None
        if self.connection is None:
            self.open_connection()

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_queries.write_weather_data_json,
                           (json_data, service, call_type, api_call))
            inserted_id = cursor.fetchone()[0]
            cursor.close()

        except Exception as e:
            logging.warning("Could not write temperature / humidity reading to Marra")

        return inserted_id

    def has_quick_display_data(self, id):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql_queries.get_quick_display, [id])
            try:
                result = cursor.fetchone()
            except:
                return False

            return result is not None

        except Exception as e:
            logging.warning('could not get quick display data from database')
            return False
        finally:
            cursor.close()

    def write_quick_display_data(self, id, main, description, icon):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql_queries.write_quick_display, (id, main, description, icon))
        except Exception as e:
            logging.warning('could not write quick display data.')
        finally:
            cursor.close()

    def write_hourly_forcast(self, weather_forcast_id, timestamp, temperature, feels_like_temp, pressure, humidity, clouds, visibility, wind_speed, wind_deg, wind_gust, weather_quick_display_id, uv_index, dew_point):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql_queries.write_hourly_forcast, (weather_forcast_id, timestamp, temperature, feels_like_temp, pressure, humidity, clouds, visibility, wind_speed, wind_deg, wind_gust, weather_quick_display_id, uv_index, dew_point))
        except Exception as e:
            logging.warning('Could not write hourly forcast')
        finally:
            cursor.close()

    def write_daily_forcast(self, sunrise, sunset, moonrise, moon_phase, day_temp, min_temp, max_temp, night_temp, eve_temp, morning_temp, pressure, humidity, dew_point, wind_speed, wind_deg, wind_gust, weather_quick_display_id, clouds, pop, uv_index, weather_forcast_id, time_stamp, moon_set):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql_queries.write_daily_forcast, (sunrise, sunset, moonrise, moon_phase, day_temp, min_temp, max_temp, night_temp, eve_temp, morning_temp, pressure, humidity, dew_point, wind_speed, wind_deg, wind_gust, weather_quick_display_id, clouds, pop, uv_index, weather_forcast_id, time_stamp, moon_set))
        except Exception as e:
            logging.warning('Could not write to daily forcast.')
        finally:
            cursor.close()

