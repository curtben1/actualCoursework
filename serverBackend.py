# -*- coding: utf-8 -*-
"""
server backend code using the sql reading libraries functions
"""
'''
import socket                                         

ipdict={}
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = socket.gethostname()                           
port = 7070                                          
serversocket.bind((host, port))                                  
serversocket.listen(5)                                           
while True:
    clientsocket,addr = serversocket.accept()      

    print("Got a connection from %s" % str(addr))
    msg = 'hello world'+ "\r\n"
    clientsocket.send(msg.encode('ascii'))
    clientsocket.close()







    #data = clientsocket.recv(1024).decode()
    #ipdict[data]=addr       adds the ip info to a dictionary using the username as a key

'''
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
            uName=inp.decode("ascii")
            if uName == "sList":
                sList=sql.readTable(mainDatabase.db, serverList)
            elif uName != ""    
                ipdict[inp]=self.addr        # adds the ip info to a dictionary using the username as a key
                print(ipdict)
            conf="connected"
            conf=conf.encode("ascii")
            self.sock.send(conf)        # sends back a confirmation message
            


serversocket.listen(5)
print ('server started and listening')
while 1:
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)
    
