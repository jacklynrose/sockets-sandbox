import time

error_code = 44
e = int(('e').encode('utf-8').hex()) * 1000
signal = e + error_code
print(signal)
to_send = int(signal)
to_send = int.to_bytes(to_send, length=4, byteorder='big')

print(to_send)