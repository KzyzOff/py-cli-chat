import socket
from dataclasses import dataclass
from enum import Enum


class Command(Enum):
    QUIT = '/quit'


@dataclass
class Message:
    """

    Attributes
    ----------
    head : int
        int representing how long (in bytes) is the body; head length is always 64 bytes
    command : Command
        tells the server what user wants to do
    sender : socket.AF_INET
        sender ip address
    body : str
        string representing body of the message
    """
    head: int
    command: Command
    sender: socket.AF_INET
    body: str


# TODO: Read about 'pup design pattern'
# https://www.cs.uaf.edu/courses/cs441/notes/protocols/index.html
# TODO: Remember about network byte order!
def msg2bytes(msg: Message, fmt: str = 'utf-8') -> str:
    pass


def bytes2msg(msg: str) -> Message:
    pass


def right_pad(data: str, width_bytes: int) -> str:
    return ' ' * (width_bytes - len(data)) + data
