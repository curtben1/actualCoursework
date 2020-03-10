import mainloop as mL
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = ""   # ip of my home pc add this in later and maybe replace with pasberry pi                          
port = 7070 # port forward this on my router
s.connect((host, port))                            

def main():
    menu=input("would you like to connect to the server or play a local hand (LOCAL/SERVER): ")
    if menu=="LOCAL":
        table=mL.Table()
        table.playHand()
    else:
        uName=input("what is your username (no spaces)")        # A placeholder until actual usernames are implemented 
        uName=uName.encode("ascii")
        s.send(uName)                             
        msg = s.recv(1024)                                     
        s.close()
        print (msg.decode('ascii'))

