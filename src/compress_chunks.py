import lzma
import bz2
import gzip
import os
import matplotlib.pyplot as plt
#install matplot library for graph plotting
#the path where you can see the original chunks
files = os.listdir('../files_required/chunks_stripped')
ratio = list()
myorder = list()
org = list()

#the function which compresses 100 different chunks of each group.
def compression_algm(case):
    for filename in sorted(files):  # 'file' is a builtin type, 'name' is a less-ambiguous variable name.

        infilename = os.path.join('../files_required/chunks_stripped/', filename)
        #lzma algorithm
        if case == 1:
            outfilename = os.path.join('../files_required/chunks_lzmacomp/', filename + "." + 'lzma')
            try:
                with open(infilename, 'rb') as f, open(outfilename, 'wb') as out:
                    out.write(lzma.compress(bytes(f.read())))
            finally:
                out.close()
                compression_ratio(infilename, outfilename)
        #gzip(deflate) algorithm
        elif case == 2:
            outfilename = os.path.join('../files_required/chunks_gzipcompressed/', filename + "." + 'gzip')
            try:
                with open(infilename, 'rb') as f, gzip.open(outfilename, 'wb') as out:
                    out.write(bytes(f.read()))
            finally:
                out.close()
                compression_ratio(infilename, outfilename)

#this function finds the compression ratio for each chunks
def compression_ratio(infilename, outfilename):
    #infilename-original filename
    #outfilename-compressed version filename
    #ratio-list which stores all compression ratios
    orginalSize = float(os.stat(infilename).st_size)
    compressSize = float(os.stat(outfilename).st_size)
    ratio.append(orginalSize / compressSize)


#the function to reorder the compression ratios of group of chunks to specific position.
#it is in the order(chunks group) 1024,128,16,1,256,2,32,4,512,64,8
#it reorders to 1,2,4,8,16,32,64,128,256,512,1024
def reorder(ratio):
    for i in range(300, 400):
        myorder.append(i)
    for i in range(500, 600):
        myorder.append(i)
    for i in range(700, 800):
        myorder.append(i)
    for i in range(1000, 1100):
        myorder.append(i)
    for i in range(200, 300):
        myorder.append(i)
    for i in range(600, 700):
        myorder.append(i)
    for i in range(900, 1000):
        myorder.append(i)
    for i in range(100, 200):
        myorder.append(i)
    for i in range(400, 500):
        myorder.append(i)
    for i in range(800, 900):
        myorder.append(i)
    for i in range(0, 100):
        myorder.append(i)
    ratio = [ratio[i] for i in myorder]
    return ratio

#this functon plot the graph for different group chunks based on the compression ratio.
#matplotlib library does the graph plotting
def plot_graph(ratio):
    #ratio is list of all compression ratios
    #data is 2 dimensional array which stores 11 different list,each consists of 100 values
    data = [[0 for x in range(100)] for x in range(100)]
    j = 0
    k = 0
    for i in ratio:
        data[j][k] = i
        k = k + 1
        if (k % 100 == 0):
            k = 0
            j = j + 1
    #the real graph plotting starts from here
    plot_chunks = plt.boxplot(data, widths=1, positions=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    for line in plot_chunks['medians']:
        # get position data for median line
        x, y = line.get_xydata()[1]  # top of median line
        # overlay median value
        plt.text(x, y, '%.1f' % y, horizontalalignment='center')  # draw above, centered
    plt.ylabel('compression ratio')
    plt.xlabel('chunks size')
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], ['1', '2', '4', '8', '16', '32', '64', '128', '256', '512', '1024'])
    plt.show()


if __name__ == "__main__":
    case = int(input("which  compression algorithm do you want to use 1:lzma 2:gzip(deflate)"))
    compression_algm(case)
    ratio = reorder(ratio)
    plot_graph(ratio)
