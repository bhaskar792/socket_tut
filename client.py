#!/usr/bin/env python3
import skt_tut_util
import sys
server_ip = sys.argv[1]
server_port = int(sys.argv[2])


with skt_tut_util.connect(server_ip,server_port) as skt:
    while(True):
        write_data = input()
        skt_tut_util.send_str(skt,write_data)
        resp = skt_tut_util.recv_str(skt)
        print(resp)
