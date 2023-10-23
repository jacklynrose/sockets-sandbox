import socket
import signal
import sys
import time

HOST='127.0.0.1'
PORT=5000

def signal_handler(signal, frame):
	global s
	with s:
		print("\nSending closing signal...")
		s.sendall(b'\x00\x00\x00\x00')
		sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
	global s

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	
	print(f"Client is connected {s}")
	
	while True:
		binary_int_to_send = 0b00000001000100001010000011111111

		binary_data = int.to_bytes(binary_int_to_send, length=4, byteorder='big')

		print(f"Sending command {bin(binary_int_to_send)}")
		s.sendall(binary_data)

		data = s.recv(4)
		if data == b'\x00\x00\x00\x00':
			print("Closing signal received. Closing...")
			break

		binary_int = int.from_bytes(data, byteorder='big')
		print(f"Received data: {bin(binary_int)}")

		time.sleep(2)

if __name__ == "__main__":
	main()
