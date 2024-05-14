import socket
import time
from utils import right_pad


class Client:
    def __init__(self, addr, port):
        self.MSGLEN = 1024
        self.HEADLEN = 64
        self.addr = addr
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        # try:
        self.socket.connect((self.addr, self.port))
        msg = 'Yo from a client'
        msg = right_pad(str(len(msg)), self.HEADLEN) + msg
        self.socket.send(msg.encode('utf-8'))
        print('[CLIENT] Message sent')
        # rlen = 0
        # rcv = ''
        # while rlen < self.MSGLEN:
        #     print('Before recv...')
        #     rcv += self.socket.recv(self.MSGLEN).decode('utf-8')
        #     rlen += len(rcv)
        # print(f'Got from server: {rcv}')

        time.sleep(2)
        end_msg = right_pad(str(len('')), self.HEADLEN)
        self.socket.send(end_msg.encode('utf-8'))

        self.socket.close()
