"""
For use by gamehost.py, works to holepunch to a device behind NAT
"""


import socket
import struct
import sys
import time
master = ("81.151.18.101",7070)     #home pc with port forwarding so no NAT traversal is necesary




def recvMsg(socket, message, targetIP):
    message = targetIP + ':' + message
    message = message.encode("ascii")
    socket.sendall(message)
    while True:
        retValue = socket.recvfrom(1024)
        retValue = retValue.decode("ascii")
        tag = retValue.split(':')[0]        # splits tage from main message
        if tag == "forHost":        # maybe add an else that returnes Null or an error
            retValue = retValue.split(':')[1]
            return retValue

def sendMsg(socket, message, targetIP):         # sends a message but takes no return, might not use if I always send a confirmation message which when using udp isnt a bad idea
    master = ("81.151.18.101",7070)     #add tuple of my pc address + a forwarded port
    me=("192.168.1.162",52527)           
    message = targetIP + ':' + message      # appends target ip as a tag then sends to everyone, the recipient can then check its for them but I dont need to worry too much abouy t knowing port numbers since I can just use sendAll
    message = message.encode("ascii")
    socket.sendall(message)
    