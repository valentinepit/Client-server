import json
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM

from common.config import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from common.utils import send_msg, receive_msg, get_address_and_port


class Client:

    def __init__(self, address, port):
        self.server_port = port
        self.server_address = address

    def get_transport(self):
        transport = socket(AF_INET, SOCK_STREAM)
        transport.connect((self.server_address, self.server_port))
        return transport

    def check_server(self):
        transport = self.get_transport()
        msg = self.create_presence()
        send_msg(transport, msg)
        try:
            answer = self.process_ans(receive_msg(transport))
            print(answer)
        except(ValueError, json.JSONDecodeError):
            print("Не удается расшифровать сообщение")

    def create_presence(self, account_name="Guest"):
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: account_name
            }
        }
        return out

    def process_ans(self, message):
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200 : OK'
            return f'400: {message[ERROR]}'
        raise ValueError


def main():
    address, port = get_address_and_port(sys.argv)
    if not address:
        sys.exit(1)
    client = Client(address, port)
    client.check_server()


if __name__ == "__main__":
    main()
