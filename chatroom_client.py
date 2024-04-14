#!/usr/bin/env python3
import skt_tut_util
import threading
import sys

server_ip = ''
server_port = 9876


def msg_reader(skt):
    while(True):
        got = skt_tut_util.recv_str(skt)
        print(got)



def msg_writer(skt):
    while(True):
       write_data = input()
       skt_tut_util.send_str(skt,write_data)



with skt_tut_util.connect(server_ip,server_port) as skt:
    skt_tut_util.send_str(skt,"suraaj")
    t1 = threading.Thread(target=msg_reader,args=(skt,))
    t2 = threading.Thread(target=msg_writer,args=(skt,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
