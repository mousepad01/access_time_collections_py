# Stanciu Adrei Calin - proiectul 1 pentru curusl de Tehnici de simulare

import time
import random

#from mpl_toolkits import mplot3d
#from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pickle

# variable to prevent optimization
_aux = 0
_aux2 = False

class TestTime:

    def __init__(self, element_cnt):

        self.set = set()
        self.list = []
        # self.dict = {}
        # self.tuple = tuple()

        for _ in range(element_cnt):
            
            el = TestTime._rand_str()

            self.set.add(el)
            self.list.append(el)

    @staticmethod
    def _rand_str(l = 16):

        chrs = [chr(i) for i in range(ord('a'), ord('z') + 1)]
            
        s = ''
        for _ in range(l):
            s += (random.choice(chrs))

        return s

    @staticmethod
    def start():

        EPOCH_CNT = 40
        RND_PER_EPOCH = 2000

        ELEMENT_CNT = [2 ** i for i in range(2, 18)]
        NONEXISTENCE_RATIO = [0, 0.1, 0.25, 0.6]

        def _mean_overhead(el_cnt, ne_ratio):

            global _aux, _aux2

            t = 0

            for _ in range(EPOCH_CNT):

                test = TestTime(el_cnt)
                
                ne_cnt = int(ne_ratio * RND_PER_EPOCH)
                e_cnt = RND_PER_EPOCH - ne_cnt

                elements = [random.choice(test.list) for _ in range(e_cnt)] + [TestTime._rand_str() for _ in range(ne_cnt)]
                found = []

                t_start = time.time()

                for el in elements:

                    # existence check

                    if _aux > 128:
                        _aux2 ^= True

                t_end = time.time()
                t += t_end - t_start

            return t / EPOCH_CNT

        def _mean_check_time(el_cnt, ne_ratio, overhead):

            global _aux, _aux2

            t_set = 0
            t_list = 0

            for _ in range(EPOCH_CNT):

                test = TestTime(el_cnt)
                
                ne_cnt = int(ne_ratio * RND_PER_EPOCH)
                e_cnt = RND_PER_EPOCH - ne_cnt

                elements = [random.choice(test.list) for _ in range(e_cnt)] + [TestTime._rand_str() for _ in range(ne_cnt)]

                # for SET

                t_start = time.time()

                for el in elements:

                    found = el in test.set

                    if _aux > 128:
                        _aux2 ^= found

                t_end = time.time()
                t_set += 1000 * (t_end - t_start - overhead)

                # for LIST

                t_start = time.time()

                for el in elements:

                    found = el in test.list

                    if _aux > 128:
                        _aux2 ^= found

                t_end = time.time()
                t_list += 1000 * (t_end - t_start - overhead)

            return t_set / (EPOCH_CNT * RND_PER_EPOCH), t_list / (EPOCH_CNT * RND_PER_EPOCH)
        
        t_set = {ne_ratio: [] for ne_ratio in NONEXISTENCE_RATIO}
        t_list = {ne_ratio: [] for ne_ratio in NONEXISTENCE_RATIO}

        for ne_ratio in NONEXISTENCE_RATIO:

            print(f"[i] Testing for non-existence ratio {ne_ratio}")
               
            for element_cnt in ELEMENT_CNT:

                print(f"[i] ---- Testing for element count {element_cnt}")

                overhead = _mean_overhead(element_cnt, ne_ratio)
                t_set_, t_list_ = _mean_check_time(element_cnt, ne_ratio, overhead)

                t_set[ne_ratio].append(t_set_)
                t_list[ne_ratio].append(t_list_)

            print(f"[*] ---- Done")

        print(f"[*] Done")

        # credit for plotting info: https://jakevdp.github.io/PythonDataScienceHandbook/04.12-three-dimensional-plotting.html

        # plot for set

        with open("res_set.bin", "wb+") as f:
            pickle.dump(t_set, f)

        with open("res_list.bin", "wb+") as f:
            pickle.dump(t_list, f)

        for ne_ratio in NONEXISTENCE_RATIO:
            
            p = plt.axes()
            p.plot(ELEMENT_CNT, t_set[ne_ratio])

            p.set_title(f"SET stats, {ne_ratio * 100}% of queries are NOT in the set")
            p.set_xlabel("elements in the set")
            p.set_ylabel("time per query (ms)")

            plt.show()

        # plot for list

        for ne_ratio in NONEXISTENCE_RATIO:
            
            p = plt.axes()
            p.plot(ELEMENT_CNT, t_list[ne_ratio])

            p.set_title(f"LIST stats, {ne_ratio * 100}% of queries are NOT in the list")
            p.set_xlabel("elements in the list")
            p.set_ylabel("time per query (ms)")

            plt.show()

if __name__ == "__main__":
    TestTime.start()