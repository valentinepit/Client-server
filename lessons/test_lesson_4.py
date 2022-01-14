import unittest
from socket import socket

from common import config
from lesson_3_client import Client
from lesson_3_server import Server


class ClientServerTest(unittest.TestCase):
    params = {
            'error_msg': '400: Bad Request',
            'ok_msg': '200 : OK',
            'ok_response': {'response': 200},
            'msg_params': {
                config.ACTION: config.PRESENCE,
                config.TIME: 1.1,
                config.USER: {config.ACCOUNT_NAME: 'Guest'}
            },
            'err_dict': {
                config.RESPONSE_DEFAULT_IP_ADDRESS: 400,
                config.ERROR: 'Bad Request'
            }
        }

    def setUp(self):
        # Предварительная настройка
        self.client = Client('127.0.0.1', 7777)
        self.server = Server('127.0.0.1', 7777)

    def tearDown(self):
        # Выполнить завершающие действия (если необходимо)
        pass

    def test_presence_valid(self):
        # "Проверка запроса на корректность"
        client = Client('127.0.0.1', 7777)
        test = client.create_presence()
        test['time'] = 1.1
        self.assertEqual(test, self.params['msg_params'])

    def test_presence_invalid(self):
        # "Проверка некорректного запроса"
        test = self.client.create_presence()
        test['time'] = 1.1
        self.assertNotEqual(test, {config.ACTION: config.PRESENCE, 'time': 1.1,
                                   config.USER: {config.ACCOUNT_NAME: 'Test'}})

    def test_200_ans(self):
        # Тест корректного разбора ответа
        self.assertEqual(self.client.process_ans({config.RESPONSE: 200}), self.params['ok_msg'])

    def test_400_ans(self):
        # Тест корректного разбора ответа
        self.assertEqual(self.client.process_ans({config.RESPONSE: 400, config.ERROR: 'Bad Request'}),
                         self.params['error_msg'])

    def test_no_response(self):
        # "Тест на исключение без поля Response"
        self.assertRaises(ValueError, self.client.process_ans, {config.ERROR: 'Bad Request'})

    def test_check_client_transport(self):
        # Проверка транспорта клиента
        server_transport = self.server.get_transport()
        server_transport.listen(config.MAX_CONNECTION)
        self.assertIsInstance(self.client.get_transport(), socket)

    def test_check_server_transport(self):
        # Проверка транспорта сервера
        self.assertIsInstance(self.server.get_transport(), socket)

    def test_to_chek(self):
        # Проверка на корректный запрос
        self.assertEqual(self.server.process_client_message(self.params['msg_params']), self.params['ok_response'])

    def test_wrong_action(self):
        self.assertEqual(self.server.process_client_message({config.ACTION: 'Wrong',
                                                             config.TIME: 1.1,
                                                             config.USER: {config.ACCOUNT_NAME: 'Guest'}}),
                         self.params['err_dict'])

    def test_no_action(self):
        self.assertEqual(
            self.server.process_client_message({config.TIME: 1.1, config.USER: {config.ACCOUNT_NAME: 'Guest'}}),
            self.params['err_dict'])

    def test_no_time(self):
        self.assertEqual(self.server.process_client_message({config.ACTION: config.PRESENCE,
                                                             config.USER: {config.ACCOUNT_NAME: 'Guest'}}),
                         self.params['err_dict'])

    def test_no_user(self):
        self.assertEqual(self.server.process_client_message({config.ACTION: config.PRESENCE, config.TIME: 1.1}),
                         self.params['err_dict'])

    def test_wrong_user(self):
        self.assertEqual(self.server.process_client_message({config.ACTION: config.PRESENCE, config.TIME: 1.1,
                                                             config.USER: {config.ACCOUNT_NAME: 'Test'}}),
                         self.params['err_dict'])


if __name__ == "__main__":
    unittest.main()
