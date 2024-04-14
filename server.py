#!/usr/bin/env python3
import socket
import threading

PORT = 9595

def handle_connection(conn, addr):
    print("GOT CONNECTION FROM", str(addr))
    with conn:
        bytes_read = 0
        while True:
            data = conn.recv(128)
            if not data:
                break
            bytes_read += len(data)
            print(bytes_read)
            print("GOT SOME DATA", addr, data)
            if bytes_read >= 1024:
                print('Sending response to client')
                try:
                    conn.sendall(b'Thanks for the data!')
                except IOError:
                    pass
                break            

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("", PORT))
    s.listen()
    print('Server listening on port', str(PORT))
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_connection, args=(conn, addr))
        t.start()
