import select
import sys
import logging
import time

from log import log_conf
from socket import socket, AF_INET, SOCK_STREAM

from common.config import ACTION, PRESENCE, USER, ACCOUNT_NAME, \
    RESPONSE_DEFAULT_IP_ADDRESS, ERROR, MAX_CONNECTION, TIME
from common.utils import receive_msg, send_msg, get_address_and_port, log

logger = logging.getLogger('server')


class Server:

    def __init__(self, address, port):
        self.listen_port = port
        self.listen_address = address

    @log
    def get_transport(self):
        transport = socket(AF_INET, SOCK_STREAM)
        transport.bind((self.listen_address, self.listen_port))
        transport.settimeout(0.5)
        return transport

    @log
    def process_client_message(self, message, _clients):
        logger.debug(f"Разбор сообщения от клиента. {message}")
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
            for client in _clients:
                send_msg(client, message)
        logger.debug(f"{ERROR}: Bad Request")
        return {
            RESPONSE_DEFAULT_IP_ADDRESS: 400,
            ERROR: 'Bad Request'
        }

    @log
    def get_client_message(self):
        clients = []
        messages = []
        transport = self.get_transport()
        transport.listen(MAX_CONNECTION)
        while True:
            try:
                client, client_address = transport.accept()
            except OSError:
                pass
            else:
                logger.info(f'Установлено соединение с клиентом {client_address}')
                clients.append(client)

            recv_data_lst = []
            send_data_lst = []

            try:
                if clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
            except OSError:
                pass

            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        msg = receive_msg(client_with_message)
                        self.process_client_message(msg, send_data_lst)
                    except:
                        logger.info(f'Клиент {client_with_message.getpeername()} '
                                    f'отключился от сервера.')
                        clients.remove(client_with_message)

            if messages and send_data_lst:
                message = {
                    ACTION: PRESENCE,
                    'SENDER': messages[0][0],
                    TIME: time.time(),
                    'msg_text': messages[0][1]
                }
                del messages[0]
                for waiting_client in send_data_lst:
                    try:
                        send_msg(waiting_client, message)
                    except:
                        logger.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                        waiting_client.close()
                        clients.remove(waiting_client)


def main():
    address, port, _ = get_address_and_port(sys.argv)
    if not address:
        sys.exit(1)
    server = Server(address, port)
    server.get_client_message()


if __name__ == "__main__":
    main()
