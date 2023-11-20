from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import socket

hostName = '192.168.0.121'
serverPort = 8080

def from_bytes_big(b):
    n = 0
    for x in b:
        n <<= 8
        n |= x
    return n

time.strftime('%H%M')
timestamp_h=time.localtime( time.time() )[3]*100
timestamp_m=time.localtime( time.time() )[4]
t = int(('t').encode('utf-8').hex())*10000
timestamp = int(timestamp_m+timestamp_h+t)
print(timestamp)
timestamp = int.to_bytes(timestamp, length=4, byteorder='big')
print(from_bytes_big(timestamp)//740000)
print(timestamp)
print(len(timestamp))
def webpage():
    with open('webpage.html', 'r') as f:
        html_string = f.read()
    return html_string.encode('utf-8')

#html = webpage()
#client.send(html)

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

ip = hostName
connection = open_socket(ip)
print('connected')
while True:
    client = connection.accept()[0]
    request = client.recv(1024)
    request = str(request)
    print(request)
    html = webpage()
    client.send(html)
    client.close()
