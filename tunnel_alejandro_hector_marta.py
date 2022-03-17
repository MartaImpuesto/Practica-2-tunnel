# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 10:43:15 2022

@author: mimpu
"""

import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = "north"
NORTH = "south"

NCARS = 10

def delay(n=3):
    time.sleep(random.random()*n)

class Tunnel():
    def __init__(self):
        self.cars_north = Value('i', 0)
        self.cars_south = Value('i', 0)
        self.mutex = Lock()
        
    def waiting_in_north(self):
        return self.cars_north.value == 0
    
    def waiting_in_south(self):
        return self.cars_south.value == 0

    def 