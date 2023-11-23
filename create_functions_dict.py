import json
with open('LG_send_dict.json', 'r') as f:
    send_dict = json.load(f)
with open('LG_recieve_dict.json', 'r') as f:
    recieve_dict = json.load(f)

id = '1100010000001'
def set_power(power_on=0,
              power_off=0):


    if power_on == 1:
        signal = send_dict['power_on']

    if power_off == 1:
        signal = send_dict['power_on']

    print('sending power signal')
    print('signal')
    to_send = int(signal, 2)
    to_send = int.to_bytes(to_send, length=4, byteorder='big')
    return(to_send)
    #send(s, to_send)
    #listen(s)
    #time.sleep(3)

def set_states(mode='auto',
               temperature='24',
               fan='0'):

    print('sending state_signal')

    key = f'{mode}_{temperature}_{fan}'
    signal = send_dict[key]
    to_send = int(signal, 2)
    to_send = int.to_bytes(to_send, length=4, byteorder='big')
    return(to_send)
    #send(s, to_send)
    #listen(s)
    #time.sleep(3)



signal = set_states()
def from_bytes_big(b):
    n = 0
    for x in b:
        n <<= 8
        n |= x
    return n

def is_matching_pattern(s, startswith):
    if s.startswith(startswith) and s[len(startswith):].isdigit() and len(s) == 21:
        return True
    else:
        return False
def check_state_signal(data):
    string_data = bin(from_bytes_big(data))[2:]
    print(string_data)
    if is_matching_pattern(string_data, id):
        IR_signal = recieve_dict[string_data]['signal']
        setting = recieve_dict[string_data]['setting']
        print(IR_signal)
        if setting == 1:
            print('turn power on')
        elif setting == 0:
            print('turn power off')
        else:
            mode = setting['mode']
            temp = setting['temp']
            fan = setting['fan']
            print(f'{mode}, {temp}, {fan}')



check_state_signal(signal)