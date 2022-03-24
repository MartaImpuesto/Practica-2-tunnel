# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 10:43:15 2022

@author: mimpu
"""

import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

NORTH = "north"
SOUTH = "south"

NCARS = 10

def delay(n=3):
    time.sleep(random.random()*n)

class Tunnel():
    def __init__(self):
        self.cars_north = Value('i', 0)
        self.cars_south = Value('i', 0)
        self.mutex = Lock()
        self.stop = Condition(mutex)
        
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
            self.stop.wait(self.cars_south == 0)
            self.cars_north += 1
        elif direction == SOUTH:
            self.stop.wait(self.cars_north == 0)
            self.cars_south += 1
        self.mutex.release()
            
    def leaves_tunnel(self, direction):
        self.mutex.acquire()
        #print(self.cars_north.value, self.cars_south.value)
        if direction == NORTH: 
            self.cars_noth -= 1
            self.stop.notify()
        elif direction == SOUTH:
            self.cars_south -= 1
            self.stop.notify()
        self.mutex.release()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        