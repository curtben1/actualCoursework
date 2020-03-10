# -*- coding: utf-8 -*-
"""
server backend code using the sql reading libraries functions
"""

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