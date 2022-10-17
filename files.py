from struct import pack, unpack
import shutil

def read_to_set(path):
    with open(path, "r") as file:
        return set(line.strip() for line in file if line.strip() != "")

def rmtree(path):
    shutil.rmtree(path, ignore_errors=True)

def unpack_string(file):
    buffer = file.read(1)
    if buffer == '':
        return None
    s_len, = unpack("B", buffer)
    return unpack(str(s_len) + "s", file.read(s_len))[0].decode()

def unpack_int(file):
    buffer = file.read(4)
    if buffer == '':
        return None
    return unpack("I", buffer)[0]

def pack_string(s):
    b = s.encode()
    return pack("B", len(b)) + b

def pack_int(n):
    return pack("I", n)
