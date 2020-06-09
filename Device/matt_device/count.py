# A dummy program that counts down seconds

import sys, time

def count(num):
    for i in range(0, num):
        print("count", i)
        time.sleep(1)

count(int(sys.argv[1]))