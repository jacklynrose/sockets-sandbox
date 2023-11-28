import socket
import signal
import sys
import time
from Weather import Weather
import requests
import json
from SignalSender import SignalSend

with open('LG_send_dict.json', 'r') as f:
    send_dict = json.load(f)

server_url = 'http://192.168.0.139:5050'
w_forecast = Weather()
HOST = '192.168.0.148'
PORT = 5000
MAX_RECONNECT_ATTEMPTS = 5
RECONNECT_WAIT_SECONDS = 30
ERROR_LOG_FILE = 'error_log.json'

def check_state():
    try:
        response = requests.get(
            'http://192.168.0.139:5050/get')  # Replace <your_server_address> with the actual address of your server
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching state: {e}")
        return None

def calculate_checksum(signal):
    # Check if the input signal is exactly 24 bits
    if len(signal) != 24:
        raise ValueError("Input signal must be 24 bits long")

    # Split the 24-bit signal into 4-bit groups
    groups = [signal[i:i + 4] for i in range(0, len(signal), 4)]

    # Add the values of each 4-bit group
    checksum = sum(int(group, 2) for group in groups)

    # Ignore overflow by subtracting 32 if the sum is greater than or equal to 32
    checksum = checksum - (32 * (checksum // 32))

    # Convert the result to a 4-bit binary string
    checksum_binary = format(checksum, '04b')

    return checksum_binary

def log_error(error_message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    error_data = {'timestamp': timestamp, 'error_message': error_message}

    try:
        with open(ERROR_LOG_FILE, 'a') as log_file:
            log_file.write(json.dumps(error_data) + '\n')
    except Exception as e:
        print(f"Error logging to file: {e}")

def signal_handler(s):
    with s:
        print("\nSending closing signal...")
        s.sendall(b'\x00\x00\x00\x00')
        sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main():
    reconnect_attempts = 0

    while reconnect_attempts < MAX_RECONNECT_ATTEMPTS:
        try:
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

            signalsend = SignalSend(s, send_dict, Weather)

            print(f"Client is connected {s}")
            reconnect_attempts = 0

            while True:
                sent_state = False
                sent_time = False
                sent_weather = False

                if check_state() != old_state:
                    new_state = check_state()
                    time.sleep(1)
                    if check_state() == new_state:
                        signalsend.send_states(new_state, old_state)
                        old_state = new_state
                        sent_state = True

                if abs(old_time_t - time.time()) >= 60:
                    signalsend.send_time()
                    old_time_t = time.time()
                    sent_time = True

                if abs(old_time_w - time.time()) >= 3600:
                    signalsend.send_weather()
                    old_time_w = time.time()
                    sent_weather = True

                if sent_state or sent_time or sent_weather:
                    continue
                else:
                    to_send = int(('xc').encode('utf-8').hex())
                    to_send = int.to_bytes(to_send, length=4, byteorder='big')
                    signalsend.send(to_send)
                    signalsend.listen()

                time.sleep(2)
        except (socket.error, ConnectionError) as e:
            reconnect_attempts += 1
            print(f"Socket connection lost. Reconnecting... Attempt {reconnect_attempts}/{MAX_RECONNECT_ATTEMPTS}")
            log_error(str(e))
            time.sleep(RECONNECT_WAIT_SECONDS)
            continue


if __name__ == "__main__":
    main()
