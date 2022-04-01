#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 17:58:52 2022
@author: hector
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

PASSES = 3

NCARS = 100


class Monitor():
    def __init__(self):
        self.cars_north = Value('i', 0)
        self.cars_south = Value('i', 0)
        self.turn = Value("i", 0)
        self.mutex = Lock()
        self.someone_north = Condition(self.mutex)
        self.someone_south = Condition(self.mutex)
        self.want_south = Value ("i", 0)
        self.want_north = Value ("i", 0)


    def empty_direction_north(self):
        return self.cars_north.value == 0 and (self.turn.value == 1 or self.want_north.value == 0)

    def empty_direction_south(self):
        return self.cars_south.value == 0 and (self.turn.value == 0 or self.want_south.value == 0)

    def wants_enter(self, direction):
        self.mutex.acquire()
        if direction == NORTH:
            self.want_north.value += 1
            print("WN", self.want_north.value)
            self.someone_south.wait_for(self.empty_direction_south)
            self.cars_north.value += 1
            self.allowed_north.value = (self.allowed_north.value + 1)
            print("N", self.allowed_north.value)
            if self.want_north.value >2:
                self.turn.value = 1
        elif direction == SOUTH:
            self.want_south.value += 1
            print("WS", self.want_south.value)
            self.someone_north.wait_for(self.empty_direction_north)
            self.cars_south.value += 1
            self.allowed_south.value = (self.allowed_south.value + 1)
            print("S", self.allowed_south.value)
            if self.want_south.value >2:
                self.turn.value = 0
        print(self.cars_north.value, self.cars_south.value)
        self.mutex.release()

    def leaves_tunnel(self, direction):
        self.mutex.acquire()
        if direction == NORTH:
            self.cars_north.value -= 1
            self.want_north.value -= 1
            self.someone_north.notify_all()
        elif direction == SOUTH:
            self.cars_south.value -= 1
            self.want_south.value -= 1
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
