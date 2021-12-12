#!/usr/bin/python3
from backend.backend import SaunaBackend
from backend.api import SaunaApi
from frontend.gui import GUI

def main():
    backend = SaunaBackend()
    print('Main thread')
    gui = GUI(SaunaApi(backend))  
    gui.eventListenerLoop()
    gui.dispose()
    
if __name__ == '__main__':
    main()


