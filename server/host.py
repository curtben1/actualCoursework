"""
goes on my pc and handles passthrough to punch sockets and traverse nats

"""

import socket
import struct
import sys

server_listening_port = 7070

sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockfd.bind(("", server_listening_port))
print("listening on the port", str(server_listening_port))

client_requests=[]

while True:
    data, addr = sockfd.recvfrom(32)
    client_requests.append(addr)
    print("connection from", str(addr))

    if len(client_requests)==2:         # take player numbers from server list of active servers
        break

client_a_ip = client_requests[0][0]     # recode so it knows/ recognises and always talks host + one other, will be hard but its 100% possible
client_a_port = client_requests[0][1]
client_b_ip = client_requests[1][0]
client_b_port = client_requests[1][1]

msg = str(client_a_ip)+':'+str(client_a_port)
msg = msg.encode("ascii")
msg2 = str(client_b_ip)+':'+str(client_b_port)
msg2 = msg2.encode("ascii")

sockfd.sendto(msg,client_requests[1])     
sockfd.sendto(msg2, client_requests[0])   
sockfd.close()