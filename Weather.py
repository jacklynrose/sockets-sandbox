import pyowm
import re

class Weather:
    def __init__(self):
        self.key = '95f90ac291ec3d81fd76d7343aea3e72'
        self.place = 'Enmore, AU'

    def get_weather(self):
        owm = pyowm.OWM(self.key)
        weather_mgr = owm.weather_manager()
        forecast = weather_mgr.forecast_at_place(self.place, '3h')

        weather = forecast.forecast.weathers[0]
        temp = int(weather.temp['feels_like']-273.15)
        status = weather.weather_code

        three_hour_forecast = {
            'temperature': temp,
            'status': status
        }

        return three_hour_forecast

