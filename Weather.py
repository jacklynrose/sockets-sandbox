import pyowm

class  Weather:
    def __init__(self):
        self.key = '95f90ac291ec3d81fd76d7343aea3e72'
        self.place = 'Enmore, AU'

    def get_weather(self):
        owm = pyowm.OWM(self.key)
        weather_mgr = owm.weather_manager()
        forecast = weather_mgr.forecast_at_place(self.place, '3h')
        temp = []
        rain = []
        clouds = []
        for weather in forecast.forecast:
            temp.append(weather.temp)
            rain.append(weather.rain)
            clouds.append(weather.clouds)

        five_day_forecast = {
            'temperature' : temp,
            'rain': rain,
            'clouds': clouds
        }

        return five_day_forecast
