"""
server backend code using the sql reading libraries functions

integrate gameserver

test lobby voting

hook up a server list that reflects centrally hosted(remove ip and add location of object within ongoing games array maybe or 1 game at a time)
"""

import socket
from threading import *
import SQLreader as sql
import pickle
from gameServer import gameServer
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
port = 5050
print (host)
print (port)
serversocket.bind((host, port))

server = gameServer()

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()
        # self.run()

    def run(self):
        while 1:
            print("looping")
            inp = self.sock.recv(1024)
            inp = inp.decode("ascii")
            if inp  == "sList":
                reply = ""
                reply = sql.readsList()
                reply = pickle.dumps(reply)
            elif inp  == "stats":
                reply = sql.readStats()
                reply = reply.encode("ascii")
                pass    # send the stats for the current account maybe across a few transmissions or as a file
                
            elif inp != "":
                ipaddr = str(self.addr[0])
                sql.writeHost(inp,ipaddr)
                reply = "connected"
                reply = reply.encode("ascii")
                
            try:
                self.sock.send(reply)        # sends back a confirmation message
                print("sent")
                break
            except:
                print("not sent")
                pass
            
serversocket.listen(5)
print ('server started and listening')
while 1:
    print("looping 1")
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)
