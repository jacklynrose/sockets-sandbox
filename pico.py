import socket
import signal
import sys
import time

HOST='127.0.0.1'
PORT=5000

def is_connection_closed(conn) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = conn.recv(4, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except Exception as e:
        return False
    return False

def is_valid_command(command):
	command_length = len(bin(command)[2:])

	if command_length < 24:
		print(f"Invalid command: {bin(command)}")
		return False
	else:
		return True
	

def get_command_header(command):
	# move all bits except the first 4 to the right
	# only the first 4 bits will be returned

	if not is_valid_command(command):
		return 0

	return command >> len(bin(command)[2:]) - 4

def get_command_data(command):
	if not is_valid_command(command):
		return 0
	
	header_and_data = command >> len(bin(command)[2:]) - 24
	return header_and_data & int('0' * 4 + '1' * 20, 2)

def signal_handler(signal, frame):
	global connection
	try:
		with connection:
			print("\nSending closing signal...")
			connection.sendall(b'\x00\x00\x00\x00')
	except:
		print("\nNo client was connected")
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
	global connection

	# This is just here to show how the above functions work
	# It does nothing
	command_example = 0b1000110011001100110011000011111
	print(f"Header: {bin(get_command_header(command_example))}")
	print(f"Data: {bin(get_command_data(command_example))}")

	# Invalid example
	get_command_header(0b11)

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()

		print(f"Server is listening {s}")

		while True:
			print("Waiting for connection...")

			connection, addr = s.accept()

			with connection:
				print(f"Connected {addr}")
				while True:
					try:
						if is_connection_closed(connection):
							print('Client disconnected')
							connection.close()
							break

						data = connection.recv(4)
						
						if data == b'\x00\x00\x00\x00':
							print("Closing signal received. Closing...")
							connection.close()
							break

						binary_int = int.from_bytes(data, byteorder='big')

						print(f"Received data: {bin(binary_int)}")

						# Commands (fake examples obviously)
						# Emit: 1111 / 15
						# - Next 20 bits are data to emit
						# Request Pico Status: 1010 / 10
						# - Next 20 bits are ignored
						# Enter power saving mode: 1001 / 9
						# - Next 20 bits are ignored
						command_header = get_command_header(binary_int)

						if command_header == 15:
							print(f"Emitting  data {bin(get_command_data(binary_int))}")
						elif command_header == 10:
							print('Fetching status')
							print('Returning status to client')
						elif command_header == 9:
							print('Entering power saving mode')
						else:
							print('Command not found')

						print(f"Echoing data: {bin(binary_int)}")
						connection.sendall(data)
					except:
						print('Client disconnected')
						connection.close()
						break
			

if __name__ == "__main__":
	main()
