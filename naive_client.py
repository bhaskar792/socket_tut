#!/usr/bin/env python3
import socket
import sys

server_ip = sys.argv[1]
server_port = int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((server_ip, server_port))
    write_data = input()
    s.sendall(write_data.encode())
    print('Sent data to server')
