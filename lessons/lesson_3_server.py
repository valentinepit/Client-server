import json
import sys
import logging

from common.errors import IncorrectDataReceivedError
from log import log_conf
from socket import socket, AF_INET, SOCK_STREAM

from common.config import ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE, \
    RESPONSE_DEFAULT_IP_ADDRESS, ERROR, MAX_CONNECTION, TIME
from common.utils import receive_msg, send_msg, get_address_and_port

log = logging.getLogger('server')


class Server:

    def __init__(self, address, port):
        self.listen_port = port
        self.listen_address = address

    def get_transport(self):
        transport = socket(AF_INET, SOCK_STREAM)
        transport.bind((self.listen_address, self.listen_port))
        return transport

    def process_client_message(self, message):
        log.debug(f"Разбор сообщения от клиента. {message}")
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
            return {RESPONSE: 200}
        log.debug(f"{ERROR}: Bad Request")
        return {
            RESPONSE_DEFAULT_IP_ADDRESS: 400,
            ERROR: 'Bad Request'
        }

    def get_client_message(self):
        transport = self.get_transport()
        transport.listen(MAX_CONNECTION)
        while True:
            client, client_address = transport.accept()
            log.info(f'Установлено соединение с клиентом {client_address}')
            try:
                message_from_client = receive_msg(client)
                log.info(f"Получено сообщение {message_from_client}")
                response = self.process_client_message(message_from_client)
                log.info(f"Сформирован ответ {response}")
                send_msg(client, response)
                log.info(f"Закрытие сесси с клиентом {client_address}")
                client.close()
            except (ValueError, json.JSONDecodeError):
                log.error(f"Не удалось декодировать сообщение от {client_address}. Закрытие сесси с клиентом")
                client.close()
            except IncorrectDataReceivedError:
                log.error(f"Приняты некорректные данные от {client_address}. Закрытие сесси с клиентом")
                client.close()


def main():
    address, port = get_address_and_port(sys.argv)
    if not address:
        sys.exit(1)
    server = Server(address, port)
    server.get_client_message()


if __name__ == "__main__":
    main()
