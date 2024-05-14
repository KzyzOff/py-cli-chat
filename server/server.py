from dataclasses import dataclass
import socket
import threading


@dataclass
class Message:
    sender: socket
    body: str


class Server:
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

    def _handle_client(self, conn: socket, addr):
        connected = True
        try:
            while connected:
                recv_len = 0
                received = ''
                msg_len = int(conn.recv(self.HEADLEN).decode('utf-8'))
                if msg_len == 0:
                    break
                while recv_len < msg_len:
                    received += conn.recv(self.MSGLEN).decode('utf-8')
                    recv_len += len(received)
                    if not received:
                        connected = False
                        break
                if received:
                    self._broadcast(Message(conn, received))
                    print(f'[SERVER] ({addr}): {received}')

        finally:
            with self.lock:
                self.clients.remove(conn)
            conn.close()
            print(f'[SERVER] {addr} disconnected from the server.')

    def _broadcast(self, msg: Message):
        for client in self.clients:
            # if client is not msg.sender:
            client.send(msg.body.encode('utf-8'))

    def run(self, max_conns: int = 4):
        self.socket.listen(max_conns)
        running = True
        while running:
            conn, addr = self.socket.accept()
            with self.lock:
                self.clients.add(conn)

            thread = threading.Thread(target=self._handle_client,
                                      args=(conn, addr))
            thread.start()
