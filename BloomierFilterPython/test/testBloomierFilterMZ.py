import unittest
import sys
import zlib
from matplotlib import pyplot as plt
from pybloom import *
import timeit
sys.path.append("../src")

FILTER_TEST = True
FILTER_SIZE_TEST = True

from core.bloomierFilter import *


MAX_BLOOMIER_FILTERS = 10
SEED_INDEX = 0

class TestBloomierFilter(unittest.TestCase):
    def setUp(self):
        pass

    def checkExistence(self, bloomiers, blooms, key, keysDict):
        for bloom, bloomier in zip(blooms, bloomiers):
            if key in bloom and bloomier.get(key) != None:
                return bloomier.get(key)

        return None # it literally doesn't exist.


    def tryInserting(self, bloomiers, blooms, seeds, key, keysDict, m,  k, q):
        global SEED_INDEX
        inserted = False
        for i, bloom in enumerate(blooms):
            bloomier = bloomiers[i]
            # this is the case that we simply can't do anything about: the key is in the bloom filter and
            # there is a collision in the bloomier filter. We end early.
            if key in bloom and bloomier.get(key) != None:
                print ("The element " + key + " could not be inserted.")
                return False # in the future, we can try skipping over the element that can't be inserted
                # and keep on going.

            # if the key is not in the bloom filter, we could potentially add it in to the bloomier filter.
            # if the bloomier filter insertion doesn't work out, then we can keep on going.
            elif key not in bloom:
                if bloomier.insert(key, keysDict[key]):
                    bloom.add(key)
                    return True


        # we haven't already inserted yet, but we didn't break early: it's still possible to insert
        if not inserted:
            if len(bloomiers) >= MAX_BLOOMIER_FILTERS or SEED_INDEX >= MAX_BLOOMIER_FILTERS:
                # we need to create another bloomier filter, but we're past threshold
                return False
            else:
                # we'll create another bloom filter and bloomier filter structure and insert it there
                # the bloom filter and bloomier filter will have the same number of buckets to start.
                bloomier = BloomierFilter(seeds[SEED_INDEX], keysDict, m, k, q)
                bloom = BloomFilter(capacity=m, error_rate=0.001)
                bloomier.insert(key, keysDict[key])
                bloom.add(key)
                bloomiers.append(bloomier)
                blooms.append(bloom)
                SEED_INDEX += 1
                return True



    def testBloom_BloomierFilter(self):
        global SEED_INDEX
        # hashSeed, keysDict, m, k, q
        # m should be multiple of the size m
        # k
        # q : bit size

        # trial Bloom Filter
        f = BloomFilter(capacity=1000, error_rate=0.001)
        [f.add(x) for x in range(10)]

        print ([(x in f) for x in range(10)])

        #- ---------------------------------------------------------------------------------------------

        seeds = [0, 67, 72, 93, 83, 0, 13, 14, 34, 6, 7, 12]
        # seeds = [0, 14, 1, 4, 5, 6, 7, 11, 12, 3, 13, 15]

        num_elems = 100000

        # set up all the keys we want to test
        keysDict = {}
        for i in range(num_elems):
            keysDict[str(i)] = i

        values_k = range(2, 15)
        c = 2


        numInsertions = []
        times = []
        for value_k in values_k:
            start = timeit.default_timer()

            m = int(1000*value_k*c) # # len(k) * 1.5 len(k) * 1.1
            SEED_INDEX = 0
            bloomiers = []
            blooms = []
            bloomier = BloomierFilter(seeds[SEED_INDEX], keysDict, m, value_k, 16)
            bloom = BloomFilter(capacity=m, error_rate=0.001)
            bloomiers.append(bloomier)
            blooms.append(bloom)
            SEED_INDEX += 1

            inserted = 0
            final = 0
            for i, key in enumerate(keysDict):
                if not self.tryInserting(bloomiers, blooms, seeds, key, keysDict, m, value_k, 16):
                    final = i
                    break
                else:
                    inserted += 1
                # if inserted % 1000 == 0:
                #     print (inserted)
                #     print (SEED_INDEX)

            # check correct insertions
            for i, key in enumerate(keysDict):
                if i >= final:
                    break
                self.assertEqual(self.checkExistence(bloomiers, blooms, key, keysDict), keysDict[key])


            # false positives
            for i in range(num_elems, num_elems + 1):
                self.assertEqual(self.checkExistence(bloomiers, blooms, str(i), i), None)

            print (inserted)
            print ("this is length", m)
            numInsertions.append(inserted)

        plt.plot(values_k, numInsertions)
        plt.title('Number of Insertions Within 10 Bloom-Bloomier Structures')
        plt.xlabel('k value (number of hash functions); number of buckets is m = 2000*k (both Bloom & Bloomier)')
        plt.ylabel('Number of Insertions Within 10 Bloom-Bloomier Structures')
        plt.savefig('linear_k_num_ins_in_10_bloom_bloomier2.png')


if __name__ == "__main__":
    unittest.main(verbosity=2)
