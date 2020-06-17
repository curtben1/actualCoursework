"""
For use by someone connecting to a server
"""



import socket
import struct
import sys
import urllib
import re

def get_ip():       # uses a website to get public ip, function from https://stackoverflow.com/questions/58294/how-do-i-get-the-external-ip-of-a-socket-in-python
    group = re.compile(u'(?P<ip>\d+\.\d+\.\d+\.\d+)').search(urllib.URLopener().open('http://jsonip.com/').read()).groupdict()
    return group['ip']



def estCon():       # udp hole punching code adapted from 
    master = ("81.151.18.101",7070)     #add tuple of my pc address + a forwarded port
    me=("192.168.1.162",52527)           # my ip and a random port as tuple, 3:37 in vid


    try:
        sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sockfd.bind(("",0))
        msg1="Hello".encode("ascii")
        sockfd.sendto(msg1, master)

    except socket.error:
        print("Failed to create  socket")
        sys.exit

    peer_data, addr = sockfd.recvfrom(1024)
    print(peer_data.decode("ascii"))

    print("trying to com with peer")
    peer_data=peer_data.decode("ascii")
    peer_ip = peer_data.split(':')[0]
    peer_port = int(peer_data.split(':')[1])
    print(peer_ip,peer_port)
    sockfd.sendto("hello from your peer".encode("ascii"), (peer_ip, peer_port))

    while True:
        print("listening")

        datarec,sendaddr = sockfd.recvfrom(1024)
        datarec.decode("ascii")
        print("data rec",datarec)
        if datarec !=None:
            return sockfd

def main(socket):       # function that should normally be running when playing a game, recives any incoming messages and return the 
    while True:
        raw = socket.recvfrom(1024)
        dec = raw.decode("ascii")
        tag = dec.split(':')[0]    
        dispData = dec.split(':')[1]    
        if tag == get_ip():        # maybe outsource this to mainprogClient so it can deal with each differently
            return dispData
        elif tag == "forAll":
            return dispData
        

def reply(socket, message):          # called if [0] == 1 is true for returned dispdata from main, this check goes in mainprogclient along with input so it can be used in ui 
    message = "Forhost:" + message      # adds tag so other devices know not to respond 
    message = message.encode("ascii")
    socket.sendall(message) 