import mainloop as mL
import gamehost as gh
import socket
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = "86.170.85.22"   # ip of my home pc add this in later and maybe replace with pasberry pi                          
port = 7070 # port forward this on my router
s.connect((host, port))                            

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

def playGame():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    host = "0.0.0.0"   # ip of my home pc maybe replace with pasberry pi for constant service                         
    port = 8080
    s.bind((host, port))
    s.listen(5)
    while True:
        cs, address = s.accept()
        msg=cs.recv(1024)
        msg=msg.decode("ascii")   
        if msg[0] == "0":           #if it is just a message with no return necessary
            print(msg[1:len(msg)-1])
        else:                       # if the message needs to print and then take an input and retransmit
            reply=input(msg[1:len(msg)-1])
            reply.encode("ascii")
            cs.send(reply)

def menu():
    menu=input("would you like to connect to the server or play a local hand or view the server list(LOCAL/SERVER/VIEW): ")
    result=login(menu)
    if menu=="VIEW":
        print(result)
        selection=input("which server would you like to connect to (By serverID): ")
        for i in range(0,len(result)):
            if result[i][0]==selection:
                newip=result[i][2]
                port=8080
                s.connect((newip,port))
                transmission= input("enter your username: ")
                transmission = transmission.encode("ascii")
                s.send(transmission)
                playGame()
    elif menu=="HOST":
        gh.listen()

playGame()