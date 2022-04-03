"""
Solution to the one-way tunnel
"""

"""
SOLUCIÓN BÁSICA
"""

import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = "south"
NORTH = "north"

NCARS = 100

class Monitor():
    def __init__(self):
        self.cars_north = Value('i', 0) # Número de coches yendo hacia el norte en el tunel
        self.cars_south = Value('i', 0) # Número de coches yendo hacia el sur en el tunel
        self.mutex = Lock()
        self.someone_north = Condition(self.mutex) # Condición para ver si algún coche esta yendo hacia el norte en el tunel
        self.someone_south = Condition(self.mutex) # Condición para ver si algún coche esta yendo hacia el sur en el tunel
        
    def empty_direction_north(self):
        return self.cars_north.value == 0
        
    def empty_direction_south(self):
        return self.cars_south.value == 0
    
    def wants_enter(self, direction):
        self.mutex.acquire()
        if direction == NORTH:
            self.someone_south.wait_for(self.empty_direction_south) # Si un coche quiere entrar el tunel hacia el norte, se espera a que no haya ninguno dentro yendo hacia el sur
            self.cars_north.value += 1
        elif direction == SOUTH:
            self.someone_north.wait_for(self.empty_direction_north) # Si un coche quiere entrar el tunel hacia el sur, se espera a que no haya ninguno dentro yendo hacia el norte
            self.cars_south.value += 1
        print(self.cars_north.value, self.cars_south.value)
        self.mutex.release()
            
    def leaves_tunnel(self, direction):
        self.mutex.acquire()
        if direction == NORTH: 
            self.cars_north.value -= 1
            self.someone_north.notify_all()
        elif direction == SOUTH:
            self.cars_south.value -= 1
            self.someone_south.notify_all()
        print(self.cars_north.value, self.cars_south.value)
        self.mutex.release()
        
        
def delay(n=3):
    time.sleep(random.random()*n)

def car(cid, direction, monitor):
    print(f"car {cid} direction {direction} created", flush = True)
    delay(6)
    print(f"car {cid} heading {direction} wants to enter", flush = True)
    monitor.wants_enter(direction)
    print(f"car {cid} heading {direction} enters the tunnel", flush = True)
    delay(3)
    print(f"car {cid} heading {direction} leaving the tunnel", flush = True)
    monitor.leaves_tunnel(direction)
    print(f"car {cid} heading {direction} out of the tunnel", flush = True)



def main():
    monitor = Monitor()
    cid = 0
    for _ in range(NCARS):
        direction = NORTH if random.randint(0,1)==1  else SOUTH
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        time.sleep(random.expovariate(1/0.5)) # a new car enters each 0.5s

if __name__ == "__main__":
    main()
