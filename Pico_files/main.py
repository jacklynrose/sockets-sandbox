from PiicoDev_SSD1306 import *
from PiicoDev_SSD1306 import PiicoDev_SSD1306
from PiicoDev_BME280 import PiicoDev_BME280
import network
import socket
from time import sleep
import machine
from machine import Pin
import struct
from UI_create import create_UI 
import os
import json
from adhoc_functions import *
from NECprotocol import NECProtocolEncoderDecoder as encoder
from ir_tx import Player

with open('weather.json', 'r') as f:
    weather = json.load(f)

weather_keys = weather.keys()
print(weather_keys)

global reconnect_attempts
global connected_socket

recieve_dict = LazyJSONLoader('LG_recieve_dict.json')
weather = LazyJSONLoader('weather.json')
IR_led = Pin(15, Pin.OUT)
display = create_PiicoDev_SSD1306(freq=400000)
display.fill(0)
sensor = PiicoDev_BME280()
prev_time = 0000
UI = create_UI(display, 'fonts.json', 'images.json')
UI.initialise()

port=5000
ssid = 'Optus_0732D1'
#ssid = 'Telstra35CE44'
password = 'pekeswaderpvy9v'
#password = 'pzepeyeq678rehzt'

ERROR_LOG_FILE = 'error_log.json'
MAX_RECONNECT_ATTEMPTS = 5
RECONNECT_WAIT_SECONDS = 5


def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    # Initialize the flashing state
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    UI.wifi_connect(1)
    print(f'Connected on {ip}')
    return ip

def check_time(data):
    if from_bytes_big(data)//740000==1:
        try:
            time = from_bytes_big(data)-740000
            UI.time(str(time))
            tempC, presPa, humRH = sensor.values()
            UI.indoor_temp(str(int(tempC)))
        except:
            UI.error(1)
            print('indoor temp error')

def check_weather(data):
    weather_pattern = '77'
    temp_pattern = '7774'
    rain_pattern = '7772'
    clouds_pattern = '7763'
    status_pattern = '7773'
    string_data = str(from_bytes_big(data))
    if is_matching_pattern(string_data, weather_pattern):
        #checkfortemp
        if is_matching_pattern(string_data, temp_pattern):
            outdoor_temp = string_data[5:7]
            UI.outdoor_temp(outdoor_temp)
        
        #checkforweathericon
        if is_matching_pattern(string_data, status_pattern):
            weather_condition = from_bytes_big(data)-7773000
            print(weather_condition)
            images = []
            if weather_condition < 800 and str(roundup(weather_condition)) in weather_keys:
                images = weather.get(str(roundup(weather_condition)))
            elif weather_condition in [800, 801, 802, 803, 804]:
                images = weather.get(str(weather_condition))
           
            if len(images)>1:
                try:
                    UI.weather_1(images[0])
                    UI.weather_2(images[1])
                except:
                    UI.error(1)
                    print('could not display images')
            else:
                try:
                    UI.weather_1(images[0])
                except:
                    UI.error(1)
                    print('could not display images')


def check_state_signal(data):
    string_data = bin(from_bytes_big(data))[2:]
    if is_matching_state(string_data, '1100010000001'):
        print('Match')
        IR_signal = recieve_dict.get(string_data)['signal']
        setting = recieve_dict.get(string_data)['setting']
        print(IR_signal)
        print(setting)
        if isinstance(setting, int):
            if setting == 0:
                print('turn power off')
                UI.AC_OFF()
            else:
                print('turn power on')
        else:
            mode = setting['mode']
            print(mode)
            temp = setting['temp']
            print(temp)
            fan = setting['fan']
            print(fan)
            UI.set_temp(temp)
            UI.mode(mode)
            UI.fan(fan)
            
        data = encoder().encode_data(IR_signal)
        Player(IR_led).play(data)

def socket_connect(HOST, PORT):
    global connection
    
    s = socket.socket()
    address = (HOST, PORT)
    s.bind(address)
    s.listen()
    print(f"Server is listening {s}")

    print("Waiting for connection...")
    
    client = s.accept()[0]
    UI.socket_connect(1)
    while True:
        reconnect_attempts = 0
        data = client.recv(4)
        
        
        if data == b'\x00\x00\x00\x00':
            print("Closing signal received. Closing...")
            break
        
        check_state_signal(data)
        
        check_time(data)     
        
        check_weather(data)
            
        binary_int = from_bytes_big(data)
        print(f"Received data: {bin(binary_int)}")
        sleep(2)
        
        test = struct.unpack('<h', data)[0]
        print(bin(test))
        #print(f"test: {bin(test)}")

        print(f"Echoing data: {bin(binary_int)}")
        client.sendall(data)
    

def log_error(error_message):
    error_data = {'error_message': error_message}

    try:
        with open(ERROR_LOG_FILE, 'a') as log_file:
            log_file.write(json.dumps(error_data) + '\n')
    except Exception as e:
        print(f"Error logging to file: {e}")


def main():
    reconnect_attempts = 0

    while reconnect_attempts < MAX_RECONNECT_ATTEMPTS:
        ip = connect()
        sleep(3)
        tempC, presPa, humRH = sensor.values()
        UI.indoor_temp(str(int(tempC)))
        try:
            socket_connect(ip, port)
        except (Exception) as e:
            reconnect_attempts += 1
            print(f"Socket connection lost. Reconnecting... Attempt {reconnect_attempts}/{MAX_RECONNECT_ATTEMPTS}")
            log_error(str(e))
            sleep(RECONNECT_WAIT_SECONDS)
        
  
if __name__ == "__main__":
    main()