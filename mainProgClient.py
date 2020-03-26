import mainloop as mL
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = "86.168.151.34"   # ip of my home pc add this in later and maybe replace with pasberry pi                          
port = 7070 # port forward this on my router
s.connect((host, port))                            

def main():
    menu=input("would you like to connect to the server or play a local hand or view the server list(LOCAL/SERVER/VIEW): ")
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
        s.send()
        msg=s.recv(1024)
        msg=msg.decode("ascii")
    return msg

main() 
