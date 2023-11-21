import socket
import signal
import sys
import time
from Weather import Weather
import requests

server_url = 'http://192.168.0.139:5050'

w_forecast = Weather()

HOST = '192.168.0.148'
#HOST = '192.168.0.2'
PORT = 5000

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
    send_signal = False

    if power_state == 1:
        if power_on == 1:
            base_signal = power_on_sig
            send_signal = True

        if power_off == 1:
            base_signal = power_off_sig
            send_signal = False

        signal = address + base_signal + crc
        print('sending power signal')
        if len(signal) == 28:
            to_send = int(signal, 2)
            to_send = int.to_bytes(to_send, length=4, byteorder='big')
            send(s, to_send)
            listen(s)
            time.sleep(2)
        else:
            return 'exception'

    if settings_state == 1 and power_on==1:
        mode_settings = mode_dict['value'][mode]
        temp_settings = temperature_dict['value'][temperature]
        fan_settings = fan_dict['value'][fan]
        base_signal = timer_settings+mode_settings+temp_settings+pos_13+fan_settings

        signal = address+base_signal+crc
        print('settings signal')

        if len(signal) == 28:
            to_send = int(signal, 2)
            to_send = int.to_bytes(to_send, length=4, byteorder='big')
            send(s, to_send)
            listen(s)
            time.sleep(2)
        else:
            return 'exception'

    if power_on==1:
        print('power sent, resend signal')
        mode_settings = mode_dict['value'][mode]
        temp_settings = temperature_dict['value'][temperature]
        fan_settings = fan_dict['value'][fan]
        base_signal = timer_settings + mode_settings + temp_settings + pos_13 + fan_settings

        signal = address + base_signal + crc
        print(signal)

        if len(signal) == 28:
            to_send = int(signal, 2)
            to_send = int.to_bytes(to_send, length=4, byteorder='big')
            send(s, to_send)
            listen(s)
            time.sleep(2)
        else:
            return 'exception'


def send_time(s):
    timestamp_h = time.localtime(time.time())[3] * 100
    timestamp_m = time.localtime(time.time())[4]
    t = int(('t').encode('utf-8').hex()) * 10000
    timestamp = int(timestamp_m + timestamp_h + t)
    timestamp = int.to_bytes(timestamp, length=4, byteorder='big')
    send(s, timestamp)
    listen(s)
    time.sleep(2)

def send_weather(s):

    additions = [1000, 100000]
    threehf = w_forecast.get_weather()

    for element in threehf.keys():
        e = threehf[element]
        print(element)
        hex_l = 0
        letter = element[0]
        hex_l += int(('w').encode('utf-8').hex())*additions[1]
        hex_l += int((letter).encode('utf-8').hex())*additions[0]
        to_send = hex_l+e
        print(hex_l)
        to_send = int.to_bytes(to_send, length=4, byteorder='big')
        s.sendall(to_send)
        data = s.recv(4)
        binary_int = int.from_bytes(data, byteorder='big')
        print(f"Received data: {bin(binary_int)}")

        time.sleep(2)

    to_send = int.to_bytes(int(('fi').encode('utf-8').hex()), length=4, byteorder='big')
    s.sendall(to_send)

def signal_handler(signal, frame):
    global s
    with s:
        print("\nSending closing signal...")
        s.sendall(b'\x00\x00\x00\x00')
        sys.exit(0)

def send(s, to_send):
    s.sendall(to_send)

def listen(s):
    data = s.recv(4)
    binary_int = int.from_bytes(data, byteorder='big')
    print(f"Received data: {bin(binary_int)}")

def send_states(new_state_dict, old_state):
    new_fan = new_state_dict['fan']
    new_mode = new_state_dict['mode']
    new_power = new_state_dict['power']
    new_temp = new_state_dict['temp']
    old_fan = old_state['fan']
    old_mode = old_state['mode']
    old_temp = old_state['temp']

    if new_fan != old_state['fan'] or new_mode != old_state['mode'] or new_temp != old_state['temp']:
        print('change_settings')
        settings_state = 1
    else:
        settings_state = 0

    if new_power != old_state['power']:
        print('change_power')
        power_state = 1
    else:
        power_state = 0

    if new_power == 'on':
        power_on = 1
        power_off = 0
    else:
        power_on = 0
        power_off = 1

    set_states(power_state=power_state,
               settings_state=settings_state,
               power_on=power_on,
               power_off=power_off,
               mode=new_mode,
               temperature=str(int(float(new_temp))),
               fan=new_fan)



def check_state():
    try:
        response = requests.get('http://192.168.0.139:5050/get')  # Replace <your_server_address> with the actual address of your server
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching state: {e}")
        return None

signal.signal(signal.SIGINT, signal_handler)


def main():
    old_time_w = 0
    old_time_t = 0
    old_state = {'fan': '1',
                 'mode': 'cool',
                 'power': 'off',
                 'swing': 'both',
                 'temp': '21'}
    global s

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print(f"Client is connected {s}")

    while True:
        sent_state=False
        sent_time=False
        sent_weather=False

        if check_state() != old_state:
            new_state = check_state()
            send_states(new_state, old_state)
            old_state = new_state
            sent_state = True

        if abs(old_time_t-time.time()) >= 60:
            send_time(s)
            old_time_t = time.time()
            sent_time = True

        if abs(old_time_w-time.time()) >= 3600:
            send_weather(s)
            old_time_w = time.time()
            sent_weather = True

        if sent_state or sent_time or sent_weather:
            continue
        else:
            to_send = int(('xc').encode('utf-8').hex())
            to_send = int.to_bytes(to_send, length=4, byteorder='big')
            send(s, to_send)
            listen(s)

        time.sleep(2)


if __name__ == "__main__":
    main()
