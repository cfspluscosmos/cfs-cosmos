from multiprocessing.connection import Client
from multiprocessing.connection import Listener
from collections import deque
import sys

class MsgManager:
    
    def __init__(self):
        #open connection for telemetry
        tlmAddress = ('localhost', 6000)
        
        #open connection for Sensors.py
        senAddress = ("localhost", 5432)
        sen = Client(address)

        queue = deque(["IDL"])

    def getTlm(self):
        listener = Listener(tlmAddress)
        tlm = listener.accept()
        msg = tlm.recv()
        print("Connection with Telemetry System accepted")
        queue.append(msg)

    def forwardTlm(self):
        data = queue.popleft()
        sen.send(data)
        
