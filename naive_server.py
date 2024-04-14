#!/usr/bin/env python3
import socket

PORT = 9595
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("",PORT))
s.listen()
print("Listening for a connection")
conn,addr = s.accept()
while(True):
    data = conn.recv(100)
    print(data)
    if not data: 
        break

