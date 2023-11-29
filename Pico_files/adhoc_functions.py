import math
import json

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

def is_matching_state(s, startswith):
    if s.startswith(startswith) and s[len(startswith):].isdigit() and len(s) == 21:
        return True
    else:
        return False

def roundup(x):
    return int(math.floor(x / 100.0)) * 100

class LazyJSONLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_handle = None

    def open(self):
        self.file_handle = open(self.file_path, 'r')

    def close(self):
        if self.file_handle is not None:
            self.file_handle.close()

    def get(self, key):
        try:
            self.open()
            for line in self.file_handle:
                data = json.loads(line)
                if key in data:
                    return data[key]
        finally:
            self.close()
            
    def keys(self):
        try:
            self.open()
            for line in self.file_handle:
                data = json.loads(line)
                yield data.keys()
        finally:
            self.close()

