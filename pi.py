import socket
import signal
import sys
import time

HOST = '192.168.0.148'
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

def signal_handler(signal, frame):
    global s
    with s:
        print("\nSending closing signal...")
        s.sendall(b'\x00\x00\x00\x00')
        sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main():
    global s

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print(f"Client is connected {s}")

    while True:
        states = set_states(settings_state=1, temperature='20')
        binary_int_to_send = int(states, 2)

        binary_data = int.to_bytes(binary_int_to_send, length=4, byteorder='big')

        print(f"Sending command {bin(binary_int_to_send)}")
        s.sendall(binary_data)

        data = s.recv(4)
        if data == b'\x00\x00\x00\x00':
            print("Closing signal received. Closing...")
            break

        binary_int = int.from_bytes(data, byteorder='big')
        print(f"Received data: {bin(binary_int)}")

        time.sleep(2)


if __name__ == "__main__":
    main()
