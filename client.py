#!/usr/bin/env python3
import skt_tut_util

server_ip = ''
SERVER_PORT = 9595


with skt_tut_util.connect(server_ip,SERVER_PORT) as skt:
    while(True):
        write_data = input()
        skt_tut_util.send_str(skt,write_data)
        resp = skt_tut_util.recv_str(skt)
        print(resp)
