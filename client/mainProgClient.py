import socket
import pickle


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = "0.0.0.0"   # ip of my home pc add this in later and maybe replace with pasberry pi
port = 5050 # port forward this on my router
s.connect(host, port)
servers = []
def options(menu):                
    if menu=="HOST":
        uName=input("what is your username (no spaces)")        # A placeholder until actual usernames are implemented 
        uName=uName.encode("ascii")
        s.send(uName)
        msg = s.recv(1024)
        s.close()
        msg = msg.decode('ascii')
    elif menu == "VIEW":
        request = "sList"
        request=request.encode("ascii")
        s.send(request)
        msg=s.recv(1024)
        msg=pickle.loads(msg)
    return msg

def playGame(serverNum, serverList):     
    gamesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    for row in serverList:
        if row[0] == serverNum:
            host = row[2]
            break
    port = 5050         # port forwarded this on servers router
    gamesocket.bind(host, port)
    while True:
        data = gamesocket.recv(1024)
        data = pickle.loads(data)
        print(data)
        if isinstance(data, list):
            print(data)
            start = input("do you want to start the game now (YES/OTHER)")
            if start == "YES":
                msg = pickle.dumps(start)
                gamesocket.send(msg)
        else:
            print("game starting")
    while True:
        data = gamesocket.recv(1024)
        data = pickle.loads(data)
        if data == "game over":
            return "Game Over"
        
def newServer():
    sendval = 
    s.send()


def menu():     # the first function to get run
    menu=input("would you like to connect to the server or play a local hand or view the server list(LOCAL/SERVER/VIEW): ")     # ui element
    result=options(menu)
    if menu=="VIEW":
        print(result)
        selection=input("which server would you like to connect to (By serverID): ")        #ui element
        status = playGame(selection, result)
        if status == "Game Over":
            menu()      # boots ended games back to menu, can have other status' with more info later if need be
    elif menu=="HOST":
        newServer()

menu()