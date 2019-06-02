from pybloom import BloomFilter
f = BloomFilter(capacity=1000, error_rate=0.001)
[f.add(x) for x in range(10)]

print ([(x in f) for x in range(10)])

