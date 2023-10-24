import socket
import signal
import sys
import time

HOST='127.0.0.1'
PORT=5000

def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	
	print(f"Client is connected {s}")
	
	binary_int_to_send = int(sys.argv[1], 2)

	binary_data = int.to_bytes(binary_int_to_send, length=4, byteorder='big')

	print(f"Sending command {bin(binary_int_to_send)}")
	s.sendall(binary_data)

if __name__ == "__main__":
	main()
