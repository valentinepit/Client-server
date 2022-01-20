import json
import unittest

from common import config
from common.utils import receive_msg, send_msg


class TestSocket:
    encoded_msg = None
    received_msg = None

    def __init__(self, test_dict):
        self.test_dict = test_dict

    def send(self, msg_to_send):
        json_test_msg = json.dumps(self.test_dict)
        self.encoded_msg = json_test_msg.encode(config.ENCODING)
        self.received_msg = msg_to_send

    def recv(self, max_len):
        json_test_msg = json.dumps(self.test_dict)
        return json_test_msg.encode(config.ENCODING)


class TestUtils(unittest.TestCase):
    test_dict_send = {
        config.ACTION: config.PRESENCE,
        config.TIME: 111111.111111,
        config.USER: {
            config.ACCOUNT_NAME: 'test_test'
        }
    }
    test_dict_recv_ok = {config.RESPONSE: 200}
    test_dict_recv_err = {
        config.RESPONSE: 400,
        config.ERROR: 'Bad Request'
    }

    def setUp(self):
        # Предварительная настройка
        pass

    def tearDown(self):
        # Выполнить завершающие действия (если необходимо)
        pass

    def test_send_msg(self):
        test_socket = TestSocket(self.test_dict_send)
        send_msg(test_socket, self.test_dict_send)
        self.assertEqual(test_socket.encoded_msg, test_socket.received_msg)

    def test_rise_type_err(self):
        test_socket = TestSocket(self.test_dict_send)
        self.assertRaises(TypeError, send_msg, test_socket, "wrong dictionary")

    def test_get_ok_msg(self):
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        self.assertEqual(receive_msg(test_sock_ok), self.test_dict_recv_ok)

    def test_get_err_msg(self):
        test_sock_err = TestSocket(self.test_dict_recv_err)
        self.assertEqual(receive_msg(test_sock_err), self.test_dict_recv_err)
