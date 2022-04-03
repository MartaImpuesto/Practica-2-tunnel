#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 17:58:52 2022

@author: alejandro
"""

"""
Solution to the one-way tunnel
"""
import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = "south"
NORTH = "north"

NCARS = 100

PASSES = 5

class Monitor():
    def __init__(self):
        self.cars_north = Value('i', 0)
        self.cars_south = Value('i', 0)
        #esperan para entrar
        self.cars_north_waiting= Value ('i', 0)
        self.cars_south_waiting= Value ('i', 0)
        #turno 0 para la dirección norte y 1 para la dirección sur
        self.turn = Value("i", 0)
        self.allowed_passes = Value("i", 0)
        #bloqueo
        self.mutex = Lock()
        self.someone_north = Condition(self.mutex)
        self.someone_south = Condition(self.mutex)
        
    def empty_direction_north(self):
        #Dirección norte sin coches, con turno para dirección sur y sin cola de coches en el norte
        return self.cars_north.value == 0 and (self.turn.value == 1 or self.cars_north_waiting.value == 0)
        
    def empty_direction_south(self):
        #Snálogo al anterior con los coches en dirección sur
        return self.cars_south.value == 0 and (self.turn.value == 0 or self.cars_south_waiting.value == 0)
    
    def wants_enter(self, direction):
        self.mutex.acquire()
        if direction == NORTH:
            self.cars_north_waiting.value += 1
            print("w", self.cars_north_waiting.value, self.cars_south_waiting.value)
            self.someone_south.wait_for(self.empty_direction_south)
            if self.cars_south_waiting.value == 0:
                self.turn.value = 0
                self.allowed_passes.value = 0
            self.cars_north_waiting.value -= 1
            print("w", self.cars_north_waiting.value, self.cars_south_waiting.value)
            self.cars_north.value += 1
            self.allowed_passes.value = (self.allowed_passes.value + 1)%PASSES
            print("N", self.allowed_passes.value)
            if self.allowed_passes.value == PASSES-1:
                self.turn.value = 1
        elif direction == SOUTH:
            self.cars_south_waiting.value += 1
            print("w", self.cars_north_waiting.value, self.cars_south_waiting.value)
            self.someone_north.wait_for(self.empty_direction_north)
            if self.cars_north_waiting.value == 0:
                self.turn.value = 1
                self.allowed_passes.value = 0
            self.cars_south_waiting.value -= 1
            print("w", self.cars_north_waiting.value, self.cars_south_waiting.value)
            self.cars_south.value += 1
            self.allowed_passes.value = (self.allowed_passes.value + 1)%PASSES
            print("S", self.allowed_passes.value)
            if self.allowed_passes.value == PASSES-1:
                self.turn.value = 0
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
