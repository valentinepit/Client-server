import json
import sys
from socket import socket, AF_INET, SOCK_STREAM

from common.config import ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE, \
    RESPONSE_DEFAULT_IP_ADDRESS, ERROR, MAX_CONNECTION, TIME
from common.utils import receive_msg, send_msg, get_address_and_port


class Server:

    def __init__(self, address, port):
        self.listen_port = port
        self.listen_address = address

    def get_transport(self):
        transport = socket(AF_INET, SOCK_STREAM)
        transport.bind((self.listen_address, self.listen_port))
        return transport

    def process_client_message(self, message):
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
            return {RESPONSE: 200}
        return {
            RESPONSE_DEFAULT_IP_ADDRESS: 400,
            ERROR: 'Bad Request'
        }

    def get_client_message(self):
        transport = self.get_transport()
        transport.listen(MAX_CONNECTION)
        while True:
            client, client_address = transport.accept()
            try:
                message_from_client = receive_msg(client)
                print(message_from_client)
                response = self.process_client_message(message_from_client)
                send_msg(client, response)
                client.close()
            except (ValueError, json.JSONDecodeError):
                print("Принято некорректное сообщение")
                client.close()


def main():
    address, port = get_address_and_port(sys.argv)
    server = Server(address, port)
    server.get_client_message()


if __name__ == "__main__":
    main()
