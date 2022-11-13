from multiprocessing import *
import sys
import math
from Constants import *


def MESI(n, input_file, block_size, modcache, cache):
    print("MESI: " + str(n))

    # Open the file and read contents
    with open('./' + input_file + '_four/' + input_file + '_' + str(n) + '.data', 'r') as f:
        f_contents = f.readlines()

    # Set up all the output variables
    cycle = 0
    compute_cycles = 0
    load_store_instructions = 0
    idle_cycles = 0
    misses_core = 0
    bus_transfers = 0
    invalidations = 0
    private_data_accesses = 0
    shared_data_accesses = 0


    # Set up help variables
    total_lines = len(f_contents)

    # Every time we have a delay go a couple of extra_cycles times through loop
    def delay(extra_cycles):
        while extra_cycles > 0:
            extra_cycles -= 1

    # Based on the element and the move we process, change state of all elements influenced by this
    def change_state(element, cycle, move, core, idle_cycles, misses_core, bus_transfers, invalidations, private_data_accesses, shared_data_accesses):
        if element[1] == "M":
            if move == "PR":
                private_data_accesses += 1
                delay(CACHE_HIT)
                idle_cycles += CACHE_HIT
                q = cache[core]
                try:
                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].remove(element)
                except:
                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].pop(0)
                q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].append(element)
                cache[core] = q

            elif move == "PW":
                private_data_accesses += 1
                q = cache[core]
                try:
                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].remove(element)
                except:
                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].pop(0)
                q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].append(element)
                cache[core] = q

            elif move == "BR":
                q = cache[core]
                try:
                    q[getIndex(element[0], block_size, modcache)].remove(element)
                except:
                    q[getIndex(element[0], block_size, modcache)].pop(0)
                element[1] == "S"
                q[getIndex(element[0], block_size, modcache)].append(element)
                cache[core] = q

            elif move == "BRX":
                q = cache[core]
                try:
                    q[getIndex(element[0], block_size, modcache)].remove(element)
                except:
                    q[getIndex(element[0], block_size, modcache)].pop(0)
                element[1] == "I"
                q[getIndex(element[0], block_size, modcache)].append(element)
                cache[core] = q

        elif element[1] == "E":
            if move == "PR":
                private_data_accesses += 1
                delay(CACHE_HIT)
                idle_cycles += CACHE_HIT
                q = cache[core]
                try:
                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].remove(element)
                except:
                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].pop(0)
                q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].append(element)
                cache[core] = q

            elif move == "PW":
                private_data_accesses += 1
                q = cache[core]
                try:
                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].remove(element)
                except:
                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].pop(0)
                element[1] == "M"
                q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].append(element)
                cache[core] = q

            elif move == "BR":
                q = cache[core]
                try:
                    q[getIndex(element[0], block_size, modcache)].remove(element)
                except:
                    q[getIndex(element[0], block_size, modcache)].pop(0)
                element[1] == "S"
                q[getIndex(element[0], block_size, modcache)].append(element)
                cache[core] = q

            elif move == "BRX":
                q = cache[core]
                try:
                    q[getIndex(element[0], block_size, modcache)].remove(element)
                except:
                    q[getIndex(element[0], block_size, modcache)].pop(0)
                element[1] == "I"
                q[getIndex(element[0], block_size, modcache)].append(element)
                cache[core] = q
                
        elif element[1] == "S":
            if move == "PR":
                shared_data_accesses += 1
                delay(CACHE_HIT)
                idle_cycles += CACHE_HIT
                q = cache[core]
                try:
                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].remove(element)
                except:
                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].pop(0)
                q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].append(element)
                cache[core] = q

            if move == "PW":
                shared_data_accesses += 1
                q = cache[core]
                try:
                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].remove(element)
                except:
                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].pop(0)
                element[1] == "M"
                q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].append(element)
                cache[core] = q
                for i in range(len(cache)):
                    if i != core:
                        for j in range(len(cache[i][getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)])):
                            if cache[i][getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)][j][0] == int(f_contents[cycle][2:-1], base=16):
                                invalidations += 1
                                bus_transfers += 1
                                change_state(cache[i][getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)][j], cycle, "BRX", i, idle_cycles, misses_core, bus_transfers, invalidations, private_data_accesses, shared_data_accesses)

            elif move == "BRX":
                q = cache[core]
                try:
                    q[getIndex(element[0], block_size, modcache)].remove(element)
                except:
                    q[getIndex(element[0], block_size, modcache)].pop(0)
                element[1] = "I"
                q[getIndex(element[0], block_size, modcache)].append(element)
                cache[core] = q

            elif move == "BR":
                q = cache[core]
                try:
                    q[getIndex(element[0], block_size, modcache)].remove(element)
                except:
                    q[getIndex(element[0], block_size, modcache)].pop(0)
                q[getIndex(element[0], block_size, modcache)].append(element)
                cache[core] = q

        elif element[1] == "I":
            if move == "PR":
                misses_core += 1
                tf = False
                for i in range(len(cache)):
                    if i != core and tf == False:
                        for j in range(len(cache[i][getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)])):
                            if cache[i][getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)][j][0] == int(f_contents[cycle][2:-1], base = 16) and cache[i][getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)][j][1] != "I" and tf == False:
                                bus_transfers += 1
                                idle_cycles, misses_core, bus_transfers, invalidations, private_data_accesses, shared_data_accesses = change_state(cache[i][getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)][j], cycle, "BR", i, idle_cycles, misses_core, bus_transfers, invalidations, private_data_accesses, shared_data_accesses)
                                delay(CACHE_TO_CACHE * block_size / 4 + CACHE_HIT)
                                idle_cycles += CACHE_TO_CACHE * block_size / 4 + CACHE_HIT                                
                                if element[0] == None:
                                    q = cache[core]
                                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].pop(0)
                                    element = [int(f_contents[cycle][2:-1], base=16), "S"]
                                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].append(element)
                                    cache[core] = q
                                else:
                                    q = cache[core]
                                    try:
                                        q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].remove(element)
                                    except:
                                        q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].pop(0)
                                    element = [int(f_contents[cycle][2:-1], base=16), "S"]
                                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].append(element)
                                    cache[core] = q
                                tf = True

                if tf == False:
                    delay(MEMORY_TO_CACHE + CACHE_HIT)
                    idle_cycles += MEMORY_TO_CACHE + CACHE_HIT
                    if element[0] == None:
                        q = cache[core]
                        q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].pop(0)
                        element = [int(f_contents[cycle][2:-1], base=16), "E"]
                        q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].append(element)
                        cache[core] = q
                    else:
                        q = cache[core]
                        try:
                            q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].remove(element)
                        except:
                            q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].pop(0)
                        element = [int(f_contents[cycle][2:-1], base=16), "E"]
                        q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].append(element)
                        cache[core] = q

            elif move == "PW":
                if element[0] == None:
                    misses_core += 1
                    q = cache[core]
                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].pop(0)
                    element = [int(f_contents[cycle][2:-1], base=16), "M"]
                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].append(element)
                    cache[core] = q
                else:
                    q = cache[core]
                    try:
                        q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].remove(element)
                    except:
                        q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].pop(0)
                    element = [int(f_contents[cycle][2:-1], base=16), "M"]
                    q[getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)].append(element)
                    cache[core] = q

                for i in range(len(cache)):
                    if i != core:
                        for j in range(len(cache[i][getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)])):
                            if cache[i][getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)][j][0] == int(f_contents[cycle][2:-1], base=16):
                                invalidations += 1
                                bus_transfers += 1
                                idle_cycles, misses_core, bus_transfers, invalidations, private_data_accesses, shared_data_accesses = change_state(cache[i][getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)][j], cycle, "BRX", i, idle_cycles, misses_core, bus_transfers, invalidations, private_data_accesses, shared_data_accesses)

        return idle_cycles, misses_core, bus_transfers, invalidations, private_data_accesses, shared_data_accesses

    # Iteration for one core
    while cycle < total_lines:
        if f_contents[cycle][0] == LOAD:
            load_store_instructions += 1
            tf = False
            for i in range(len(cache[n][getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)])):
                if cache[n][getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)][i][0] == int(f_contents[cycle][2:-1], base=16):
                    tf = True

                    idle_cycles, misses_core, bus_transfers, invalidations, private_data_accesses, shared_data_accesses = change_state(cache[n][getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)][i], cycle, "PR", n, idle_cycles, misses_core, bus_transfers, invalidations, private_data_accesses, shared_data_accesses)

            if tf == False:
                element = [None, "I"]
                idle_cycles, misses_core, bus_transfers, invalidations, private_data_accesses, shared_data_accesses = change_state(element, cycle, "PR", n, idle_cycles, misses_core, bus_transfers, invalidations, private_data_accesses, shared_data_accesses)    

        elif f_contents[cycle][0] == STORE:
            load_store_instructions += 1
            tf = False
            for i in range(len(cache[n][getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)])):
                if cache[n][getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)][i][0] == int(f_contents[cycle][2:-1], base=16):
                    tf = True
                    idle_cycles, misses_core, bus_transfers, invalidations, private_data_accesses, shared_data_accesses = change_state(cache[n][getIndex(int(f_contents[cycle][2:-1], base=16), block_size, modcache)][i], cycle, "PW", n, idle_cycles, misses_core, bus_transfers, invalidations, private_data_accesses, shared_data_accesses)

            if tf == False:
                element = [None, "I"]
                idle_cycles, misses_core, bus_transfers, invalidations, private_data_accesses, shared_data_accesses = change_state(element, cycle, "PW", n, idle_cycles, misses_core, bus_transfers, invalidations, private_data_accesses, shared_data_accesses)

        elif f_contents[cycle][0] == DELAY:
            delay_dec = int(f_contents[cycle][2:-1], base=16)
            delay(delay_dec)
            compute_cycles += delay_dec
            
        else: 
            raise Exception("Invalid operation")
        
        
        cycle += 1

    # Nice to see how progress is going
        if (cycle % 500000) == 0:
            print("Cycle: " + str(cycle))

    # Prints output at end of execution
    print(cache[n])
    print((n, (cycle + compute_cycles + idle_cycles), compute_cycles, load_store_instructions, idle_cycles, float(misses_core)/float(load_store_instructions), (bus_transfers * block_size), invalidations, private_data_accesses, shared_data_accesses))
        

def getIndex(address, block_size, modcache):
    return math.floor((int(address) / block_size) % modcache)
          

def Dragon(n, input_file, cache_size, associativity, block_size):
    print("Dragon: " + n)
    


if len(sys.argv) != 6:
    raise Exception("Invalid number of arguments.")

protocol = sys.argv[1]
input_file = sys.argv[2]
cache_size = sys.argv[3]
associativity = sys.argv[4]
block_size = sys.argv[5]

# Develop the virtual cache model
block_size = int(block_size)
modcache = int((int(cache_size) / block_size) / int(associativity))
p_cache = {}
for key in range(modcache):
    p_cache[key] = [[None, "I"] for i in range(int(associativity))]

# Develop a shared variable of the cache model, so that all processes can access it
manager = Manager()
cache = manager.list()
for i in range(4):
    cache.append(p_cache)

# If protocol is MESI, then run MESI in parallel for each core
if protocol == "MESI":
    p = [None,None,None,None]
    for n in range(4):
        p[n] = Process(target=MESI, args=(n, input_file, block_size, modcache, cache))
        p[n].start()
    
    for n in range(4):
        p[n].join()

# If protocol is Dragon, then run Dragon in parallel for each core
elif protocol == "Dragon":
    p = [None,None,None,None]
    for n in range(4):
        p[n] = Process(target=Dragon, args=(n, input_file, cache_size, associativity, block_size, cache))
        p[n].start()
        p[n].join()

else:
    raise Exception("Invalid protocol")