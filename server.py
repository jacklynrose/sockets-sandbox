# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json


hostName = '192.168.0.121'
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):

    def send_data_to_homebridge(self, data):
        print("Sending response")
        print(data)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(data, "utf-8"))

    def do_GET(self):
        pathComponents = self.path.split('/')
        if pathComponents[1] == "aircon":
            checkaction = pathComponents[2]
            if checkaction == "getcurrentheatercoolerstate":
                self.send_data_to_homebridge('pow=1&mode=3')
            elif checkaction == 'getcoolingtemperature':
                self.send_data_to_homebridge('getcool=22.0')
            elif checkaction == 'gettargetheatercoolerstate':
                self.send_data_to_homebridge('pow=1&mode=3')
            elif checkaction == 'settargetheatercoolerstate':
                self.send_data_to_homebridge('mode=3')
            elif checkaction == 'getactive':
                self.send_data_to_homebridge('pow=1')
            elif checkaction == 'setactive':
                self.send_data_to_homebridge('pow=1')
            elif checkaction == 'getcurrenttemperature':
                self.send_data_to_homebridge('temp=31.0')
            elif checkaction == 'setcoolingtemperature':
                self.send_data_to_homebridge('temp=31.0')

        else:
            self.wfile.write(bytes(json.dumps({ "path": self.path, "device": "unknown" }), "utf-8"))

if __name__ == "__main__":
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
