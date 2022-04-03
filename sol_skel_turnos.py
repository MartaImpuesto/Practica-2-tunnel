#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 17:58:52 2022

@author: alejandro
"""

"""
Solution to the one-way tunnel
"""

"""
SOLUCIÓN USANDO TURNOS
"""

import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = "south"
NORTH = "north"

NCARS = 100

PASSES = 5 # Máximo número de pasos consecutivos de un lado mientras que hay algún coche esperando en el lado contrario

class Monitor():
    def __init__(self):
        self.cars_north = Value('i', 0) # Número de coches yendo hacia el norte en el tunel
        self.cars_south = Value('i', 0) # Número de coches yendo hacia el sur en el tunel
        self.cars_north_waiting= Value ('i', 0) # Número de coches esperando para ir hacia el norte en el tunel
        self.cars_south_waiting= Value ('i', 0) # Número de coches esperando para ir hacia el sur en el tunel
        self.turn = Value("i", 0) # Turno. 0 si le toca pasar a los del norte, 1 si le toa a los del sur
        self.allowed_passes = Value("i", 0) # Contador para ver cúantos coches han pasado
        self.mutex = Lock()
        # NOTA: Los dos siguientes condition se podrían dejar como uno solo.
        self.someone_north = Condition(self.mutex) # Condición para ver si algún coche esta yendo hacia el norte en el tunel
        self.someone_south = Condition(self.mutex) # Condición para ver si algún coche esta yendo hacia el sur en el tunel
    
    # Si un coche quiere entrar el tunel hacia el norte, se espera a que no haya ninguno dentro yendo hacia el sur. 
    # Además espera a que sea su turno o no hayan coches esperando a entrar en sentido contrario, en cuyo caso toma el turno.
    def empty_direction_north(self):
        return self.cars_north.value == 0 and (self.turn.value == 1 or self.cars_north_waiting.value == 0)
    
    # Si un coche quiere entrar el tunel hacia el sur, se espera a que no haya ninguno dentro yendo hacia el norte. 
    # Además espera a que sea su turno o no hayan coches esperando a entrar en sentido contrario, en cuyo caso toma el turno.    
    def empty_direction_south(self):
        return self.cars_south.value == 0 and (self.turn.value == 0 or self.cars_south_waiting.value == 0)
    
    def wants_enter(self, direction):
        self.mutex.acquire()
        if direction == NORTH:
            self.cars_north_waiting.value += 1
            print("w", self.cars_north_waiting.value, self.cars_south_waiting.value)
            self.someone_south.wait_for(self.empty_direction_south)
            self.cars_north_waiting.value -= 1
            print("w", self.cars_north_waiting.value, self.cars_south_waiting.value)
            self.cars_north.value += 1
            self.allowed_passes.value = (self.allowed_passes.value + 1)%PASSES
            if self.cars_south_waiting.value == 0: # Si no hay coches que quieren pasar en sentido contrario, toma el turno para su lado
                self.turn.value = 0
                self.allowed_passes.value = 0
            print("N", self.allowed_passes.value)
            if self.allowed_passes.value == PASSES-1:
                self.turn.value = 1
        elif direction == SOUTH:
            self.cars_south_waiting.value += 1
            print("w", self.cars_north_waiting.value, self.cars_south_waiting.value)
            self.someone_north.wait_for(self.empty_direction_north)
            self.cars_south_waiting.value -= 1
            print("w", self.cars_north_waiting.value, self.cars_south_waiting.value)
            self.cars_south.value += 1
            self.allowed_passes.value = (self.allowed_passes.value + 1)%PASSES
            if self.cars_north_waiting.value == 0: # Si no hay coches que quieren pasar en sentido contrario, toma el turno para su lado
                self.turn.value = 1
                self.allowed_passes.value = 0
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
        direction = NORTH if random.randint(0,7)==1  else SOUTH # Cambiado 1 por 7 para comprobar que no hay inanición incluso cuando pasan muchos más del sur que del norte
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        time.sleep(random.expovariate(1/0.5)) # a new car enters each 0.5s

if __name__ == "__main__":
    main()
