import socket
import signal
import sys
import time
from Weather import Weather
import requests
import json
import math

with open('LG_send_dict.json', 'r') as f:
    send_dict = json.load(f)

server_url = 'http://192.168.0.139:5050'

w_forecast = Weather()

HOST = '192.168.0.148'
#HOST = '192.168.0.2'
PORT = 5000

def calculate_checksum(signal):
    # Check if the input signal is exactly 24 bits
    if len(signal) != 24:
        raise ValueError("Input signal must be 24 bits long")

    # Split the 24-bit signal into 4-bit groups
    groups = [signal[i:i+4] for i in range(0, len(signal), 4)]

    # Add the values of each 4-bit group
    checksum = sum(int(group, 2) for group in groups)

    # Ignore overflow by subtracting 32 if the sum is greater than or equal to 32
    checksum = checksum - (32 * (checksum // 32))

    # Convert the result to a 4-bit binary string
    checksum_binary = format(checksum, '04b')

    return checksum_binary

def set_power(power_on=0,
              power_off=0):


    if power_on == 1:
        signal = send_dict['power_on']

    if power_off == 1:
        signal = send_dict['power_off']

    print('sending power signal')
    print('signal')
    to_send = int(signal, 2)
    to_send = int.to_bytes(to_send, length=4, byteorder='big')
    send(s, to_send)
    listen(s)
    time.sleep(2)

def set_states(mode='auto',
               temperature='24',
               fan='0'):

    print('sending state_signal')

    key = f'{mode}_{math.floor(float(temperature))}_{fan}'
    signal = send_dict[key]
    to_send = int(signal, 2)
    to_send = int.to_bytes(to_send, length=4, byteorder='big')
    send(s, to_send)
    listen(s)
    time.sleep(3)

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
    settings_state = 0
    power_state = 0
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
            set_power(power_on=1)
            print('sending_states')
            set_states(new_mode, new_temp, new_fan)
        else:
            set_power(power_off=1)
            power_state = new_power


    if settings_state == 1 and old_state['power'] == 'on':
        print('sending_states')
        set_states(new_mode, new_temp, new_fan)


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
            time.sleep(1)
            if check_state() == new_state:
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
