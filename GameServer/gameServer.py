import mainloop
import socket
import pickle

class gameServer:

    def __init__(self):
        self.playerList = []

        self.gameSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        host = "0.0.0.0"    # self
        port = 5050         # port forwarded this on servers router
        self.gameSock.bind(host, port)

    def lobby(self,maxPlayers):
        votes = 0
        while len(self.playerList)<maxPlayers and votes < len(self.playerList) -1:
            player = self.gameSock.recv(1024)
            player = pickle.loads(player)
            if isinstance(player, list):
                self.playerList.append(player)
                pickleList = pickle.loads(self.playerList)
                self.gameSock.sendall(pickleList)
            else:
                votes += 1
        table = mainloop.Table(self.playerList, self.gameSock)
        while True:
            table.playHand()
            