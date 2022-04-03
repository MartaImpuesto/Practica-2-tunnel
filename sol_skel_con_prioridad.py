# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 09:08:32 2022

@author: mimpu
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
        self.cars_north_waiting= Value ('i', 0) # Número de coches esperando para ir hacia el norte en el tunel
        self.cars_south_waiting= Value ('i', 0) # Número de coches esperando para ir hacia el sur en el tunel
        self.mutex = Lock()
        self.someone_north = Condition(self.mutex)
        self.someone_south = Condition(self.mutex)
        self.nobody = Condition(self.mutex)
        
    def empty_direction_north(self):
        return self.cars_north.value == 0 and self.cars_north_waiting.value <= self.cars_south_waiting.value
        
    def empty_direction_south(self):
        return self.cars_south.value == 0 and self.cars_south_waiting.value <= self.cars_north_waiting.value
    
    def wants_enter(self, direction):
        self.mutex.acquire()
        if direction == NORTH:
            self.cars_north_waiting.value += 1
            print("w", self.cars_north_waiting.value, self.cars_south_waiting.value)
            self.someone_south.wait_for(self.empty_direction_south)
            self.cars_north.value += 1
            self.cars_north_waiting.value -= 1
            print("w", self.cars_north_waiting.value, self.cars_south_waiting.value)            
        elif direction == SOUTH:
            self.cars_south_waiting.value += 1
            print("w", self.cars_north_waiting.value, self.cars_south_waiting.value)
            self.someone_north.wait_for(self.empty_direction_north)
            self.cars_south.value += 1
            self.cars_south_waiting.value -= 1
            print("w", self.cars_north_waiting.value, self.cars_south_waiting.value)
        print(self.cars_north.value, self.cars_south.value)
        self.mutex.release()
            
    def leaves_tunnel(self, direction):
        self.mutex.acquire()
        #print(self.cars_north.value, self.cars_south.value)
        if direction == NORTH: 
            self.cars_north.value -= 1
            self.someone_north.notify_all()
            if self.cars_north.value == 0:
                self.nobody.notify()
        elif direction == SOUTH:
            self.cars_south.value -= 1
            self.someone_south.notify_all()
            if self.cars_south.value == 0:
                self.nobody.notify()
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