"""
todo - hook up database to functioning playgame lobby

test the lobby voting 

vm pass = 1

"""


import socket
import pickle
from sys import getsizeof

"""s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = "86.157.43.62"   # ip of my home pc add this in later and maybe replace with pasberry pi
port = 5050 # port forward this on my router
s.connect((host, port))
servers = []"""

def options(menu):                
    if menu == "HOST":
        uName = input("what is your username (no spaces)")        # A placeholder until actual usernames are implemented 
        uName = uName.encode("ascii")
        s.send(uName)
        msg = s.recv(1024)
        s.close()
        msg = msg.decode('ascii')
    elif menu  == "VIEW":
        request = "sList"
        request = request.encode("ascii")
        s.send(request)
        msg = s.recv(1024)
        msg = pickle.loads(msg)
    return msg

def playGame(serverNum, serverList):     
    gamesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    """for row in serverList:
        if row[0]  == serverNum:
            host = row[2]
            break"""
    port = 6060         # port forwarded this on servers router
    gamesocket.connect(("81.135.23.12", port))
    playerInfo = ["command line", "playerNum"]  ## use actual info here
    msg = pickle.dumps(playerInfo)
    gamesocket.send(msg)


    while True: 
        
        data2 = gamesocket.recv(4096)
        if data2:
            data2 = pickle.loads(data2)
            if isinstance(data2, list):
                print(data2)
                break
                start = input("do you want to start the game now (YES/OTHER)")
                if start  == "YES":
                    msg =  pickle.dumps(start)
                    gamesocket.send(msg)
            else:
                print(data2)
                print("game starting")
                break
    while True:
        print("again")
        data = gamesocket.recv(4096)
        print("recieved")
        data = pickle.loads(data)   # http://acbl.mybigcommerce.com/52-playing-cards/ connect incoming data to labels with these cards
        
        try:
            data = data.split('#')
            if data[0]== '1'or data[0]=='6':
                try:
                    pot = int(data[1])
                    pickled  = pickle.dumps("None")
                    gamesocket.send(pickled)
                except:
                    if len(data) == 3:
                        print("the current bet to call is ", data[2])
                    val = input(data[1])
                    val = pickle.dumps(val)
                    gamesocket.send(val)
            else:
                print(data[1])
        except:
            print("notstring")
            try:
                print("sending")
                myvar = data[0]["chips"]
                var = pickle.dumps("None")
                gamesocket.send(var)
                print("sent")
            except Exception as exception:
                print(exception,"data was ", data)
                pass
            print(data)
            if data  == "game over":
                return "Game Over" 
        
        
def newServer():            # create a new server if there are rescources 
    sendval = None
    s.send()


def menu():     # the first function to get run
    menu = input("would you like to connect to the server or play a local hand or view the server list(LOCAL/SERVER/VIEW): ")     # ui element
    result = options(menu)
    if menu == "VIEW":
        print(result)
        selection = input("which server would you like to connect to (By serverID): ")        #ui element
        status = playGame(selection, result)
        if status  == "Game Over":
            menu()      # boots ended games back to menu, can have other status' with more info later if need be
    elif menu == "HOST":
        newServer()

#menu
if __name__ == "__main__":
    playGame(None,None)