import json

# set_values
address = '10001000'
power_on_sig = '0000010011110100'
power_off_sig = '1100000000000101'
timer_settings = '00001'
pos_13 = '0'

mode_dict = {
            'heat': '100',
            'auto': '011',
            'cool': '000'
        }

temperature_dict = {
                   '16': '0000',
                   '17': '0001',
                   '18': '0010',
                   '19': '0011',
                   '20': '0100',
                   '21': '0101',
                   '22': '0110',
                   '23': '0111',
                   '24': '1000',
                   '25': '1001',
                   '26': '1010',
                   '27': '1011',
                   '28': '1100',
                   '29': '1101',
                   '30': '1111'
               }

fan_dict = {'0': '001',
           '1': '000',
           '2': '010',
           '4': '100'}

binary_dict = {
    'address':'10001000',
    'timer_settings':'00001',
    'power_on':'0000010011110100',
    'power_off':'1100000000000101',
    'pos_13':'0',
    'states':{
        'mode':mode_dict,
        'temperature':temperature_dict,
        'fan':fan_dict
    }
}

def calculate_checksum(signal):
    # Check if the input signal is exactly 24 bits
    if len(signal) != 24:
        raise ValueError("Input signal must be 24 bits long")

    # Split the 24-bit signal into 4-bit groups
    groups = [signal[i:i+4] for i in range(0, len(signal), 4)]

    # Add the values of each 4-bit group
    checksum = sum(int(group, 2) for group in groups)

    # Ignore overflow by subtracting 32 if the sum is greater than or equal to 32
    checksum = checksum - (32 * (checksum // 32))

    # Convert the result to a 4-bit binary string
    checksum_binary = format(checksum, '04b')

    return checksum_binary

count = 2
address='10001000'
timer_settings='00001'
id = bin(int(('bs').encode('utf-8').hex()))[2:]
print(id)

send_signal_dict = {}
recieve_signal_dict = {}
power_on = address + '0000010011110100' + calculate_checksum(address + '0000010011110100')
power_off = address + '1100000000000101' + calculate_checksum(address + '1100000000000101' )

recieve_signal_dict[id+'00000001'] = {
    'signal':power_on,
    'setting':1
}
recieve_signal_dict[id+'00000000'] = {
    'signal':power_off,
    'setting':0
}
send_signal_dict['power_on'] = id+'00000001'
send_signal_dict['power_off'] = id+'00000000'
zereos = '00000000'
for m, key_mode in enumerate(mode_dict.keys()):
    value_mode = mode_dict[key_mode]
    for t, key_temp in enumerate(temperature_dict.keys()):
        value_temp = temperature_dict[key_temp]
        for f, key_fan in enumerate(fan_dict.keys()):
            value_fan = fan_dict[key_fan]
            new_key_send = bin(count)[2:]
            if len(new_key_send) != 8:
                new_key_send = zereos[:8-len(new_key_send)]+new_key_send

            new_key_send = id + new_key_send
            count += 1
            if len(new_key_send) != 21:
                print(len(new_key_send))
            signal = address + timer_settings + value_mode + value_temp + pos_13 + value_fan
            signal = signal+calculate_checksum(signal)
            recieve_signal_dict[new_key_send] = {
                'signal':signal,
                'setting':{
                    'mode': value_mode,
                    'temp': value_temp,
                    'fan': value_fan
                }
            }
            send_signal_dict[f'{key_mode}_{key_temp}_{key_fan}'] = new_key_send


with open('LG_send_dict.json', 'w') as f:
    json.dump(send_signal_dict, f)

with open('LG_recieve_dict.json', 'w') as f:
    json.dump(recieve_signal_dict, f)