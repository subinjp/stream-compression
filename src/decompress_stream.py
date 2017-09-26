#!/usr/bin/env python3
from __future__ import print_function
import io
import zlib
import sys
import lzma
import struct
# we used python3 to write this script
output = io.BytesIO()

#algorithm to decompress the streaming data
def decompress(contents):
    dat =zlib.decompress(contents)
    sys.stdout.buffer.write(dat)
    sys.stdout.buffer.flush()

if __name__ == '__main__':
    #os.remove('a.bin')
    no_error=True
    decom=False
    while no_error:
        #first take the size of the buffer
        bin_size=sys.stdin.buffer.read(4)
        if len(bin_size) ==0:
            break
        size=struct.unpack("i",bin_size)[0]
        data=sys.stdin.buffer.read(size)
        if len(data) == 0:
           break
        decompress(data)
