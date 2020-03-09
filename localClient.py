'''
takes the client pc's inputs when prompted and returns them over the network
'''
import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

port = 8888

# connection to hostname on the port.
s.connect((host, port))                               

# Receive no more than 1024 bytes
msg = s.recv(1024)                                     
answer=input(msg.decode('ascii'))


s.close()
sendAns(answer,s,host,port)
def sendAns(answer,s,host,port):
    s.bind((host, port))                                  

    # queue up to 5 requests
    s.listen(5)   
    while True:
        # establish a connection
        clientsocket,addr = s.accept()      

        print("Got a connection from %s" % str(addr))
        if type==0:
            msg="Do you want to \nCall(C)\nRaise(R)\nFold(F)\n " + "\r\n"
        else:
            msg="Do you want to \nCheck(C)\nRaise(R)\nFold(F)\n " + "\r\n"
        clientsocket.send(msg.encode('ascii'))        
        clientsocket.close()

sendAns(answer,s,host,port)