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


IR_led = Pin(15, Pin.OUT)

display = create_PiicoDev_SSD1306(freq=400000)
display.fill(0)

sensor = PiicoDev_BME280()
prev_time = 0000

# Opening JSON file
with open('images.json', 'r') as openfile:
    images_dict = json.load(openfile)
    
with open('text_19px.json', 'r') as openfile:
    text_19 = json.load(openfile)
    
with open('text_9px.json', 'r') as openfile:
    text_9 = json.load(openfile)

with open('weather.json', 'r') as openfile:
    weather = json.load(openfile)

fonts = {}
fonts[9] = text_9
fonts[19] = text_19

UI = create_UI(display, fonts, images_dict)

UI.initialise()

port=5000
ssid = 'Optus_0732D1'
#ssid = 'Telstra35CE44'
password = 'pekeswaderpvy9v'
#password = 'pzepeyeq678rehzt'


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
            if weather_condition < 800 and weather_condition in weather.keys():
                images = weather[str(roundup(weather_condition))]
            elif weather_condition in [800, 801, 802, 803, 804]:
                images = weather[str(weather_condition)]
           
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
    print(string_data)
    off_int = int('1000100011000000000001010001')
    on_int = int('1000100000000100111101000111')
    int_string = int(string_data)
    if state_signal_match(string_data):
        data = encoder().encode_data(string_data)
        Player(IR_led).play(data)
        time.sleep(1)
        Player(IR_led).play(data)
    if off_int == int_string:
        print('power_off')
        UI.AC_OFF()
    else:
        if on_int == int_string:
            print('power_on')
        elif state_signal_match(string_data):
            temp = temp_dict()['value'][string_data[16:20]]
            m = mode_dict()['value'][string_data[13:16]]
            f = fan_dict()['value'][string_data[21:24]]
            UI.set_temp(str(temp))
            UI.mode(m)
            UI.fan(f)
            return None

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
    


try:
    ip = connect()
    sleep(3)
    tempC, presPa, humRH = sensor.values()
    UI.indoor_temp(str(int(tempC)))
    socket_connect(ip, port)
except KeyboardInterrupt:
    machine.reset()
    