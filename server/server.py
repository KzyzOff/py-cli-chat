import time
from dataclasses import dataclass
import socket
import threading
from queue import Queue


class Server:
    @dataclass
    class Message:
        sender: socket
        body: str

    def __init__(self, addr, port):
        self.MSGLEN = 1024
        self.HEADLEN = 64
        self.addr = addr
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.addr, self.port))
        self.clients: set[socket] = set()
        self.lock = threading.RLock()
        self.is_running = threading.Event()
        self.msg_queue = Queue()

    def _handle_client(self, conn: socket, addr):
        connected = True
        try:
            while connected:
                recv_len = 0
                received = ''
                conn.setblocking(True)
                msg_len = int(conn.recv(self.HEADLEN).decode('utf-8'))
                if msg_len == 0:
                    break
                conn.setblocking(False)
                while recv_len < msg_len:
                    received += conn.recv(self.MSGLEN).decode('utf-8')
                    recv_len += len(received)
                    if not received:
                        connected = False
                        break
                if received:
                    self.msg_queue.put(self.Message(conn, received))
                    print(f'[SERVER] ({addr}): {received}')
        finally:
            with self.lock:
                self.clients.remove(conn)
            conn.close()
            print(f'[SERVER] {addr} disconnected from the server.')

    def _resolve_messages(self):
        while not self.msg_queue.empty():
            msg = self.msg_queue.get()
            self._broadcast(msg)

    def _broadcast(self, msg: Message):
        with self.lock:
            for client in self.clients:
                if client is not msg.sender:
                    client.send(msg.body.encode('utf-8'))

    def _listen(self):
        client_ths: list[threading.Thread] = []
        listening = True
        try:
            while listening:
                conn, addr = self.socket.accept()
                with self.lock:
                    self.clients.add(conn)
                th = threading.Thread(target=self._handle_client,
                                      args=(conn, addr))
                th.start()
                client_ths.append(th)
        except OSError:
            print('[SERVER] Server is stopping to listen for new connections.')
        finally:
            for t in client_ths:
                t.join()

    def run(self, max_conns: int = 4):
        self.socket.listen(max_conns)
        listener = threading.Thread(target=self._listen)
        listener.start()
        try:
            while True:
                self._resolve_messages()
        except KeyboardInterrupt:
            print('[SERVER] Keyboard interrupt (CTRL + C). Server is shutting down...')
        finally:
            self.socket.close()
            listener.join()
