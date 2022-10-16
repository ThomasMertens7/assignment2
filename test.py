from multiprocessing import Process
import sys
import math
from Constants import *


def MESI(n, input_file, cache_size, associativity, block_size):
    print("MESI: " + str(n))

    with open('./' + input_file + '_four/' + input_file + '_' + str(n) + '.data', 'r') as f:
        f_contents = f.readlines()

    cycle = 0
    compute_cycles = 0
    load_store_instructions = 0
    idle_cycles = 0
    misses_core = 0
    load_instruction = 0

    extra_cycles = 0
    total_lines = len(f_contents)

    modcache = int((int(cache_size) / int(block_size)) / int(associativity))
    L1_cache = {}
    for key in range(modcache):
        L1_cache[key] = [[None, "I", 0] * int(associativity)]

    current_assignment = ""

    while cycle < total_lines:
        if extra_cycles > 1:
            extra_cycles -= 1
        
        elif extra_cycles == 1:
            extra_cycles = 0
            if current_assignment == "M":
                for i in L1_cache[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)]:
                    if i[0] == int(f_contents[cycle][2:-1], base=16):
                        L1_cache[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].remove(i)
                        i[1] = "M"
                        L1_cache[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].append(i)
                        break
            elif len(current_assignment) > 0 and current_assignment[0] == "S":
                L1_cache[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].remove(i)
                i[0] = "S"
                L1_cache[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].append(i)
                L1_cache[j].remove(k)
                k[0] = "S"
                L1_cache[j].append(k)

            elif len(current_assignment) > 0 and current_assignment[0] == "E":
                L1_cache[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].pop(0)
                i = [int(f_contents[cycle][2:-1], base=16), "M", 0]
                L1_cache[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].append(i)
            cycle += 1
            current_assignment = ""

        else:
            if f_contents[cycle][0] == LOAD:
                load_store_instructions += 1
                for i in L1_cache[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)]:
                    if i[0] == f_contents[cycle][2:-1]:
                        extra_cycles += CACHE_HIT
                        idle_cycles += CACHE_HIT
                        break

                    else:
                        misses_core += 1
                        tf = False
                        for j in L1_cache.keys():
                            if (j != L1_cache[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)]) and (tf == False):
                                for k in L1_cache[j]:
                                    if (k[0] == f_contents[cycle][2:-1]) and (k[1] != "I") and (tf == False):
                                        extra_cycles += (CACHE_TO_CACHE * block_size) + CACHE_HIT
                                        idle_cycles += (CACHE_TO_CACHE * block_size) + CACHE_HIT
                                        current_assignment = "S " + i + " " + j + " " + k
                                        tf = True
    
                        if tf == False:
                            extra_cycles += MEMORY_TO_CACHE + CACHE_HIT
                            idle_cycles += MEMORY_TO_CACHE + CACHE_HIT
                            current_assignment = "E"

            elif f_contents[cycle][0] == STORE:
                tf = False
                for i in L1_cache[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)]:
                    if i[0] == f_contents[cycle][2:-1] and tf == False:
                        current_assignment = "M"
                        tf = True
                        #Should send message to other processors now


                

                    

                  


                load_store_instructions += 1
                extra_cycles += MEMORY_TO_CACHE
                idle_cycles += MEMORY_TO_CACHE

            elif f_contents[cycle][0] == DELAY:
                extra_cycles += int(f_contents[cycle][2:-1], base = 16)
                compute_cycles += int(f_contents[cycle][2:-1], base = 16)
                idle_cycles += int(f_contents[cycle][2:-1], base = 16)
            
            else: 
                raise Exception("Invalid operation")

    return (cycle + idle_cycles), compute_cycles, load_store_instructions, idle_cycles

def getIndex(address, block_size, modcache):
    return math.floor((int(address) / block_size) % modcache)
          
print(MESI(0, 'blackscholes', 4096, 2, 32))