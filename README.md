# stream-compression
Project Description 
OpenSky Network  is an initiative took by researches from armasuisse(Switzerland),
University of Kaiserslautern(Germany) and University of Oxford(UK).
The main objective of the project is to provide high quality air traffic data for research purposes.
The main goal of the project can be divided in to two as follows
• Reduce the network load - Many sensors at different parts of the Europe
can cause high network load. So we need to find a suitable approach to reduce
the network load considerably.
• Loss of packets should not occur - We should find an approach that saves
each and every packets of type 2(short message) and type 3(long message).The
packets which do not come under type 2 and 3 can be neglected.


I evaluated the performance of different compression techniques. A large and quite different number of lossless
compression systems were proposed and implemented. I evaluated compression ratio, latency and time over different size of 
packets for different lossless compression techniques. 

Moreover I evaluated the performance of stream compression on real time data.
System Design Requirements
 -Real-time Capability: Compression and Decompression should never exceed 1s
 -Low complexity of compression: Compression part should have low complexity
 -Low Communication Overhead: Performance of the system measures in Total transmit data including system/Control overhead of the compression system
The compression and decompression system should be able to work via Linux pipelines as follows.
netcat sensordata | compress_stream.py | tee a.bin | decompress_stream.py > b.bin

Please look at the final presentation folder to see more details about the project, objectives and results.
