#!/usr/bin/env python3
import threading
import skt_tut_util
import socket
from queue import Queue

PORT = 9876


class AllQueues(object):
    LockType = threading.Lock
    Name = str
    Message = str
    QueueEntry = tuple[Name, Message]
    SingleQueue = Queue[QueueEntry | None]
    Conns = dict[Name, SingleQueue]

    def __init__(self) -> None:
        self.lock = AllQueues.LockType()
        self.connections = AllQueues.Conns()


    def place_stop(self,name: Name) -> bool:
        with self.lock:
            if name not in self.connections: 
                return False
            self.connections[name].put(None)
            return True

    def place_message(self, recv: Name, sender: Name, msg: Message) -> bool:
        with self.lock:
            assert self.lock.locked()
            if recv not in self.connections:
                return False
            self.connections[recv].put((sender, msg))
            return True

    def add_queue(self, name: Name) -> SingleQueue | None:
        with self.lock:
            assert (self.lock.locked())
            if name in self.connections:
                return None
            ret = AllQueues.SingleQueue()
            self.connections[name] = ret
            return ret

    def delete_queue(self, name: Name) -> bool:
        with self.lock:
            assert self.lock.locked()
            if name not in self.connections:
                return False
            self.connections.pop(name)
            return True


def client_sender(skt: socket.socket, me_queue: AllQueues.SingleQueue):
    while True:
        next_val = me_queue.get()
        if next_val is None:
            return

        try:
            skt_tut_util.send_str(skt, f"{next_val[0]} >> {next_val[1]}")
        except skt_tut_util.CommError:
            return


def client_recvr(me: AllQueues.Name, skt: socket.socket, all_queues: AllQueues):
    while True:
        try:
            recvr = skt_tut_util.recv_str(skt)
            msg = skt_tut_util.recv_str(skt)
            ret = all_queues.place_message(recvr, me, msg)
            if not ret:
                ok = all_queues.place_message(
                    me, '!!!', f'{recvr} does not exist')
                assert ok
        except skt_tut_util.CommError:
            ok = all_queues.place_stop(me)
            assert ok
            return


def client_connection(all_queues: AllQueues, skt: socket.socket, addr):
    with skt:
        potential_name = None
        potential_queue = None
        try:
            potential_name = skt_tut_util.recv_str(skt)
            print(f"{addr} with name <{potential_name}> trying to join!")

            potential_queue = all_queues.add_queue(potential_name)
            if potential_queue is None:
                skt_tut_util.send_str(skt, f"{potential_name} already taken")
                return

        except skt_tut_util.CommError:
            return
        assert type(potential_name) is not None
        assert type(potential_queue) is not None

        print(f"{potential_name} has joined!")
        recvr_thread = threading.Thread(
            target=client_recvr, args=(potential_name, skt, all_queues))
        recvr_thread.start()
        sendr_thread = threading.Thread(
            target=client_sender, args=(skt, potential_queue))
        sendr_thread.start()

        sendr_thread.join()
        recvr_thread.join()
        ok = all_queues.delete_queue(potential_name)
        assert ok
        print(f"{potential_name} has left!")


print(f'Server listening on port {PORT}')
all_queues = AllQueues()
with skt_tut_util.bind_and_listen(PORT) as s:
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=client_connection, args=(all_queues,conn, addr))
        t.start()
