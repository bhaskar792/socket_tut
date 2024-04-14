#!/usr/bin/env python3
from http import server
import socket
import sys

server_ip = sys.argv[1]
server_port = int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((server_ip, server_port))
    s.sendall(b'a'*2000)
    print('Sent data to server')
    data = s.recv(1024)
    print('Received data: ', data)
