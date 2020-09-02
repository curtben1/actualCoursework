import mainloop as mL
import gamehost as gh
import socket
import pickle
import client_B as holepunch

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM,0) 
host = "0.0.0.0"   # ip of my home pc add this in later and maybe replace with pasberry pi
port = 5050 # port forward this on my router
s.connect((host, port,0,0))

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

def playGame(hostAddr):     #the loop running while playing a remote game, should be constantly listening but also needs some holepunch modifications using client B
    gamesocket = holepunch.estCon(hostAddr)
    while True:
        data = holepunch.main(gamesocket)
        if data == "Game Over":     #ends the game
            break
        elif data[0] == 1:        # means it needs a reply
            output = data.substring(1,len(data)-2)
            replyData = input(output)       # ui element
            holepunch.reply(gamesocket, replyData)
        else:       # just needs to be displayed
            output = data.substring(1,len(data)-2)
            print(output)       # ui element
    return "Game Over"  # use this so I can return caught exceptions later

def menu():     # the first function to get run
    menu=input("would you like to connect to the server or play a local hand or view the server list(LOCAL/SERVER/VIEW): ")     # ui element
    result=options(menu)
    if menu=="VIEW":
        print(result)
        selection=input("which server would you like to connect to (By serverID): ")        #ui element
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