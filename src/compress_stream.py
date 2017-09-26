#!/usr/bin/env python3
from __future__ import print_function
import io
import zlib
import sys
import lzma
import datetime
import struct
import time
from threading import Thread
from threading import Lock
from sys import argv
ESC = 0x1A
main_buffer = io.BytesIO()
mutex= Lock()
flag = 0

USAGE='''
we used python3 to write this script
USAGE Example: nc x|tee a.bin|./compress_stream.py optional_timeout|tee b.bin|./decompress_stream.py >c.bin
'''

def read_data(header,packettype,bits,ignore):
    '''
    Helper function to read through remaining bytes within a packet
    bits-remaning bytes to read
    '''
    buffer = []
    #reading remaining bytes in the packet and remove escape bytes if not needed
    while bits > 0:
        next_byte=sys.stdin.buffer.read(1)
        it=iter(next_byte)
        value=next(it)
        if value == ESC:
            buffer.append(value)
            extrabyte=sys.stdin.buffer.read(1)
            it=iter(extrabyte)
            value=next(it)
            buffer.append(value)
            bits -=1
        else:
            bits -= 1
            buffer.append(value)

    if not ignore:
        data=bytes([header]+[packettype]+buffer)
        return data

#algorithm to compress the data
def deflate(contents):
    dat =zlib.compress(contents)
    size =len(dat)
    s=struct.pack("i",size)
    sys.stdout.buffer.write(s)
    sys.stdout.buffer.write(dat)
    sys.stdout.buffer.flush()

def main():
    no_error = True
    reset_timer = True
    while no_error:
        '''
        check first two bytes of packet
        rbr -remaining bytes to read from each packet
        '''

        two_bytes= sys.stdin.buffer.read(2)
        if len(two_bytes)==0:
            break
        #iterate over first two bytes of the packet
        it = iter(two_bytes)
        header =next(it)
        if header!=ESC:
            raise Exception("Error expected <esc>, but got header", header)
        packettype = next(it)

        #considering only the packets of type 2 and 3,else we drop the packets
        if packettype == ord('2'):
            rbr=14
            drop= False
            data=read_data(header,packettype,rbr,drop)
        elif packettype == ord('3'):
            rbr=21
            drop= False
            data=read_data(header,packettype,rbr,drop)
        else:
            rbr=21
            drop= True
            read_data(header,packettype,rbr,drop)

        #add to buffer only the packets of type 2 and 3
        if not drop:
            mutex.acquire()
            main_buffer.write(data)
            mutex.release()

#calling deflate function at every 950 milliseconds
def call_deflate():
    no_error = True
    reset_timer = True
    while no_error == True:
        if reset_timer == True:
            start_time=datetime.datetime.now()
            reset_timer = False
        current_time=datetime.datetime.now()
        diff_time=current_time-start_time
        if diff_time.microseconds >= 950000:
            if not mutex.locked():
                mutex.acquire()
                contents = main_buffer.getvalue()
                if len(contents) == 0:
                    continue
                deflate(contents)
                reset_timer=True
                main_buffer.truncate(0)
                main_buffer.seek(0)
                mutex.release()



if __name__ == '__main__':
    t1 = Thread(target =  main)
    t1.start()
    t = Thread(target = call_deflate)
    t.start()


