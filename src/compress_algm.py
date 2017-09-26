from __future__ import print_function

import zipfile
# import lzma
import gzip
import bz2
import os
import bz2file
import time
import huffman_algm


# deflate algorithm.
# To add compression, the zlib module is required. If zlib is available, you can set the compression mode for individual files or for the archive as a whole using zipfile.ZIP_DEFLATED.
#  The default compression mode is zipfile.ZIP_STORED.
def deflated(file_name):
    # the beginning time of the compression algorithm.
    start_time = time.time()
    try:
        import zlib
        compression = zipfile.ZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED

    modes = {zipfile.ZIP_DEFLATED: 'deflated',
             zipfile.ZIP_STORED: 'stored',
             }
    print(file_name)
    print("creating zipfile")
    outfilename = file_name + '.zip'
    zf = zipfile.ZipFile(outfilename, mode='w')
    try:
        print('adding peds_project.bin with compression mode', modes[compression])
        zf.write(file_name, compress_type=compression)
    finally:
        print('closing')
        zf.close()
    comprsn_details(file_name, outfilename, start_time)


# lzma algorithm which uses pylzma algorithm.To use this library install the library using easy_install lzma
# you can find the library information here: https://pypi.python.org/pypi/pylzma
def lzma_algm(file_name):
    start_time = time.time()
    import pylzma
    outfilename = file_name + '.lzma'
    try:
        with open(file_name, 'rb') as f, open(outfilename, 'wb') as out:
            out.write(pylzma.compress(f.read()))
    finally:
        comprsn_details(file_name, outfilename, start_time)


# algorithm which uses deflate algorithm.Here we can give the compression level we need.
# The compression level is directly proportional to compression ration but inversily proportional to the execution time
def gzip_algm(filename, level):
    start_time = time.time()
    # open the file which need to compress in read mode
    data = open(filename, 'rb')

    outfilename = filename + '.gz'
    # open the file to which the compressed data to store in write mode
    output = gzip.open(outfilename, 'wb', level)
    try:
        output.write(bytes(data.read()))
    finally:
        output.close()
        comprsn_details(filename, outfilename, start_time)


# burrows wheeler algorithm which uses bz2file library.Install it using pip install bz2file
def burrows_wheeler(filename, level):
    start_time = time.time()
    outfilename = filename + '.bz'
    try:
        with open(filename, 'rb') as f, bz2file.open(outfilename, 'wb', level) as out:
            out.write(bz2.compress(bytes(f.read())))
    finally:
        print("closing")
        comprsn_details(filename, outfilename, start_time)


# this function deals with lzw algorithm.For this we used an external library called lzw
def lzw_algm(filename):
    start_time = time.time()
    from src import lzw
    try:
        outfilename = filename + '.lzw'
        file_bytes = lzw.readbytes(filename)
        compressed = lzw.compress(file_bytes)
        lzw.writebytes(outfilename, compressed)
    finally:
        comprsn_details(filename, outfilename, start_time)


# this function provides huffman coding algorithm which uses the external library huffman_algm
def huffman_coding(filename):
    start_time = time.time()
    outfilename = filename + '.hf'
    enc = huffman_algm.Compress(filename)
    enc.write(outfilename)
    comprsn_details(filename, outfilename, start_time)


# decompression for deflate algorithm.It can decompress only the zip files.
def decomp_deflated(filename):
    import zipfile
    # here you need to enter the originalfilename that you have compressed
    archieve = raw_input('Enter the file name in the archieve: ')
    zf = zipfile.ZipFile(filename)
    # the filename to which the data to be decompressed
    outfilename = filename + '.decomp'
    try:
        data = zf.read(archieve)
        with open(outfilename, 'wb') as out:
            out.write(data)

    finally:
        print("decompression is over")


# decompression for lzma algorithm.It can decompress only the lzma files.
def decom_lzma_algm(file_name):
    import pylzma
    outfilename = file_name + '.decomp'
    try:
        with open(file_name, 'rb') as f, open(outfilename, 'wb') as out:
            out.write(pylzma.decompress(f.read()))
    finally:
        out.close()


# decompression for gzip files.It can decompress only the gzip files.
def decomp_gzip_algm(filename):
    data = open(filename, 'rb')

    outfilename = filename + '.decomp'
    output = gzip.open(outfilename, 'wb')
    try:
        output.write(bytes(data.read()))
    finally:
        output.close()


# decompression for burrows wheeler algorithm.It can decompress only the bzip files.
def decomp_burrows_wheeler(filename):
    start_time = time.time()
    outfilename = filename + '.bz'
    try:
        with open(filename, 'rb') as f, bz2file.open(outfilename, 'wb') as out:
            out.write(bz2.decompress(bytes(f.read())))
    finally:
        out.close()


# decompression for lzw algorithm.It can decompress only the lzw files.
def decomp_lzw_algm(filename):
    start_time = time.time()
    from src import lzw
    try:
        outfilename = filename + '.decom'
        file_bytes = lzw.readbytes(filename)
        uncompressed = lzw.decompress(file_bytes)
        lzw.writebytes(outfilename, uncompressed)

    finally:
        print("decompression is over")


# huffman coding decompression.It can decompress only the compressed files which uses huffman coding
def decomp_huffman_coding(filename):
    start_time = time.time()
    outfilename = filename + '.hf'
    dec = huffman_algm.Decompress(filename)
    dec.write_file(outfilename)

# the function which let you to choose the file to compress and which algorithm you want to use for compressing the file
def compress():
    filename = raw_input('Enter the file name to compress: ')
    # Enter the compression algm to use
    case = int(input(
        'Enter the compression algorithm : \n 1:deflated \n 2:lzma \t \n 3:gzip  \n 4:burrows_wheeler \n 5:lzw \t \n 6:huffman coding \t'))
    if case == 1:
        deflated(filename)
    elif case == 2:
        lzma_algm(filename)
    elif case == 3:
        level = int(input('Enter compression level'))
        gzip_algm(filename, level)
    elif case == 4:
        level = int(input('Enter compression level'))
        burrows_wheeler(filename, level)
    elif case == 5:
        lzw_algm(filename)
    elif case == 6:
        huffman_coding(filename)

# the function which let you to choose the file to decompress and which algorithm you want to use for decompressing the file
def decompress():
    filename = raw_input('Enter the file name to decompress: ')
    case = int(input(
        'Enter the decompression algorithm : \n 1:deflated \n 2:lzma \t \n 3:gzip  \n 4:burrows_wheeler \n 5:lzw \t \n 6:huffman coding \t'))
    if case == 1:
        decomp_deflated(filename)
    elif case == 2:
        decom_lzma_algm(filename)
    elif case == 3:
        decomp_gzip_algm(filename)
    elif case == 4:
        decomp_burrows_wheeler(filename)
    elif case == 5:
        decomp_lzw_algm(filename)
    elif case == 6:
        decomp_huffman_coding(filename)

# the function which gives compression details such as original size,compressed size,compression ratio and compression time
def comprsn_details(filename, outfilename, start_time):
    print(outfilename, 'contains', os.stat(outfilename).st_size, 'bytes of compressed data')
    os.system('file -b --mime %s' % outfilename)
    orginalSize = float(os.stat(filename).st_size)
    compressSize = float(os.stat(outfilename).st_size)
    print("compression ratio", orginalSize / compressSize)
    seconds = time.time() - start_time
    minute, second = divmod(seconds, 60)
    print("compression time= %02d:%02d" % (minute, second))


if __name__ == "__main__":
    option = int(input('Do you want to compress or decompress: \t 1:compress \t 2: decompress'))
    if option == 1:
        compress()
    elif option == 2:
        decompress()
