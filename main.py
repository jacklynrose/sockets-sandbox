from PiicoDev_SSD1306 import *
import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
import struct
from display_bitmap import plot_image, remove_image

port=5000

display = create_PiicoDev_SSD1306()
ssid = 'Optus_0732D1'
password = 'pekeswaderpvy9v'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    # Initialize the flashing state
    display.fill(0)
    flash_state = 0
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        # Flash the images or colors
        if flash_state == 0:
            plot_image('wifi.txt', 0, 0, display)
            flash_state = 1
        if flash_state == 1:
            remove_image('wifi.txt', 0, 0, display)
            flash_state = 0
        sleep(2)
    ip = wlan.ifconfig()[0]
    remove_image('wifi.txt', 0, 0, display)
    plot_image('wifi.txt', 0, 0, display)
    print(f'Connected on {ip}')
    return ip

def from_bytes_big(b):
    n = 0
    for x in b:
        n <<= 8
        n |= x
    return n


def socket_connect(HOST, PORT):
    global connection
    
    s = socket.socket()
    address = (HOST, PORT)
    s.bind(address)
    s.listen()
    print(f"Server is listening {s}")

    print("Waiting for connection...")

    client = s.accept()[0]
    plot_image('network.txt', 15, 0, display)
    while True:
        data = client.recv(4)
        
        if data == b'\x00\x00\x00\x00':
            print("Closing signal received. Closing...")
            break
            
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
    socket_connect(ip, port)
except KeyboardInterrupt:
    machine.reset()
    