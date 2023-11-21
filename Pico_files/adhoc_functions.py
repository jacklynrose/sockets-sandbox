import math

def from_bytes_big(b):
    n = 0
    for x in b:
        n <<= 8
        n |= x
    return n

def is_matching_pattern(s, startswith):
    if s.startswith(startswith) and s[len(startswith):].isdigit() and len(s) == 7:
        return True
    else:
        return False
    
def state_signal_match(s):
    address = '10001000'
    crc = '0111'
    if s.startswith(address) and s[len(address):].isdigit() and crc in s:
        return True
    else:
        return False
    
def off_match(s):
    address = '10001000'
    crc = '0111'
    if s.startswith(address) and s[len(address):].isdigit() and crc in s:
        return True
    else:
        return False
    
def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

def temp_dict():
    temperature_dict = {'position': (9, 12),
                   'value': {
                       '0000':'16',
                       '0001':'17',
                       '0010':'18',
                       '0011':'19',
                       '0100':'20',
                       '0101':'21',
                       '0110':'22',
                       '0111':'23',
                       '1000':'24',
                       '1001':'25',
                       '1010':'26',
                       '1011':'27',
                       '1100':'28',
                       '1101':'29',
                       '1111':'30'
                   }
                   }
    return temperature_dict

def mode_dict():
    mode_dict = {'position': (6, 8),
                'value': {
                    '100':'heat',
                    '011':'auto',
                    '001':'dehumidify',
                    '000':'cool'
                }
                }
    return mode_dict

def fan_dict():
    fan_dict = {'position': (14, 16),
               'value': {
                   '001':0,
                   '000':1,
                   '010':2
               }
               }
    return fan_dict
