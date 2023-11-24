import socket
import signal
import sys
import time
from Weather import Weather
import requests

def set_states(power_state=0,
               settings_state=0,
               power_on=0,
               power_off=0,
               mode='auto',
               temperature='24',
               fan='0'):
    # set_values
    address = '10001000'
    crc = '0111'
    power_on_sig = '0000010011110100'
    power_off_sig = '1100000000000101'
    timer_settings = '00001'
    pos_13 = '0'

    mode_dict = {'position': (6, 8),
            'value': {
                'heat': '100',
                'auto': '011',
                'cool': '000'
            }
            }

    temperature_dict = {'position': (9, 12),
                   'value': {
                       '16': '0000',
                       '17': '0001',
                       '18': '0010',
                       '19': '0011',
                       '20': '0100',
                       '21': '0101',
                       '22': '0110',
                       '23': '0111',
                       '24': '1000',
                       '25': '1001',
                       '26': '1010',
                       '27': '1011',
                       '28': '1100',
                       '29': '1101',
                       '30': '1111'
                   }
                   }

    fan_dict = {'position': (14, 16),
           'value': {
               '0': '001',
               '1': '000',
               '2': '010',
               '4': '100'
           }
           }

    if power_state == 1:
        if power_on == 1:
            base_signal = power_on_sig
        if power_off == 1:
            base_signal = power_off_sig

    if settings_state == 1:
        mode_settings = mode_dict['value'][mode]
        temp_settings = temperature_dict['value'][temperature]
        fan_settings = fan_dict['value'][fan]
        base_signal = timer_settings+mode_settings+temp_settings+pos_13+fan_settings

    signal = address+base_signal+crc

    if len(signal) == 28:
        return signal
    else:
        return 'exception'

def send_states(new_state_dict, old_state):
    new_fan = new_state_dict['fan']
    new_mode = new_state_dict['mode']
    new_power = new_state_dict['power']
    new_temp = new_state_dict['temp']

    if new_fan != old_state['fan'] or new_mode != old_state['mode'] or new_temp != ['temp']:
        settings_state = 1
    else:
        settings_state = 0

    if new_power != old_state['power']:
        power_state = 1
    else:
        power_state = 0

    if new_power == 'on':
        power_on = 1
        power_off = 0
    else:
        power_on = 1
        power_off = 0

    states = set_states(power_state=power_state,
                        settings_state=settings_state,
                        power_on=power_on,
                        power_off=power_off,
                        mode=new_mode,
                        temperature=str(int(float(new_temp))),
                        fan=new_fan)

    to_send = int(states, 2)
    to_send = int.to_bytes(to_send, length=4, byteorder='big')

    print(to_send)

def check_state():
    try:
        response = requests.get('http://192.168.0.139:5050/get')  # Replace <your_server_address> with the actual address of your server
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching state: {e}")
        return None

old_state = {'fan': '1','mode': 'cool','power': 'off','swing': 'both','temp': '21'}

while True:
    if check_state() != old_state:
        new_state = check_state()
        print(old_state)
        print(new_state)
        send_states(new_state, old_state)
        old_state = new_state