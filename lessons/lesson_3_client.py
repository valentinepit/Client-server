import json
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM
import logging
from log import log_conf

from common.config import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from common.utils import send_msg, receive_msg, get_address_and_port

log = logging.getLogger('client')


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
        answer = ''
        try:
            answer = self.process_ans(receive_msg(transport))
            log.info(f"Получен ответ от сервера: {answer}")
        except(ValueError, json.JSONDecodeError):
            log.error(f"Не удается расшифровать сообщение {answer}")
        except ConnetionRefusedError:
            log.critical(f"Не удается подключиться к серверу {self.server_address}:{self.server_port}")
        except ReqFileMissingError as error:
            log.error(f"В ответе сервера отсутствует необходимое поле {error}")

    def create_presence(self, account_name="Guest"):
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: account_name
            }
        }
        log.info(f"Сформировано сообщение {PRESENCE} для пользователя {account_name}")
        return out

    def process_ans(self, message):
        log.debug(f"Разбор сообщения от сервера: {message}")
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200 : OK'
            return f'400: {message[ERROR]}'
        raise ValueError


def main():
    address, port = get_address_and_port(sys.argv)
    if not address:
        log.critical(f"Попытка вызова сервера без указания адреса")
        sys.exit(1)
    client = Client(address, port)
    log.info(f"Запущен клиент. Адрес сервера: {address}, порт: {port}")
    client.check_server()


if __name__ == "__main__":
    main()
