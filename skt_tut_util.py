import socket

STRLEN_BYTES = 8

"""
We raise this for everything
"""

class CommError(Exception):
    pass

def wrap_comm_err(f,*args):
    try:
        return f(*args)
    except CommError:
        return CommError()


def bind_and_listen(port, ip = '') -> socket.socket:
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip,port))
        s.listen()
        return s
    except OSError:
        raise CommError()



def connect(ip, port) -> socket.socket:
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip,port))
        return s
    except OSError:
        raise CommError()

def recv_exactly(skt: socket.socket, count: int) -> bytes:
    ret = b''

    def pending():
        return count - len(ret)

    try:
        while (pending() > 0):
            d = skt.recv(pending())
            if not d:
                raise CommError()
            ret += d

        return ret
    except ConnectionResetError:
        raise CommError()



MAGIC_BYTES = b'magic'
def recv_str(skt: socket.socket) -> str:
    m1 = recv_exactly(skt,len(MAGIC_BYTES))
    if m1 != MAGIC_BYTES:
        raise CommError()
    str_len = int.from_bytes(recv_exactly(skt, STRLEN_BYTES),byteorder='little')
    ret =  recv_exactly(skt, str_len).decode()
    m2 = recv_exactly(skt,len(MAGIC_BYTES))
    if m2 != MAGIC_BYTES:
        raise CommError()
    return ret


def send_str(conn: socket.socket, string: str) -> None:
    try:
        p1  = int.to_bytes(len(string),STRLEN_BYTES,byteorder='little')
        assert len(p1) == STRLEN_BYTES
        conn.sendall(MAGIC_BYTES)
        conn.sendall(p1)
        conn.sendall(string.encode())
        conn.sendall(MAGIC_BYTES)
    except OSError:
        raise CommError()
