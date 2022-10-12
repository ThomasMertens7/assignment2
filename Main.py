from multiprocessing import Process
import sys


def MESI(n, input_file, cache_size, associativity, block_size):
    print("MESI: " + str(n))
    with open('/blackscholes_four/blackscholes_0.data', 'r') as f:
        f_contents = f.read()
        print(f_contents)

    print(f.name)



def Dragon(n, input_file, cache_size, associativity, block_size):
    print("Dragon: " + n)
    


if len(sys.argv) != 6:
    raise Exception("Invalid number of arguments")

protocol = sys.argv[1]
input_file = sys.argv[2]
cache_size = sys.argv[3]
associativity = sys.argv[4]
block_size = sys.argv[5]

if protocol == "MESI":
    p = [None,None,None,None]
    for n in range(4):
        p[n] = Process(target=MESI, args=(n, input_file, cache_size, associativity, block_size))
        p[n].start()
        p[n].join()

elif protocol == "Dragon":
    p = [None,None,None,None]
    for n in range(4):
        p[n] = Process(target=Dragon, args=(n, input_file, cache_size, associativity, block_size))
        p[n].start()
        p[n].join()

else:
    raise Exception("Invalid protocol")