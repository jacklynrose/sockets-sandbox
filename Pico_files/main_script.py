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
import re


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
password = 'pekeswaderpvy9v'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    # Initialize the flashing state
    flash_state = 0
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        # Flash the images or colors
        if flash_state == 0:
            UI.wifi_connect(0)
            flash_state = 1
        if flash_state == 1:
            UI.wifi_connect(1)
            flash_state = 0
        sleep(2)
    ip = wlan.ifconfig()[0]
    UI.wifi_connect(0)
    UI.wifi_connect(1)
    print(f'Connected on {ip}')
    return ip

def from_bytes_big(b):
    n = 0
    for x in b:
        n <<= 8
        n |= x
    return n

def is_matching_pattern(s, startswith):
    if s.startswith(startswith) and s[len(startswith):].isdigit() and len(s) == 7:
        return True
    else:
        return False
    
def roundup(x):
    return int(math.ceil(x / 100.0)) * 100


def socket_connect(HOST, PORT):
    global connection
    
    s = socket.socket()
    address = (HOST, PORT)
    s.bind(address)
    s.listen()
    print(f"Server is listening {s}")

    print("Waiting for connection...")
    
    weather_pattern = '77'
    temp_pattern = '7774'
    rain_pattern = '7772'
    clouds_pattern = '7763'
    status_pattern = '7773'
    
    client = s.accept()[0]
    UI.socket_connect(1)
    while True:
        data = client.recv(4)
        string_data = str(from_bytes_big(data))
        
        if data == b'\x00\x00\x00\x00':
            print("Closing signal received. Closing...")
            break
        
        if from_bytes_big(data)//740000==1:
            time = from_bytes_big(data)-740000
            UI.time(str(time))
            tempC, presPa, humRH = sensor.values()
            UI.indoor_temp(str(int(tempC)))
            
        if is_matching_pattern(string_data, weather_pattern):
            #checkfortemp
            if is_matching_pattern(string_data, temp_pattern):
                outdoor_temp = string_data[5:7]
                UI.outdoor_temp(outdoor_temp)
            
            #checkforweathericon
            if is_matching_pattern(string_data, status_pattern):
                weather_condition = from_bytes_big(data)-7773000
                print(weather_condition)
                if weather_condition < 800:
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
                
                print('status')
            
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
    