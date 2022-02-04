import json
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM
import logging
from log import log_conf

from common.config import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from common.errors import ReqFileMissingError
from common.utils import send_msg, receive_msg, get_address_and_port, log

logger = logging.getLogger('client')


class Client:
    def __init__(self, address, port):
        self.server_port = port
        self.server_address = address

    @log
    def get_transport(self):
        transport = socket(AF_INET, SOCK_STREAM)
        transport.connect((self.server_address, self.server_port))
        return transport

    @log
    def check_server(self):
        transport = self.get_transport()
        msg = self.create_presence()
        send_msg(transport, msg)
        answer = ''
        try:
            answer = self.process_ans(receive_msg(transport))
            logger.info(f"Получен ответ от сервера: {answer}")
        except(ValueError, json.JSONDecodeError):
            print()
            logger.error(f"Не удается расшифровать сообщение {answer}")
        except ConnectionRefusedError:
            print()
            logger.critical(f"Не удается подключиться к серверу {self.server_address}:{self.server_port}")
        except ReqFileMissingError as error:
            print()
            logger.error(f"В ответе сервера отсутствует необходимое поле {error}")
        transport.close()

    @log
    def create_presence(self, account_name="Guest"):
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: account_name
            }
        }
        logger.info(f"Сформировано сообщение {PRESENCE} для пользователя {account_name}")
        return out

    @log
    def process_ans(self, message):
        logger.debug(f"Разбор сообщения от сервера: {message}")
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200 : OK'
        else:
            return message['text']
        raise ValueError


class ListenerClient(Client):
    @log
    def check_server(self):
        print('Это клиент для прослушки')
        while True:
            transport = self.get_transport()
            answer = self.process_ans(receive_msg(transport))
            print(answer)


class SenderClient(Client):
    @log
    def check_server(self):
        while True:
            msg_text = input('Введите сообщение для группы. Для окончания введите exit: ')
            if msg_text == 'exit':
                break
            msg = self.create_presence()
            transport = self.get_transport()
            msg['text'] = msg_text
            send_msg(transport, msg)


def main():
    address, port, mode = get_address_and_port(sys.argv)
    if not address:
        logger.critical(f"Попытка вызова сервера без указания адреса")
        sys.exit(1)
    if mode == 'listen':
        client = ListenerClient(address, port)
    else:
        client = SenderClient(address, port)
    logger.info(f"Запущен клиент. Адрес сервера: {address}, порт: {port}, режим работы {mode}")
    client.check_server()


if __name__ == "__main__":
    main()
