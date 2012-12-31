#!/usr/bin/env python

import threading
import random
import time 

class Philosopher(threading.Thread): 
    running = True 
    def __init__(self, xname, forkLeft, forkRight):
        threading.Thread.__init__(self)
        self.name = xname
        self.forkLeft = forkLeft
        self.forkRight = forkRight
 
    def run(self):
        while(self.running):      
            time.sleep( random.uniform(1,3))
            print '%s jest glodny.' % self.name
            self.dine()
 
    def dine(self):
        fork1, fork2 = self.forkLeft, self.forkRight
 
        while self.running:
            fork1.acquire(True) #czekaj na pierwszy widelec
            locked = fork2.acquire(False) #próba zarbrana drugiego zasobu
            if locked: break  #jezeli zostal zablokowany drugi zasob to zacznij jesc
            fork1.release()   #jezeli drugi zasob nie mogl zostac zajety to zwolij pierwszy       
        else:
            return
 
        self.dining()
        fork2.release()
        fork1.release()
 
    def dining(self):			
        print '%s zaczyna jesc '% self.name
        time.sleep(random.uniform(1,10))
        print '%s skonczyl jesc.' % self.name
 
def DiningPhilosophers():
    forks = [threading.Lock() for n in range(5)]
    philosopherNames = ('Filozof #1','Filozof #2','Filozof #3','Filozof #4', 'Filozof #5')
 
    philosophers = [Philosopher(philosopherNames[i], forks[i%5], forks[(i+1)%5]) \
            for i in range(5)] 
 
    Philosopher.running = True
    for p in philosophers: p.start()
    time.sleep(10)
    Philosopher.running = False
    print ("Filozofie który już rozpoczeli jedzienie musza jeszcze skonczyc")

if __name__ == "__main__":
    DiningPhilosophers()
