import mainloop as mL
import socket
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = "86.170.85.22"   # ip of my home pc add this in later and maybe replace with pasberry pi                          
port = 7070 
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


def menu():
    menu=input("would you like to connect to the server or play a local hand or view the server list(LOCAL/HOST/VIEW): ")
    returned=login(menu)
    if menu=="VIEW":
        print("Server list is: \n",returned)
        serverChoice=input("which server id do you want")
        for i in range(len(returned)):
            if returned[i][0] == serverChoice:
                newip=returned[i][2]
                break
        s.connect((newip,8080))
        uName=input("username: ")       #temp, once db structure+logons are setup it will read from there. This is for testing
        request=uName
        request = request.encode("ascii")
        s.send
