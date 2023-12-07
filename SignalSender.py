import time
import math
import pyowm
import re


class SignalSend:
    def __init__(self, socket, send_dict):
        self.socket = socket
        self.send_dict = send_dict
        self.key = '95f90ac291ec3d81fd76d7343aea3e72'
        self.place = 'Enmore, AU'

    def send(self, to_send):
        self.socket.sendall(to_send)

    def listen(self, ):
        data = self.socket.recv(4)
        binary_int = int.from_bytes(data, byteorder='big')
        if binary_int%64000 == 0:
            self.error(binary_int)
        else:
            print(f"Received data: {bin(binary_int)}")

    def error(self, signal):

        error_dict = {
            '1': 'cannot display two weather images',
            '2': 'cannot display one weather image',
            '3': 'cannot display time'
        }

        error_code = int(signal-64000)
        print(f'ERROR: {error_dict[str(error_code)]}')


    def set_power(self,
                  power_on=0,
                  power_off=0):
        if power_on == 1:
            signal = self.send_dict['power_on']

        if power_off == 1:
            signal = self.send_dict['power_off']

        print('sending power signal')
        print('signal')
        to_send = int(signal, 2)
        to_send = int.to_bytes(to_send, length=4, byteorder='big')
        self.send(to_send)
        self.listen()
        time.sleep(2)

    def set_states(self,
                   mode='auto',
                   temperature='24',
                   fan='0'):
        print('sending state_signal')

        key = f'{mode}_{math.floor(float(temperature))}_{fan}'
        signal = self.send_dict[key]
        to_send = int(signal, 2)
        to_send = int.to_bytes(to_send, length=4, byteorder='big')
        self.send(to_send)
        self.listen()
        time.sleep(3)

    def send_time(self):
        timestamp_h = time.localtime(time.time())[3] * 100
        timestamp_m = time.localtime(time.time())[4]
        t = int(('t').encode('utf-8').hex()) * 10000
        timestamp = int(timestamp_m + timestamp_h + t)
        timestamp = int.to_bytes(timestamp, length=4, byteorder='big')
        self.send(timestamp)
        self.listen()
        time.sleep(2)

    def send_weather(self):

        additions = [1000, 100000]
        threehf = self.get_weather()

        for element in threehf.keys():
            e = threehf[element]
            print(element)
            hex_l = 0
            letter = element[0]
            hex_l += int(('w').encode('utf-8').hex()) * additions[1]
            hex_l += int((letter).encode('utf-8').hex()) * additions[0]
            to_send = hex_l + e
            print(hex_l)
            to_send = int.to_bytes(to_send, length=4, byteorder='big')
            self.socket.sendall(to_send)
            data = self.socket.recv(4)
            binary_int = int.from_bytes(data, byteorder='big')
            print(f"Received data: {bin(binary_int)}")

            time.sleep(2)

        to_send = int.to_bytes(int(('fi').encode('utf-8').hex()), length=4, byteorder='big')
        self.send(to_send)
        self.listen()
        time.sleep(2)

    def send_states(self, new_state_dict, old_state):
        new_fan = new_state_dict['fan']
        new_mode = new_state_dict['mode']
        new_power = new_state_dict['power']
        new_temp = new_state_dict['temp']

        if new_fan != old_state['fan'] or new_mode != old_state['mode'] or new_temp != old_state['temp']:
            print('change_settings')
            settings_state = 1
        else:
            settings_state = 0

        if new_power != old_state['power']:
            print('change_power')
            if new_power == 'on':
                self.set_power(power_on=1)
                print('sending_states')
                self.set_states(new_mode, new_temp, new_fan)
            else:
                self.set_power(power_off=1)

        if settings_state == 1 and old_state['power'] == 'on':
            print('sending_states')
            self.set_states(new_mode, new_temp, new_fan)

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
