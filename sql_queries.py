write_weather_data_json = """
INSERT INTO public.weather_forcast(
	data, service, type, api_call)
	VALUES (%s, %s, %s, %s)
	RETURNING id;
"""

write_hourly_forcast = """
INSERT INTO public.hourly_forcast(
	weather_forcast_id, "timestamp", temperature, feels_like_temp, pressure, humidity, clouds, visibility, wind_speed, wind_deg, wind_gust, weather_quick_display_id, uv_index, dew_point)
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

write_quick_display = """
INSERT INTO public.weather_quick_display(
	id, main, description, icon)
	VALUES (%s, %s, %s, %s);"""

get_quick_display = """
select * from public.weather_quick_display
where id = %s;"""

write_daily_forcast = """
INSERT INTO public.daily_forcast(
	sunrise, sunset, moonrise, moon_phase, day_temp, min_temp, max_temp, night_temp, eve_temp, morning_temp, pressure, humidity, dew_point, wind_speed, wind_deg, wind_gust, weather_quick_display_id, clouds, pop, uv_index, weather_forcast_id, time_stamp, moon_set)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""