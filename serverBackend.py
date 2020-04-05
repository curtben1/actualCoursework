# -*- coding: utf-8 -*-
"""
server backend code using the sql reading libraries functions
"""

import socket
from threading import *
import SQLreader as sql

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"
port = 7070
ipdict={}
print (host)
print (port)
serversocket.bind((host, port))

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1:
            inp=self.sock.recv(1024)
            inp=inp.decode("ascii")
            if inp == "sList":
                reply=""
                reply=sql.readsList()
                print(reply)
            elif inp == "stats":
                reply=sql.readStats()
                pass    # send the stats for the current account maybe across a few transmissions or as a file
                
            elif inp != "":  
                ipdict[inp]=self.addr        # adds the ip info to a dictionary using the username as a key
                print(ipdict)
                reply="connected"
            try:
                reply=reply.encode("ascii")
                self.sock.send(reply)        # sends back a confirmation message
                print("sent")
                break
            except:
                print("not sent")
                pass
            


serversocket.listen(5)
print ('server started and listening')
while 1:
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)
    
