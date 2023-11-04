# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        pathComponents = self.path.split('/')
        if pathComponents[1] == "SmartAC":
            self.wfile.write(bytes(json.dumps({ "path": self.path, "device": "SmartAC" }), "utf-8"))
        else:
            self.wfile.write(bytes(json.dumps({ "path": self.path, "device": "unknown" }), "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
