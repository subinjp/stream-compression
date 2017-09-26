import timeit
import time
import gzip
import zlib
import os
import cProfile
import lzw




# this function deals with lzw algorithm.For this we used an external library called lzw
def lzw_algm(filename):
    start_time = time.time()

    try:
        outfilename = filename + '.lzw'
	comp_time = timeit.default_timer()
        file_bytes = lzw.readbytes(filename)
	tot_time = timeit.default_timer() - comp_time
        print("reading time",tot_time)
        compressed = lzw.compress(file_bytes)
	comp_time = timeit.default_timer()
        lzw.writebytes(outfilename, compressed)
	tot_time = timeit.default_timer() - comp_time
        print("writing time",tot_time)
    finally:
        print("")

if __name__ == "__main__":

    lzw_algm('../test_project1')
