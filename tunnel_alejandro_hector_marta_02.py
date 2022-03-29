# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 10:43:15 2022
@author: mimpu
"""

import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value
from multiprocessing import current_process

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
        self.nobody = Condition(self.mutex)
        
    def going_north(self):
        self.mutex.acquire()
        self.cars_north.value += 1
        self.mutex.release()
    
    def exiting_north(self):
        self.mutex.acquire()
        self.cars_north.value -= 1
        if self.cars_north == 0:
            self.nobody.notify()
        self.mutex.release()
    
    def going_south(self):
        self.mutex.acquire()
        self.cars_south.value += 1
        self.mutex.release()
        
    def exiting_south(self):
        self.mutex.acquire()
        self.cars_south.value -= 1
        if self.cars_south == 0:
            self.nobody.notify()
        self.mutex.release()
        
'''    def wants_enter(self, direction):
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
'''

def delay(n=3):
    time.sleep(random.random()*n)

def car_north(tunnel):
    print(f"car {current_process().name} from north created")
    delay()
    print(f"car {current_process().name} from north wants to go south")
    tunnel.going_north()
    print(f"car {current_process().name} from north enters the tunnel")
    delay()
    print(f"car {current_process().name} from north leaving the tunnel")
    tunnel.exiting_north()
    print(f"car {current_process().name} from north out of the tunnel")


def car_south(tunnel):
    print(f"car {current_process().name} from south created")
    delay()
    print(f"car {current_process().name} from south wants to go north")
    tunnel.going_south()
    print(f"car {current_process().name} from south enters the tunnel")
    delay()
    print(f"car {current_process().name} from south leaving the tunnel")
    tunnel.exiting_south()
    print(f"car {current_process().name} from south out of the tunnel")

#genero una serie de coches y genero direccion aleatoria. Hago proceso de un coche y por último
# la ultima linea. Expovariate unos entran antes y otros despues pero todos con media 0.5s
# no se avanzar con el Main

def main():
    tunnel = Tunnel()
    cars_from_north = [Process(target=car_north, name=f"N{i}", args=(tunnel,)) \
               for i in range(NCARS)]
   
    cars_from_south = [Process(target=car_south, name=f"S{i}", args=(tunnel,)) \
               for i in range(NCARS)]

    for x in cars_from_north+cars_from_south:
        x.start()
    for x in cars_from_north+cars_from_south:
        x.join()

# time.sleep(random.expovariate(1/0.5)) # a new car enters each 0.5
if __name__ == '__main__':
    main()
