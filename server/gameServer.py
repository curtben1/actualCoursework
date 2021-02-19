import mainloop
import socket
import pickle
 
class gameServer:

    def __init__(self):
        self.playerList = []
        self.playerListCV = []      # need a seperate list for sending to clients as version with sockets cant be serialised
        self.gameSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        host = "0.0.0.0"    # self
        port = 6060         # port forwarded this on servers router
        self.gameSock.bind((host, port))
        self.connections = []
        self.publicise()

    def publicise(self):
        tempSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "86.160.32.246"
        port = 5050
        msg = str(input("Server Name: "))
        msg = (0, msg)
        message = pickle.dumps(msg)
        tempSock.connect((host, port))
        tempSock.send(message)

    def lobby(self,maxPlayers):
        votes = 0
        counter = 0

        while len(self.playerList)<maxPlayers or votes < len(self.playerList) -1:
            print("listening")
            self.gameSock.listen(5)
            client, addr =self.gameSock.accept()

            print("connection from", addr)
            self.connections.append(client)
            player = client.recv(1024)
            player = pickle.loads(player)
            playerDict = {  "username":player[0], 
                        "playerNum":player[1],
                        "socket":client}
            if isinstance(player, list):
                self.playerList.append(playerDict)
                self.playerListCV.append({"username":player[0], "playerNum":player[1]})     # player dict without sockets so it can be serialised
                pickleList = pickle.dumps(self.playerListCV)

                #for indisock in self.connections:
                
                counter +=1 # for test
                print(counter)
                if counter == 2:
                    break
            else:
                votes += 1
                print(votes)
        for indisock in self.connections:
            indisock.send(pickleList)
        table = mainloop.Table(self.playerList, self.gameSock)
        while True:
            table.playHand()
            """if len(table.newhand.players) <= 1:
                tempSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                host = "86.134.82.174"
                port = 5050
                msg = (0, "end")
                message = pickle.dumps(msg)
                tempSock.connect((host, port))
                tempSock.send(message)
                main()
            else:
                tempSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                host = "86.134.82.174"
                port = 5050
                msg = (0, "end")
                message = pickle.dumps(msg)
                tempSock.connect((host, port))
                tempSock.send(message)
"""

def main():
    gs = gameServer()
    maxplayers = int(input("How many players: "))
    gs.lobby(maxplayers)

if __name__ == "__main__":
    main()