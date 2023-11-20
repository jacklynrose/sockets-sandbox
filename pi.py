import socket
import signal
import sys
import time
from Weather import Weather

w_forecast = Weather()

#HOST = '192.168.0.148'
HOST = '192.168.0.2'
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
                'heating': '100',
                'auto': '011',
                'dehumidify': '001',
                'cooling': '000'
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
               '2': '000',
               '3': '010',
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

def send_states(power_state=0,
               settings_state=0,
               power_on=0,
               power_off=0,
               mode='auto',
               temperature='24',
               fan='0'):
    states = set_states(power_state=power_state,
               settings_state=settings_state,
               power_on=power_on,
               power_off=power_off,
               mode=mode,
               temperature=temperature,
               fan=fan)
    to_send = int(states, 2)
    to_send = int.to_bytes(to_send, length=4, byteorder='big')
    send(s, to_send)
    listen(s)
    time.sleep(2)

def check_state():
    ###go check UI for something
    return None

signal.signal(signal.SIGINT, signal_handler)


def main():
    old_time_w = 0
    old_time_t = 0
    old_state = None
    global s

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print(f"Client is connected {s}")

    while True:
        sent_state=False
        sent_time=False
        sent_weather=False

        if set_states(settings_state=1, power_on=0,  temperature='20', fan = '2') != old_state:
            send_states(settings_state=1, power_on=0,  temperature='20', fan = '2')
            old_state = set_states(settings_state=1, power_on=0,  temperature='20', fan = '2')
            print(old_state)
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
