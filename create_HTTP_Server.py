from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import socket

hostName = '192.168.0.121'
serverPort = 8080

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
