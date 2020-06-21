import mainloop as mL
import gamehost as gh
import socket
import pickle

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM,0) 
host = "2a00:23c5:c001:9800:7c71:7eb4:f28d:ed00"   # ip of my home pc add this in later and maybe replace with pasberry pi
port = 5050 # port forward this on my router
s.connect((host, port,0,0))

def login(menu):                # may need to make each of these there there own function for when ui gets integrated
    if menu=="LOCAL":
        table=mL.Table()
        table.playHand()
    elif menu=="HOST":
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

def playGame(hostAddr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 8080
    s.bind((hostAddr, port))
    s.listen(5)
    message = s.recv()
    message=message.decode('ascii')
    if message == "joined game":
        pass
    else:
        retry = input("something has gone wrong failed to connect to the host \nWould you like to retry the connection or quit \nType QUIT to exit the application ")       # might be hard to ui this so could return failure and abstract the choice back out to mainprogclient
        if retry != "QUIT":
            playGame(hostAddr)
        else:
            return "Game Over"

def menu():
    menu=input("would you like to connect to the server or play a local hand or view the server list(LOCAL/SERVER/VIEW): ")
    result=login(menu)
    if menu=="VIEW":
        print(result)
        selection=input("which server would you like to connect to (By serverID): ")
        for i in range(0,len(result)):
            if result[i][0]==selection:             # all needs ipdating for new hole punch method, honestly might as well redo whole file at this point
                newip=result[i][2]
                port=8080
                s.connect((newip,port))
                transmission= input("enter your username: ")
                transmission = transmission.encode("ascii")
                s.send(transmission)
                status = playGame(newip)
                if status == "Game Over":
                    menu()      # boots ended games back to menu, can have other status' with more info later if need be
    elif menu=="HOST":
        gh.listen()

menu()