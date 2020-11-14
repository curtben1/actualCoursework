import mainloop
import socket
import pickle

class gameServer:

    def __init__(self):
        self.playerList = []

        self.gameSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        host = "0.0.0.0"    # self
        port = 6060         # port forwarded this on servers router
        self.gameSock.bind((host, port))
        self.connections = []
    def lobby(self,maxPlayers):
        votes = 0
        

        while len(self.playerList)<maxPlayers or votes < len(self.playerList) -1:
            print("listening")
            self.gameSock.listen(5)
            client, addr =self.gameSock.accept()

            print("connection from", addr)
            self.connections.append(client)
            player = client.recv(1024)
            player = pickle.loads(player)
            if isinstance(player, list):
                self.playerList.append(player)
                pickleList = pickle.dumps(self.playerList)

                #for indisock in self.connections:
                client.send(pickleList)
                break # for test
            else:
                votes += 1
                print(votes)

        table = mainloop.Table(self.playerList, self.gameSock)
        while True:
            table.playHand()

if __name__ == "__main__":
    gs = gameServer()
    gs.lobby(2)