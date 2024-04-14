#!/usr/bin/env python3
import threading
import util

PORT = 9595



def handle_connection(conn, addr):
    print(f"Got connection from {addr}")
    with conn:
        try:
            while True:
                    recd = util.recv_str(conn)
                    print(f"{addr}: {recd}")
                    util.send_str(conn,f"Thanks for sending {recd}")
        except util.CommError:
            print(f"{addr} disconnected")

print(f'Server listening on port {PORT}')
with util.bind_and_listen(PORT) as s:
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_connection, args=(conn, addr))
        t.start()
