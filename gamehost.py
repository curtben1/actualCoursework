import socket
from threading import *
import SQLreader as sql
import pickle
import mainloop as ml

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"
port = 8080
serversocket.bind((host, port))
players=["host","0.0.0.0"]
def addPlayer(uName,address):
    players.append(uName,address)
    Continue=input("another player joined would you like to start or keep waiting (PLAY to start game)")
    if Continue == "PLAY":
        table=ml.Table(players)
        table.playHand()




class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()
        

    def run(self):

        while True:
            inp=self.sock.recv(1024)
            inp=inp.decode("ascii")
            players.append(inp,self.addr)
def listen():
    serversocket.listen(5)
    print ('server started and listening')
    while 1:
        clientsocket, address = serversocket.accept()
        client(clientsocket, address)
    
    
            