import unittest
import sys
import zlib
from matplotlib import pyplot as plt
from pybloom import *
import timeit
sys.path.append("..\src")

FILTER_TEST = True
FILTER_SIZE_TEST = True

from core.bloomierFilter import *

class TestBloomierFilter(unittest.TestCase):
    def setUp(self):
        pass

    # def test_simple(self):
    #     k = {"abc":10, "def":20, "abd":30}
    #     bf = BloomierFilter(0, k, 10, 3, 8)

    #     #print "****\n\n\n"
    #     self.assertEqual(bf.get("abd"), k["abd"])
    #     self.assertEqual(bf.get("abc"), k["abc"])
    #     self.assertEqual(bf.get("def"), k["def"])
    #     self.assertEqual(bf.get("xyz"), None)

    #     bf.set("def", 12)
    #     self.assertEqual(bf.get("def"), 12)

    #     # return the value back
    #     bf.set("def", k["def"])
    #     return bf

    '''
    def test2(self):
        # hashSeed, keysDict, m, k, q
        # m should be multiple of the size m
        # k
        # q : bit size
        num_elems = 1000
        num_false_check = 50000

        k = {}
        for i in range(num_elems):
            k[str(i)] = i

        values_k = range(3, 16)

        plt.figure()

        for seed in [11, 12, 13, 14, 15, 0, 1, 2, 4, 5, 6, 7]:
          print(seed)
          fps = []
          for value_k in values_k:

            m = int(len(k)*4) # # len(k) * 1.5 len(k) * 1.1

            bf = BloomierFilter(seed, k, m, value_k, 16)
            for i in range(num_elems):
                self.assertEqual(bf.get(str(i)), i)

            if FILTER_TEST:
                #false positive
                falsePositive = 0
                for i in range(num_elems, num_false_check):
                    #print bf.get(str(i))
                    if bf.get(str(i)) is not None:
                        falsePositive += 1
                print("# of False positive %d: %f%%" % (falsePositive, 100.0*falsePositive/(num_false_check - num_elems)))
                fps.append(falsePositive/(num_false_check - num_elems))

          plt.plot(values_k, fps)
        plt.title('False Positive Rate for Various k')
        plt.xlabel('k value')
        plt.ylabel('False Positive Rate')
        plt.savefig('linear_k_false_positive.png')
    '''

    def test2(self):
        # hashSeed, keysDict, m, k, q
        # m should be multiple of the size m
        # k
        # q : bit size
        f = BloomFilter(capacity=1000, error_rate=0.001)
        [f.add(x) for x in range(10)]

        print ([(x in f) for x in range(10)])
        num_elems = 10000
        num_false_check = 50000

        keysDict = {}
        for i in range(num_elems):
            keysDict[str(i)] = i

        values_k = range(2, 16)
        c = 2

        for seed in [2]:
          print(seed)
          numInsertions = []
          times = []
          for value_k in values_k:
            start = timeit.default_timer()

            m = int(1000*value_k*c) # # len(k) * 1.5 len(k) * 1.1

            bf = BloomierFilter(seed, keysDict, m, value_k, 16)

            inserted = 0
            for key in keysDict:
                if bf.insert(key, keysDict[key]):
                        inserted += 1
                else:
                    break
            print (inserted)
            print ("this is length", m)
            numInsertions.append(inserted)

        plt.plot(values_k, numInsertions)
        plt.title('Number of Insertions Before first Fail')
        plt.xlabel('k value (number of hash functions); number of buckets is m = 2000*k')
        plt.ylabel('Number of Insertions Before first Fail')
        plt.savefig('linear_k_num_ins_before_first_fail2.png')

            # stop = timeit.default_timer()
            # times.append(stop-start)
            # for i in range(num_elems):    
            #     self.assertEqual(bf.get(str(i)), i)

        #     if FILTER_TEST:
        #         #insertions that worked before the first fail
        #         insertionWorks = 0
        #         done = False
        #         for i in range(num_elems, num_false_check):
        #             #print bf.get(str(i))
        #             if not done:
        #                 if bf.insert(str(i), i) is False:
        #                     done = True
        #                 else:
        #                     insertionWorks += 1
        #         # print("# of InsertionFails %d: %f%%" % (insertionWorks, 100.0*insertionWorks/(num_false_check - num_elems)))
        #         print ("size of array", m, len(bf.getTable()))
        #         insWorks.append(insertionWorks)
        # plt.plot(values_k, insWorks)
        # plt.title('Number of Insertions that Worked After ' + str(num_elems) + " inserted, before the first fail")
        # plt.xlabel('k value (number of hash functions); number of buckets is m = ckn')
        # plt.ylabel('Number of Insertions After ' + str(num_elems) + " inserted")
        # plt.savefig('linear_k_insertion_fails_with_actual_insertion.png')


      


    # def atest_givenTable(self):
    #     bfGiven = self.test_simple()
    #     table = bfGiven.getTable()
    #     valueTable = bfGiven.getValueTable()

    #     k = {"abc":10, "def":20, "abd":30}
    #     bf = BloomierFilter(0, k, 10, 3, 16, useTable=True)
    #     bf.setTable(table)
    #     bf.setValueTable(valueTable)

    #     self.assertEqual(bf.get("abd"), k["abd"])
    #     self.assertEqual(bf.get("abc"), k["abc"])
    #     self.assertEqual(bf.get("def"), k["def"])
    #     self.assertEqual(bf.get("xyz"), None)

    #     bf.set("def", 12)
    #     self.assertEqual(bf.get("def"), 12)

    # def test_bigTable(self):
    #     # hashSeed, keysDict, m, k, q
    #     # m should be multiple of the size m
    #     # k
    #     # q : bit size

    #     k = {}
    #     for i in range(1000):
    #         k[str(i)] = i

    #     m = int(len(k)*1.5) # len(k) * 1.1

    #     bf = BloomierFilter(0, k, m, 5, 16)
    #     for i in range(1000):
    #         self.assertEqual(bf.get(str(i)), i)


    #     if FILTER_SIZE_TEST:
    #         res = bf.table2string()

    #         print('\nbloomier')
    #         print(len(res))
    #         #sprint(zlib.compress(res))
    #         print(len(zlib.compress(res.encode('utf-8'))))

    #         print('\narray')
    #         res = map2string(k)
    #         print(len(res))
    #         #sprint(zlib.compress(res))
    #         print(len(zlib.compress(res.encode('utf-8'))))

    #     if FILTER_TEST:
    #         #false positive
    #         falsePositive = 0
    #         for i in range(1000, 20000):
    #             #print bf.get(str(i))
    #             if bf.get(str(i)) is not None:
    #                 falsePositive += 1
    #         print("# of False positive %d: %f%%" % (falsePositive, 100.0*falsePositive/(20000 - 1000)))


    # def test_table2string(self):
    #     k = {"abc":10, "def":20, "abd":30}
    #     bf = BloomierFilter(0, k, 10, 3, 16)
    #     res = bf.table2string()
    #     self.assertEqual(66, len(res))
    #     return res

    #     if FILTER_SIZE_TEST:
    #         #sprint(res)
    #         print('\nbloomier')
    #         print(len(res))
    #         #sprint(zlib.compress(res))
    #         print(len(zlib.compress(res.encode('utf-8'))))

    #         print('\narray')
    #         res = map2string(k)
    #         print(len(res))
    #         #sprint(zlib.compress(res))
    #         print(len(zlib.compress(res.encode('utf-8'))))

    # def test_string2table(self):
    #     k = {"abc":10, "def":20, "abd":30}
    #     bf = BloomierFilter(0, k, 10, 3, 16) # m = 10, k = 3, q = 16 (2 bytes)
    #     originalTable1 = bf.getTable()
    #     originalTable2 = bf.getValueTable()
    #     res = self.test_table2string()
    #     table1, table2 = bf.string2table(res)
    #     self.assertEqual(table1, originalTable1)
    #     self.assertEqual(table2, originalTable2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
