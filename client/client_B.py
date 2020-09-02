"""
For use by someone connecting to a server
"""

import socket
import sys
from requests import get

def get_ip():       # uses a basic api to get my public ip address
    ip = get('https://api.ipify.org').text
    return ip

def estCon(hostIP):       # udp hole punching code adapted from 
    gamesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = hostIP
    port = 7080     #manually port forwarded because holepunching is too hard, will continue to pursue in free time
    gamesocket.bind((host, port))
    return gamesocket

def main(socket):       # function that should normally be running when playing a game, recives any incoming messages and return the 
    while True:
        raw = socket.recvfrom(1024)
        dec = raw.decode("ascii")
        tag = dec.split(':')[0]
        dispData = dec.split(':')[1]    
        if tag == get_ip():       
            return dispData

        elif tag == "forAll":
            return dispData
        

def reply(socket, message):          # called if [0] == 1 is true for returned dispdata from main, this check goes in mainprogclient along with input so it can be used in ui 
    message = "Forhost:" + message      # adds tag so other devices know not to respond 
    message = message.encode("ascii")
    socket.sendall(message) 