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
        
    def wants_enter(self, direction):
        self.mutex.acquire()
        if direction == NORTH:
            self.stop.wait(self.cars_south.value == 0)
            #self.going_north()
            print("p")
            self.cars_north.value += 1
        elif direction == SOUTH:
            self.stop.wait(self.cars_north.value == 0)
            #self.going_south()
            print("q")
            self.cars_south.value += 1
        self.mutex.release()
            
    def leaves_tunnel(self, direction):
        self.mutex.acquire()
        #print(self.cars_north.value, self.cars_south.value)
        if direction == NORTH: 
            self.exiting_north()
            self.stop.notify()
        elif direction == SOUTH:
            self.exiting_south()
            self.stop.notify()
        self.mutex.release()
        
        
def delay(n=3):
    time.sleep(random.random()*n)

def car(cid, direction, monitor):
    print(f"car {cid} direction {direction} created")
    delay(6)
    print(f"car {cid} heading {direction} wants to enter")
    monitor.wants_enter(direction)
    print(f"car {cid} heading {direction} enters the tunnel")
    delay(3)
    print(f"car {cid} heading {direction} leaving the tunnel")
    monitor.leaves_tunnel(direction)
    print(f"car {cid} heading {direction} out of the tunnel")



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
