import socket
import time
from common.common import right_pad


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
        rdy2send = [f'[{i}] ' + msg for i in range(4)]
        rdy2send = list(map(lambda el: right_pad(str(len(el)), self.HEADLEN) + el, rdy2send))

        for m in rdy2send:
            self.socket.send(m.encode('utf-8'))
            print('[CLIENT] Message sent')
            time.sleep(2)

        end_msg = right_pad(str(len('')), self.HEADLEN)
        self.socket.send(end_msg.encode('utf-8'))

        self.socket.close()
