#!/usr/bin/env python3
import skt_tut_util
import threading
import sys

me_name = sys.argv[1]
server_ip = sys.argv[2]
me_file = open(me_name,'w')
server_port = 9876


def msg_reader(skt):
    while (True):
        got = skt_tut_util.recv_str(skt)
        me_file.write(got+'\n')
        me_file.flush()

def msg_writer(skt):
    while (True):
        print("Enter receiver: ",end='')
        recvr = input()
        print("Enter message: ",end='')
        msg = input()
        skt_tut_util.send_str(skt, recvr)
        skt_tut_util.send_str(skt, msg)


with skt_tut_util.connect(server_ip, server_port) as skt:
    skt_tut_util.send_str(skt, me_name)
    resp = skt_tut_util.recv_str(skt)
    print(resp)
    t1 = threading.Thread(target=msg_reader, args=(skt,))
    t2 = threading.Thread(target=msg_writer, args=(skt,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
