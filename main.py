import os
import argparse
from dotenv import load_dotenv
from client.client import Client
from server.server import Server


if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(ROOT_DIR, '.env'))

    parser = argparse.ArgumentParser(
        prog='Python CLI chat',
        description='Simple CLI chat written in Python'
    )
    parser.add_argument('-t', '--type', type=str,
                        help='"client" or "server"', choices=['server', 'client'])

    args = parser.parse_args()

    if not args.type:
        print('type argument was not provided')
        exit(1)

    prog = None
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))
    match args.type:
        case 'client':
            prog = Client(host, port)
        case 'server':
            prog = Server(host, port)
        case _:
            print('type argument was not provided')
            exit(1)

    if prog is not None:
        prog.run()
