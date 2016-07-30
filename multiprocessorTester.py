'''
Created on Jun 21, 2016

@author: TYchoi
'''

import os
from multiprocessing import Process, Pipe
from time import sleep

def ponger(p,s):
    count = 0
    while count < 100:
        msg = p.recv()
        print ("Process {0} got message: {1}".format(os.getpid(), msg))
        sleep(1)
        p.send(s)
        count += 1

def main():
    parent, child = Pipe()
    proc = Process(target=ponger, args=(child,"ping"))
    proc.start()
    parent.send("pong")
    ponger(parent, "pong")
    proc.join()
    proc.terminate()

if __name__ == "__main__":
    main()
    