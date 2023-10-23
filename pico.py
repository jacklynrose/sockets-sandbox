import socket
import signal
import sys
import time

HOST='127.0.0.1'
PORT=5000

def signal_handler(signal, frame):
	global connection
	with connection:
		print("\nSending closing signal...")
		connection.sendall(b'\x00\x00\x00\x00')
		sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
	global connection

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()

		print(f"Server is listening {s}")

		print("Waiting for connection...")

		connection, addr = s.accept()

		with connection:
			print(f"Connected {addr}")
			while True:
				data = connection.recv(4)
				
				if data == b'\x00\x00\x00\x00':
					print("Closing signal received. Closing...")
					break

				binary_int = int.from_bytes(data, byteorder='big')
				print(f"Received data: {bin(binary_int)}")
				time.sleep(2)

				print(f"Echoing data: {bin(binary_int)}")
				connection.sendall(data)

if __name__ == "__main__":
	main()
