import json
import time
from functools import wraps
from typing import List
import inspect

from common.config import MAX_PACKAGE_LENGTH, ENCODING, DEFAULT_PORT, DEFAULT_IP_ADDRESS
import logging
from log import log_conf

log_s = logging.getLogger('server')
log_c = logging.getLogger('client')


def log(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        current_frame = inspect.currentframe()
        caller_frame = current_frame.f_back
        code_obj = caller_frame.f_code
        code_obj_name = code_obj.co_name
        current_log = log_c if 'client.py' in str(code_obj) else log_s
        cur_time = time.ctime(time.time())
        current_log.info(f" {cur_time} функция {func.__name__} вызвана из {code_obj_name}")
        _fn = func(*args, **kwargs)
        return _fn

    return wrap


def file_encoding_detect(_name):
    from chardet import detect
    with open(_name, 'rb') as f:
        content = f.read()
    encoding = detect(content)['encoding']
    return encoding


@log
def send_msg(socket, msg):
    if not isinstance(msg, dict):
        raise TypeError
    js_msg = json.dumps(msg)
    socket.send(js_msg.encode(ENCODING))


def receive_msg(client):
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def get_address_and_port(params: List):
    try:
        if '-a' in params:
            address = params[params.index('-a') + 1]
        else:
            address = DEFAULT_IP_ADDRESS
    except IndexError:
        print('После параметра \'-a\' должен быть указан IP-адрес')
        return None, None
    try:
        if '-p' in params:
            port = int(params[params.index('-p') + 1])
        else:
            port = DEFAULT_PORT
        if 65535 < port < 1024:
            raise ValueError
    except IndexError:
        print('После параметра \'-p\' должен быть указан номер порта')
        return None, None
    except ValueError:
        print('Порт может быть в диапазоне от 1024 до 65535')
        return None, None
    return address, port
