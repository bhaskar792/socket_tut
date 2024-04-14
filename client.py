#!/usr/bin/env python3
import util
import sys

#server_ip = sys.argv[1]
#server_port = int(sys.argv[2])

server_ip = "0.0.0.0"
server_port = 9595

with util.connect(server_ip,server_port) as skt:
    while(True):
        write_data = input()
        util.send_str(skt,write_data)
        resp = util.recv_str(skt)
        print(resp)
