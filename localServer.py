'''
requests inputs from players and passes them into the mainloop
'''

import socket                                         
                                                                          
def sendReq(type,destIP):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # get local machine name
    host = socket.gethostname()                           

    port = 8888              
    serversocket.bind((host, port))                                  

    # queue up to 5 requests
    serversocket.listen(5)   
    while True:
        # establish a connection
        clientsocket,addr = serversocket.accept()      
        if addr==destIP:
            print("Got a connection from %s" % str(addr))
            if type==0:
                msg="Do you want to \nCall(C)\nRaise(R)\nFold(F)\n " + "\r\n"
            else:
                msg="Do you want to \nCheck(C)\nRaise(R)\nFold(F)\n " + "\r\n"
            clientsocket.send(msg.encode('ascii'))        
            clientsocket.close()
    
def recReq(destIP):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # get local machine name
    host = destIP                           

    port = 8888

    # connection to hostname on the port.
    s.connect((host, port))                               

    # Receive no more than 1024 bytes
    msg = s.recv(1024)                                     
    answer=msg.decode('ascii')
    s.close()
    return answer


def getInput(type,destIP):
    sendReq(type,destIP)
    answer=recReq(destIP)
    return answer