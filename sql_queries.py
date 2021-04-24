write_weather_data_json = """
INSERT INTO public.weather_forcast(
	data, service, type, api_call)
	VALUES (%s, %s, %s, %s)
	RETURNING id;
"""