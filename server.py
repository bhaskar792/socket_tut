#!/usr/bin/env python3
import threading
import skt_tut_util

PORT = 9595

def handle_connection(conn, addr):
    print(f"Got connection from {addr}")
    with conn:
        try:
            while True:
                    recd = skt_tut_util.recv_str(conn)
                    print(f"{addr}: {recd}")
                    skt_tut_util.send_str(conn,f"Thanks for sending <{recd}>")
        except skt_tut_util.CommError:
            print(f"{addr} disconnected")

print(f'Server listening on port {PORT}')
with skt_tut_util.bind_and_listen(PORT) as s:
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_connection, args=(conn, addr))
        t.start()
