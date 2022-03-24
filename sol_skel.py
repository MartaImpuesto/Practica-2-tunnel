"""
Solution to the one-way tunnel
"""
import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = "north"
NORTH = "south"

NCARS = 100

class Monitor():
    def __init__(self):
        self.cars_north = Value('i', 0)
        self.cars_south = Value('i', 0)
        self.mutex = Lock()
        self.stop = Condition(self.mutex)
        
    def going_north(self):
        self.mutex.acquire()
        self.cars_north.value += 1
        self.mutex.release()
    
    def exiting_north(self):
        self.mutex.acquire()
        self.cars_north.value -= 1
        self.mutex.release()
    
    def going_south(self):
        self.mutex.acquire()
        self.cars_south.value += 1
        self.mutex.release()
        
    def exiting_south(self):
        self.mutex.acquire()
        self.cars_south.value -= 1
        self.mutex.release()
        
    def empty_direction_north(self):
        return self.cars_north.value == 0
        
    def empty_direction_south(self):
        return self.cars_south.value == 0
    
    def wants_enter(self, direction):
        self.mutex.acquire()
        if direction == NORTH:
            self.stop.wait_for(self.empty_direction_north)
            #self.going_north()
            self.cars_north.value += 1
        elif direction == SOUTH:
            self.stop.wait_for(self.empty_direction_south)
            #self.going_south()
            self.cars_south.value += 1
        self.mutex.release()
            
    def leaves_tunnel(self, direction):
        self.mutex.acquire()
        #print(self.cars_north.value, self.cars_south.value)
        if direction == NORTH: 
            #self.exiting_north()
            self.cars_north.value -= 1
            self.stop.notify_all()
        elif direction == SOUTH:
            #self.exiting_south()
            self.cars_south.value -= 1
            self.stop.notify_all()
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
