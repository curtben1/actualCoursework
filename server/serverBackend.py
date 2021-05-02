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

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
port = 5050
print (host)
print (port)
serversocket.bind((host, port))



class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()
        # self.run()

    def run(self):
    
        print("looping")
        inp = self.sock.recv(1024)
        inp = pickle.loads(inp)
        print("the input is", inp)
        if inp[0] == 0:
            print("server Com")
            # server communications likely new server created or terminated
            if isinstance(inp[1], str):
                if inp[1] != "end":
                    sql.addServer(inp[1],self.addr[0])
                    print(sql.readsList())
                else:
                    sql.remServer(self.addr[0])

        elif inp[0] == 1:
            if inp[1]  == "sList":
                reply = sql.readsList()
                reply = pickle.dumps(reply)
            elif inp[1]  == "stats":
                reply = sql.readStats()
                reply = pickle.dumps(reply)

            elif inp[1] == "logon":
                username = inp[2][0]
                pword = inp[2][1]
                

            elif inp != "":
                ipaddr = str(self.addr[0])
                sql.writeHost(inp,ipaddr)
                reply = "connected"
                reply = reply.encode("ascii")
        elif inp[0] == 2:
            pass # password/account realted request, confirm access, create account etc
        elif inp[0] == 3:
            pass # stats/balance updates
        try:
            self.sock.send(reply)        # sends back a confirmation message
            print("sent")
            
        except:
            print("not sent")
            pass
            
serversocket.listen(5)
print ('server started and listening')
while 1:
    print("looping 1")
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)
