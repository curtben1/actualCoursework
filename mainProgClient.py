import mainloop as mL
import socket

def main():
    menu=input("would you like to connect to the server or play a local hand (LOCAL/SERVER): ")
    if menu=="LOCAL":
        table=mL.Table()
        table.playHand()
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        host = ""   # ip of my home pc add this in later and maybe replace with pasberry pi                          
        port = 7070 # port forward this on my router
        s.connect((host, port))                               
        msg = s.recv(1024)                                     
        s.close()
        print (msg.decode('ascii'))

